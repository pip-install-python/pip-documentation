"""
Markdown Responder for AI Chat

Handles generation of markdown-formatted responses with streaming
and cost tracking.
"""

import os
import json
from typing import Dict, Optional, Generator
from anthropic import Anthropic
from .api_cost_logger import get_logger


class MarkdownResponder:
    """Generates markdown responses for documentation questions."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the markdown responder.

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
        """
        Build the system prompt for markdown generation.

        Returns:
            System prompt string
        """
        return """You are a helpful documentation assistant for a Dash application framework.

Your role is to:
1. Answer questions about the documentation clearly and concisely
2. Provide code examples when relevant
3. Reference specific sections of the documentation using URL hashes (e.g., #installation)
4. Format responses in clean markdown
5. Be accurate and cite specific parts of the documentation

Guidelines:
- Use markdown formatting (headers, lists, code blocks, etc.)
- Keep responses focused and relevant to the question
- When mentioning documentation sections, use the format: "See [Section Name](#hash)"
- Provide working code examples in proper code blocks
- If you're uncertain, say so rather than guessing
"""

    def generate_markdown_response(
        self,
        question: str,
        context: str,
        session_id: str,
        page_path: str,
        max_tokens: int = 4000
    ) -> Generator[str, None, None]:
        """
        Generate a markdown response with streaming.

        Args:
            question: User's question
            context: Page context from ContextGatherer
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_tokens: Maximum tokens to generate

        Yields:
            Response chunks as they're generated
        """
        # Build the prompt
        user_prompt = f"""Based on the following documentation context, please answer this question:

{question}

Documentation Context:
{context}

Please provide a well-formatted markdown response that directly answers the question.
When referencing sections, use the hash format like #section-name so users can jump to them.
"""

        # Ensure client is initialized
        self._ensure_client()

        # Track tokens for this call
        input_tokens = 0
        output_tokens = 0
        accumulated_response = ""

        try:
            # Stream the response
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                system=self.build_system_prompt(),
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            ) as stream:
                # Yield chunks as they arrive
                for text in stream.text_stream:
                    accumulated_response += text
                    yield text

                # Get final message for token counts
                final_message = stream.get_final_message()
                input_tokens = final_message.usage.input_tokens
                output_tokens = final_message.usage.output_tokens

        except Exception as e:
            error_msg = f"\n\n**Error generating response:** {str(e)}"
            accumulated_response += error_msg
            yield error_msg

        finally:
            # Log the API call cost with full question and response
            if input_tokens > 0 or output_tokens > 0:
                self.logger.log_api_request(
                    session_id=session_id,
                    model=self.model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    call_type='generate_markdown',
                    page_path=page_path,
                    metadata={
                        'question': question,
                        'response': accumulated_response
                    }
                )

    def format_for_display(self, markdown_text: str) -> Dict[str, any]:
        """
        Format markdown text for display in dcc.Markdown.

        Args:
            markdown_text: Raw markdown text

        Returns:
            Dictionary with formatted content and metadata
        """
        return {
            'type': 'markdown',
            'content': markdown_text,
            'className': 'chat-markdown-response'
        }

    def stream_with_logging(
        self,
        question: str,
        context: str,
        session_id: str,
        page_path: str,
        max_tokens: int = 4000
    ) -> Generator[str, None, None]:
        """
        Stream markdown response with cost logging.

        This is the main entry point for generating responses.

        Args:
            question: User's question
            context: Page context
            session_id: Session ID for cost tracking
            page_path: Current page path
            max_tokens: Maximum tokens to generate

        Yields:
            JSON-encoded chunks for SSE
        """
        accumulated_text = ""

        try:
            # Generate the response
            for chunk in self.generate_markdown_response(
                question=question,
                context=context,
                session_id=session_id,
                page_path=page_path,
                max_tokens=max_tokens
            ):
                accumulated_text += chunk

                # Yield as JSON for SSE
                yield json.dumps({
                    'type': 'chunk',
                    'content': chunk
                }) + '\n'

            # Send final formatted response
            formatted = self.format_for_display(accumulated_text)
            yield json.dumps({
                'type': 'complete',
                'formatted': formatted,
                'raw': accumulated_text
            }) + '\n'

            # Send done signal
            yield json.dumps({'type': 'done'}) + '\n'

        except Exception as e:
            yield json.dumps({
                'type': 'error',
                'message': str(e)
            }) + '\n'