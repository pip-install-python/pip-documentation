"""
Section Suggester for AI Chat

Analyzes AI responses and suggests relevant documentation sections
that users can jump to using URL hash navigation.
"""

import os
import json
import re
from typing import Dict, List, Optional
from anthropic import Anthropic
from .api_cost_logger import get_logger


class SectionSuggester:
    """Suggests relevant documentation sections based on AI responses."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the section suggester.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self.model = "claude-haiku-4-5-20251001"
        self.logger = get_logger()

    def _ensure_client(self):
        """Ensure the Anthropic client is initialized."""
        if self.client is None:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self.client = Anthropic(api_key=self.api_key)

    def build_system_prompt(self) -> str:
        """Build system prompt for section suggestion."""
        return """You are a documentation navigation assistant. Your job is to analyze a user's question and an AI response, then suggest the most relevant documentation sections they should read.

Return a JSON array with exactly 3 section suggestions (or fewer if not enough relevant sections exist):

[
    {
        "hash": "#installation",
        "title": "Installation",
        "relevance": 0.95,
        "reason": "The question asks about setup, and this section covers installation steps"
    }
]

Rules:
- Only suggest sections that are DIRECTLY relevant to the question and response
- Provide relevance score between 0 and 1 (1 = most relevant)
- Give a brief reason explaining why each section is relevant
- Order by relevance (highest first)
- Return valid JSON only, no extra text"""

    def suggest_sections(
        self,
        question: str,
        ai_response: str,
        toc: List[Dict[str, str]],
        session_id: str,
        page_path: str,
        max_suggestions: int = 3
    ) -> List[Dict[str, any]]:
        """
        Suggest relevant sections based on question and response.

        Args:
            question: User's original question
            ai_response: The AI's response text
            toc: Table of contents structure from ContextGatherer
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_suggestions: Maximum number of suggestions (default 3)

        Returns:
            List of suggested sections with hash, title, relevance, and reason
        """
        # Build TOC context
        toc_context = "Available sections:\n"
        for item in toc:
            indent = "  " * (item['level'] - 1)
            toc_context += f"{indent}- {item['text']} ({item['hash']})\n"

        user_prompt = f"""Analyze this interaction and suggest the most relevant documentation sections:

QUESTION:
{question}

AI RESPONSE:
{ai_response}

{toc_context}

Return a JSON array of up to {max_suggestions} section suggestions."""

        # Ensure client is initialized
        self._ensure_client()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=self.build_system_prompt(),
                messages=[{"role": "user", "content": user_prompt}]
            )

            # Log the API call
            self.logger.log_api_request(
                session_id=session_id,
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                call_type='suggest_sections',
                page_path=page_path,
                metadata={'question': question[:100]}
            )

            # Extract and parse JSON
            text = response.content[0].text
            suggestions = self._extract_json(text)

            # Validate and limit suggestions
            if isinstance(suggestions, list):
                # Ensure each suggestion has required fields
                validated = []
                for sug in suggestions[:max_suggestions]:
                    if all(key in sug for key in ['hash', 'title', 'relevance', 'reason']):
                        validated.append(sug)

                return validated

            return []

        except Exception as e:
            print(f"Error suggesting sections: {e}")
            return []

    def _extract_json(self, text: str) -> List[Dict]:
        """
        Extract JSON array from response text.

        Args:
            text: Response text that may contain JSON

        Returns:
            Parsed JSON list
        """
        # Try direct parse first
        try:
            result = json.loads(text)
            if isinstance(result, list):
                return result
            # If it's a dict with a 'suggestions' key, return that
            if isinstance(result, dict) and 'suggestions' in result:
                return result['suggestions']
        except:
            pass

        # Try to find JSON in code blocks
        patterns = [
            r'```json\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'\[.*\]',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                try:
                    result = json.loads(match.group(1) if '```' in pattern else match.group(0))
                    if isinstance(result, list):
                        return result
                except:
                    continue

        # Fallback: return empty list
        return []

    def simple_keyword_suggest(
        self,
        question: str,
        toc: List[Dict[str, str]],
        max_suggestions: int = 3
    ) -> List[Dict[str, any]]:
        """
        Simple keyword-based section suggestion (no API call).

        Useful as a fallback or for quick suggestions without API cost.

        Args:
            question: User's question
            toc: Table of contents
            max_suggestions: Maximum suggestions to return

        Returns:
            List of suggested sections
        """
        # Extract keywords from question (simple approach)
        question_lower = question.lower()
        keywords = re.findall(r'\b[a-z]{4,}\b', question_lower)

        suggestions = []
        for item in toc:
            title_lower = item['text'].lower()

            # Calculate simple relevance score based on keyword matches
            matches = sum(1 for kw in keywords if kw in title_lower)
            if matches > 0:
                relevance = min(matches / len(keywords), 1.0) if keywords else 0

                suggestions.append({
                    'hash': item['hash'],
                    'title': item['text'],
                    'relevance': round(relevance, 2),
                    'reason': f'Section title matches {matches} keyword(s) from your question'
                })

        # Sort by relevance and return top N
        suggestions.sort(key=lambda x: x['relevance'], reverse=True)
        return suggestions[:max_suggestions]