"""
Code Responder for AI Chat

Handles generation of code examples using a three-call architecture:
1. Generate code
2. Generate formatting instructions
3. Format code with instructions
"""

import os
import json
import re
from typing import Dict, Optional, Generator, List
from anthropic import Anthropic
from .api_cost_logger import get_logger


class CodeResponder:
    """Generates code examples for documentation questions."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the code responder.

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

    def build_system_prompt_generate(self) -> str:
        """Build system prompt for code generation."""
        return """You are an expert Dash developer specializing in creating interactive data visualization applications.

Your role is to generate complete, working code examples that:
1. Follow Dash best practices and patterns
2. Are production-ready and well-documented
3. Include proper imports and component structure
4. Use dash-mantine-components when appropriate
5. Include callbacks for interactivity

Generate clean, documented Python code that users can run immediately."""

    def build_system_prompt_format_instructions(self) -> str:
        """Build system prompt for formatting instructions."""
        return """You are a code formatting expert. Your job is to analyze raw code and create clear, structured formatting instructions.

Generate a JSON object with the following structure:
{
    "files": [
        {
            "filename": "app.py",
            "language": "python",
            "description": "Main application file",
            "highlights": ["Lines 10-15 show callback pattern", "Line 25 demonstrates state management"]
        }
    ],
    "overall_description": "Brief description of what the code does",
    "key_concepts": ["callback", "state", "layout"]
}

Be precise and helpful."""

    def build_system_prompt_format(self) -> str:
        """Build system prompt for final formatting."""
        return """You are a code presentation specialist. Format the provided code according to the instructions into a clean JSON structure.

Return a JSON object with this exact structure:
{
    "files": [
        {
            "filename": "app.py",
            "language": "python",
            "code": "# Full code here...",
            "description": "Description from instructions",
            "highlights": ["highlight 1", "highlight 2"]
        }
    ],
    "description": "Overall description",
    "concepts": ["concept1", "concept2"]
}

Ensure the JSON is valid and properly escaped."""

    def generate_code(
        self,
        question: str,
        context: str,
        session_id: str,
        page_path: str,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate code example (Call 1).

        Args:
            question: User's question
            context: Page context
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_tokens: Maximum tokens to generate

        Returns:
            Generated code
        """
        user_prompt = f"""Based on the following documentation context, generate a complete, working code example that answers this question:

{question}

Documentation Context:
{context}

Generate a complete Python file with:
- All necessary imports
- Complete working example
- Comments explaining key parts
- Dash callbacks if needed
"""

        # Ensure client is initialized
        self._ensure_client()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                system=self.build_system_prompt_generate(),
                messages=[{"role": "user", "content": user_prompt}]
            )

            # Extract text from response
            response_text = response.content[0].text

            # Log the API call with question and response
            self.logger.log_api_request(
                session_id=session_id,
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                call_type='generate_code',
                page_path=page_path,
                metadata={
                    'question': question,
                    'response': response_text
                }
            )

            return response_text

        except Exception as e:
            error_msg = f"Error generating code: {str(e)}"
            return error_msg

    def generate_format_instructions(
        self,
        code: str,
        session_id: str,
        page_path: str,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate formatting instructions (Call 2).

        Args:
            code: Generated code from Call 1
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_tokens: Maximum tokens to generate

        Returns:
            Formatting instructions as JSON string
        """
        user_prompt = f"""Analyze this code and create formatting instructions:

{code}

Return a JSON object with file structure, descriptions, and highlights."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.3,
                system=self.build_system_prompt_format_instructions(),
                messages=[{"role": "user", "content": user_prompt}]
            )

            # Log the API call
            self.logger.log_api_request(
                session_id=session_id,
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                call_type='generate_format_instructions',
                page_path=page_path
            )

            return response.content[0].text

        except Exception as e:
            return f'{{"error": "Error generating format instructions: {str(e)}"}}'

    def format_code(
        self,
        code: str,
        instructions: str,
        session_id: str,
        page_path: str,
        max_tokens: int = 4000
    ) -> Dict:
        """
        Format code with instructions (Call 3).

        Args:
            code: Generated code
            instructions: Formatting instructions
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_tokens: Maximum tokens to generate

        Returns:
            Formatted code structure as dictionary
        """
        user_prompt = f"""Format this code according to these instructions:

CODE:
{code}

INSTRUCTIONS:
{instructions}

Return a properly formatted JSON object."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.1,
                system=self.build_system_prompt_format(),
                messages=[{"role": "user", "content": user_prompt}]
            )

            # Log the API call
            self.logger.log_api_request(
                session_id=session_id,
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                call_type='format_code',
                page_path=page_path
            )

            # Extract and parse JSON
            text = response.content[0].text
            return self._extract_json(text)

        except Exception as e:
            return {
                "error": str(e),
                "files": [],
                "description": "Error formatting code"
            }

    def _extract_json(self, text: str) -> Dict:
        """
        Extract JSON from response text with multiple fallback patterns.

        Args:
            text: Response text that may contain JSON

        Returns:
            Parsed JSON dictionary
        """
        # Try direct parse first
        try:
            return json.loads(text)
        except:
            pass

        # Try to find JSON in code blocks
        patterns = [
            r'```json\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'\{.*\}',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1) if '```' in pattern else match.group(0))
                except:
                    continue

        # Fallback: return error structure
        return {
            "error": "Could not parse JSON from response",
            "raw": text[:500],
            "files": [],
            "description": "Error parsing response"
        }

    def generate_full_response(
        self,
        question: str,
        context: str,
        session_id: str,
        page_path: str
    ) -> Generator[str, None, None]:
        """
        Generate complete code response using three-call architecture.

        Args:
            question: User's question
            context: Page context
            session_id: Session ID for cost tracking
            page_path: Current page path

        Yields:
            JSON-encoded progress updates for SSE
        """
        try:
            # Call 1: Generate code
            yield json.dumps({
                'type': 'progress',
                'step': 'generate',
                'message': 'Generating code example...'
            }) + '\n'

            code = self.generate_code(question, context, session_id, page_path)

            yield json.dumps({
                'type': 'progress',
                'step': 'generate_complete',
                'preview': code[:200] + '...'
            }) + '\n'

            # Call 2: Generate format instructions
            yield json.dumps({
                'type': 'progress',
                'step': 'format_instructions',
                'message': 'Analyzing code structure...'
            }) + '\n'

            instructions = self.generate_format_instructions(code, session_id, page_path)

            # Call 3: Format code
            yield json.dumps({
                'type': 'progress',
                'step': 'format',
                'message': 'Formatting code for display...'
            }) + '\n'

            formatted = self.format_code(code, instructions, session_id, page_path)

            # Send complete response
            yield json.dumps({
                'type': 'complete',
                'formatted': formatted,
                'response_type': 'code'
            }) + '\n'

            # Send done signal
            yield json.dumps({'type': 'done'}) + '\n'

        except Exception as e:
            yield json.dumps({
                'type': 'error',
                'message': str(e)
            }) + '\n'