"""
Context Gatherer for Page-Specific AI Chat

Collects and aggregates context about the current page including:
- Page content from markdown
- Table of contents structure
- Architecture documentation
- Related pages from sitemap
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import dash


class ContextGatherer:
    """Gathers contextual information for AI chat on documentation pages."""

    def __init__(self, base_url: str = ""):
        """
        Initialize the context gatherer.

        Args:
            base_url: Base URL of the application (e.g., "https://example.com")
        """
        self.base_url = base_url

    def get_page_content(self, page_path: str, name_content_map: Dict[str, str]) -> Optional[str]:
        """
        Get the markdown content for a specific page.

        Args:
            page_path: The page path (e.g., "/pip/dash_gauge")
            name_content_map: Dictionary mapping page names to markdown content

        Returns:
            The markdown content or None if not found
        """
        # Find the page in the registry
        for page in dash.page_registry.values():
            if page.get("path") == page_path:
                page_name = page.get("name")
                if page_name in name_content_map:
                    return name_content_map[page_name]
        return None

    def get_toc_structure(self, markdown_content: str) -> List[Dict[str, str]]:
        """
        Extract table of contents from markdown headers.

        Args:
            markdown_content: The markdown content to parse

        Returns:
            List of dictionaries with 'level', 'text', and 'hash' keys
        """
        toc = []

        # Pattern to match markdown headers (# Header, ## Header, etc.)
        header_pattern = r'^(#{1,6})\s+(.+?)$'

        for line in markdown_content.split('\n'):
            match = re.match(header_pattern, line.strip())
            if match:
                level = len(match.group(1))  # Number of # symbols
                text = match.group(2).strip()

                # Generate hash (lowercase, replace spaces with hyphens, remove special chars)
                hash_text = text.lower()
                hash_text = re.sub(r'[^\w\s-]', '', hash_text)
                hash_text = re.sub(r'\s+', '-', hash_text)

                toc.append({
                    'level': level,
                    'text': text,
                    'hash': f'#{hash_text}'
                })

        return toc

    def get_architecture(self) -> Optional[str]:
        """
        Read the architecture.txt file.

        Returns:
            Architecture documentation content or None if not found
        """
        try:
            # Try to read from the application's route
            arch_path = Path('templates') / 'architecture.txt'
            if arch_path.exists():
                return arch_path.read_text()

            # Fallback: try to generate from dash page registry
            return self._generate_architecture_from_registry()
        except Exception as e:
            print(f"Error reading architecture: {e}")
            return None

    def _generate_architecture_from_registry(self) -> str:
        """
        Generate architecture documentation from Dash page registry.

        Returns:
            Generated architecture text
        """
        arch = "# Application Architecture\n\n"
        arch += "## Pages\n\n"

        for page_path, page_info in dash.page_registry.items():
            arch += f"- **{page_info.get('name', 'Unnamed')}**\n"
            arch += f"  - Path: {page_info.get('path', 'N/A')}\n"
            if page_info.get('description'):
                arch += f"  - Description: {page_info.get('description')}\n"
            arch += "\n"

        return arch

    def get_related_pages(self, current_page_path: str) -> List[Dict[str, str]]:
        """
        Get related pages from the sitemap.

        Args:
            current_page_path: Current page path to find related pages

        Returns:
            List of related page dictionaries with 'path', 'name', and 'description'
        """
        related = []

        try:
            # Get all pages from registry
            for page_path, page_info in dash.page_registry.items():
                page_route = page_info.get('path', '')

                # Skip the current page
                if page_route == current_page_path:
                    continue

                # Find related pages (same top-level category)
                current_parts = current_page_path.strip('/').split('/')
                page_parts = page_route.strip('/').split('/')

                # If they share the same first path segment, they're related
                if len(current_parts) > 0 and len(page_parts) > 0:
                    if current_parts[0] == page_parts[0]:
                        related.append({
                            'path': page_route,
                            'name': page_info.get('name', 'Unnamed'),
                            'description': page_info.get('description', '')
                        })

            return related
        except Exception as e:
            print(f"Error getting related pages: {e}")
            return []

    def get_sitemap_xml(self) -> Optional[str]:
        """
        Read the sitemap.xml file.

        Returns:
            Sitemap XML content or None if not found
        """
        try:
            sitemap_path = Path('sitemap.xml')
            if sitemap_path.exists():
                return sitemap_path.read_text()
            return None
        except Exception as e:
            print(f"Error reading sitemap: {e}")
            return None

    def get_robots_txt(self) -> Optional[str]:
        """
        Read the robots.txt file.

        Returns:
            Robots.txt content or None if not found
        """
        try:
            robots_path = Path('robots.txt')
            if robots_path.exists():
                return robots_path.read_text()
            return None
        except Exception as e:
            print(f"Error reading robots.txt: {e}")
            return None

    def gather_full_context(
        self,
        page_path: str,
        name_content_map: Dict[str, str],
        include_architecture: bool = True,
        include_related: bool = True,
        include_sitemap: bool = False,
        include_robots: bool = False
    ) -> Dict[str, any]:
        """
        Gather all available context for a page.

        Args:
            page_path: The page path
            name_content_map: Dictionary mapping page names to markdown content
            include_architecture: Whether to include architecture.txt
            include_related: Whether to include related pages
            include_sitemap: Whether to include sitemap.xml
            include_robots: Whether to include robots.txt

        Returns:
            Dictionary with all gathered context
        """
        context = {
            'page_path': page_path,
            'content': self.get_page_content(page_path, name_content_map),
            'toc': [],
            'architecture': None,
            'related_pages': [],
            'sitemap': None,
            'robots': None
        }

        # Get TOC if we have content
        if context['content']:
            context['toc'] = self.get_toc_structure(context['content'])

        # Get optional context items
        if include_architecture:
            context['architecture'] = self.get_architecture()

        if include_related:
            context['related_pages'] = self.get_related_pages(page_path)

        if include_sitemap:
            context['sitemap'] = self.get_sitemap_xml()

        if include_robots:
            context['robots'] = self.get_robots_txt()

        return context

    def format_context_for_prompt(self, context: Dict[str, any]) -> str:
        """
        Format gathered context into a string suitable for AI prompts.

        Args:
            context: Context dictionary from gather_full_context()

        Returns:
            Formatted context string
        """
        prompt_parts = []

        # Page identification
        prompt_parts.append(f"# Current Page: {context['page_path']}\n")

        # Table of contents
        if context['toc']:
            prompt_parts.append("## Table of Contents\n")
            for item in context['toc']:
                indent = "  " * (item['level'] - 1)
                prompt_parts.append(f"{indent}- {item['text']} ({item['hash']})\n")
            prompt_parts.append("\n")

        # Page content
        if context['content']:
            prompt_parts.append("## Page Content\n")
            prompt_parts.append(context['content'])
            prompt_parts.append("\n\n")

        # Related pages
        if context['related_pages']:
            prompt_parts.append("## Related Pages\n")
            for page in context['related_pages']:
                prompt_parts.append(f"- {page['name']} ({page['path']})")
                if page.get('description'):
                    prompt_parts.append(f": {page['description']}")
                prompt_parts.append("\n")
            prompt_parts.append("\n")

        # Architecture
        if context['architecture']:
            prompt_parts.append("## Architecture\n")
            prompt_parts.append(context['architecture'])
            prompt_parts.append("\n\n")

        return "".join(prompt_parts)