"""
Page-specific AI Chat System

This package provides AI-powered chat functionality for documentation pages,
including context gathering, response generation, and section suggestions.
"""

from .handler import PageChatHandler
from .context_gatherer import ContextGatherer
from .markdown_responder import MarkdownResponder
from .code_responder import CodeResponder
from .section_suggester import SectionSuggester

__all__ = [
    'PageChatHandler',
    'ContextGatherer',
    'MarkdownResponder',
    'CodeResponder',
    'SectionSuggester',
]