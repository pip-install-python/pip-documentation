"""
Page Chat Handler - Main Orchestrator

Coordinates all page chat components to provide a unified
AI chat experience for documentation pages.
"""

import json
import uuid
from typing import Dict, Optional, Generator
from .context_gatherer import ContextGatherer
from .markdown_responder import MarkdownResponder
from .code_responder import CodeResponder
from .section_suggester import SectionSuggester
from .api_cost_logger import get_logger


class PageChatHandler:
    """Main orchestrator for page-specific AI chat functionality."""

    def __init__(
        self,
        name_content_map: Dict[str, str],
        base_url: str = "",
        api_key: Optional[str] = None
    ):
        """
        Initialize the page chat handler.

        Args:
            name_content_map: Dictionary mapping page names to markdown content
            base_url: Base URL of the application
            api_key: Anthropic API key (optional, defaults to env var)
        """
        self.name_content_map = name_content_map
        self.base_url = base_url

        # Initialize components
        self.context_gatherer = ContextGatherer(base_url=base_url)
        self.markdown_responder = MarkdownResponder(api_key=api_key)
        self.code_responder = CodeResponder(api_key=api_key)
        self.section_suggester = SectionSuggester(api_key=api_key)
        self.logger = get_logger()

    def create_session(self) -> str:
        """
        Create a new chat session.

        Returns:
            Session ID (UUID)
        """
        return str(uuid.uuid4())

    def stream_response(
        self,
        page_path: str,
        question: str,
        response_format: str = "markdown",
        session_id: Optional[str] = None
    ) -> Generator[str, None, None]:
        """
        Stream a response with SSE format.

        This is the main entry point for chat interactions.

        Args:
            page_path: Current page path (e.g., "/pip/dash_gauge")
            question: User's question
            response_format: Format of response ("markdown" or "code")
            session_id: Session ID for cost tracking (creates new if None)

        Yields:
            JSON-encoded SSE chunks
        """
        # Create session if not provided
        if not session_id:
            session_id = self.create_session()

        try:
            # Step 1: Gather context
            yield json.dumps({
                'type': 'progress',
                'step': 'gathering_context',
                'message': 'Gathering page context...'
            }) + '\n'

            context = self.context_gatherer.gather_full_context(
                page_path=page_path,
                name_content_map=self.name_content_map,
                include_architecture=True,
                include_related=True
            )

            if not context['content']:
                yield json.dumps({
                    'type': 'error',
                    'message': f'Could not find content for page: {page_path}'
                }) + '\n'
                return

            # Format context for prompt
            context_str = self.context_gatherer.format_context_for_prompt(context)

            # Step 2: Generate response based on format
            yield json.dumps({
                'type': 'progress',
                'step': 'generating_response',
                'message': f'Generating {response_format} response...'
            }) + '\n'

            accumulated_response = ""

            if response_format == "code":
                # Use CodeResponder with three-call architecture
                for chunk_str in self.code_responder.generate_full_response(
                    question=question,
                    context=context_str,
                    session_id=session_id,
                    page_path=page_path
                ):
                    yield chunk_str

                    # Try to extract response for section suggestions
                    try:
                        chunk_data = json.loads(chunk_str.strip())
                        if chunk_data.get('type') == 'complete':
                            # For code responses, use the description
                            formatted = chunk_data.get('formatted', {})
                            accumulated_response = formatted.get('description', '')
                    except:
                        pass

            else:  # markdown format
                # Use MarkdownResponder with streaming
                response_chunks = []
                for chunk_str in self.markdown_responder.stream_with_logging(
                    question=question,
                    context=context_str,
                    session_id=session_id,
                    page_path=page_path
                ):
                    yield chunk_str

                    # Accumulate response for section suggestions
                    try:
                        chunk_data = json.loads(chunk_str.strip())
                        if chunk_data.get('type') == 'chunk':
                            response_chunks.append(chunk_data.get('content', ''))
                        elif chunk_data.get('type') == 'complete':
                            accumulated_response = chunk_data.get('raw', '')
                    except:
                        pass

                # If we didn't get accumulated response, join chunks
                if not accumulated_response and response_chunks:
                    accumulated_response = ''.join(response_chunks)

            # Step 3: Suggest relevant sections
            if context['toc'] and accumulated_response:
                yield json.dumps({
                    'type': 'progress',
                    'step': 'suggesting_sections',
                    'message': 'Finding relevant sections...'
                }) + '\n'

                try:
                    suggestions = self.section_suggester.suggest_sections(
                        question=question,
                        ai_response=accumulated_response,
                        toc=context['toc'],
                        session_id=session_id,
                        page_path=page_path,
                        max_suggestions=3
                    )

                    if suggestions:
                        yield json.dumps({
                            'type': 'sections',
                            'suggestions': suggestions
                        }) + '\n'
                except Exception as e:
                    print(f"Error suggesting sections: {e}")
                    # Continue without section suggestions

            # Step 4: Send session cost summary
            session_costs = self.logger.get_session_costs(session_id)
            if session_costs:
                yield json.dumps({
                    'type': 'cost_summary',
                    'session_id': session_id,
                    'total_cost': session_costs.get('total_cost', 0),
                    'total_tokens': session_costs.get('total_tokens', 0),
                    'num_calls': len(session_costs.get('calls', []))
                }) + '\n'

            # Final done signal (if not already sent by responder)
            yield json.dumps({'type': 'done'}) + '\n'

        except Exception as e:
            yield json.dumps({
                'type': 'error',
                'message': f'Error processing request: {str(e)}'
            }) + '\n'

    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """
        Get cost summary for a session.

        Args:
            session_id: Session ID

        Returns:
            Session cost summary or None
        """
        return self.logger.get_session_costs(session_id)

    def get_total_costs(self) -> Dict[str, float]:
        """
        Get total costs across all sessions.

        Returns:
            Dictionary with total costs
        """
        return self.logger.get_total_costs()