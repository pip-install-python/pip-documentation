import dash
from dash import Dash, _dash_renderer
import json
from flask import jsonify, request, Response, abort
from components.appshell import create_appshell
import dash_mantine_components as dmc

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# AI/LLM Integration & SEO
from dash_improve_my_llms import add_llms_routes, RobotsConfig, register_page_metadata

# Analytics tracking
from lib.analytics_tracker import tracker

# Import markdown content map for custom llms.txt routes
from lib.constants import NAME_CONTENT_MAP

import re
from pathlib import Path
from typing import List

scripts = [
    "https://unpkg.com/hotkeys-js/dist/hotkeys.min.js",
]

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    external_scripts=scripts,
    update_title=None,
    prevent_initial_callbacks=True,
    index_string=open('templates/index.html').read(),
    health_endpoint="health"  # Dash 3.3.0: Production health check endpoint
)

# ============================================================================
# AI/LLM & SEO Configuration
# ============================================================================

# Set base URL for SEO (production URL)
app._base_url = "https://pip-install-python.com"

# Configure bot management policies
app._robots_config = RobotsConfig(
    block_ai_training=False,      # Block GPTBot, CCBot, anthropic-ai, etc.
    allow_ai_search=True,         # Allow ChatGPT-User, ClaudeBot, PerplexityBot
    allow_traditional=True,       # Allow Googlebot, Bingbot, etc.
    crawl_delay=10,               # 10 second delay between bot requests
    disallowed_paths=[],          # Add paths to block (e.g., ["/admin", "/api/*"])
)

# ============================================================================
# Helper Functions for Processing Source Directives
# ============================================================================

def process_source_directives(markdown_content: str) -> str:
    """
    Process .. source:: directives and replace with actual file content.

    Args:
        markdown_content: Raw markdown with directives

    Returns:
        Processed markdown with file contents embedded
    """
    # Pattern to match .. source::file_path on its own line
    pattern = r'^\.\. source::(.+?)$'

    # Language mapping for syntax highlighting
    lang_map = {
        'py': 'python', 'pyi': 'python',
        'js': 'javascript', 'jsx': 'jsx',
        'ts': 'typescript', 'tsx': 'tsx',
        'css': 'css', 'scss': 'scss', 'sass': 'sass', 'less': 'less',
        'html': 'html', 'htm': 'html', 'xml': 'xml',
        'json': 'json',
        'yaml': 'yaml', 'yml': 'yaml',
        'md': 'markdown', 'rst': 'rst', 'txt': 'text',
        'sh': 'bash', 'bash': 'bash',
        'sql': 'sql', 'r': 'r',
        'toml': 'toml', 'ini': 'ini', 'conf': 'conf',
    }

    def replace_source(match):
        file_path = match.group(1).strip()

        try:
            # Read the file content
            full_path = Path(file_path)
            content = full_path.read_text()

            # Detect language from extension
            ext = full_path.suffix.lstrip('.').lower()
            language = lang_map.get(ext, ext if ext else 'text')

            # Format as code block with file path annotation
            result = f'\n```{language}\n'
            result += f'# File: {file_path}\n\n'
            result += content
            if not content.endswith('\n'):
                result += '\n'
            result += '```\n'

            return result

        except FileNotFoundError:
            return f'\n<!-- Error: File not found: {file_path} -->\n'
        except Exception as e:
            return f'\n<!-- Error reading {file_path}: {str(e)} -->\n'

    # Replace all source directives
    processed = re.sub(pattern, replace_source, markdown_content, flags=re.MULTILINE)
    return processed


def extract_source_files(markdown_content: str) -> List[str]:
    """
    Extract all source file paths referenced in markdown.

    Args:
        markdown_content: Raw markdown with directives

    Returns:
        List of file paths found in source directives
    """
    pattern = r'^\.\. source::(.+?)$'
    matches = re.findall(pattern, markdown_content, re.MULTILINE)
    return [m.strip() for m in matches]


def process_sourcetabs_directives(markdown_content: str) -> str:
    """
    Process .. sourcetabs:: directives and replace with actual file content.

    Args:
        markdown_content: Raw markdown with sourcetabs directives

    Returns:
        Processed markdown with file contents embedded
    """
    # Pattern to match .. sourcetabs::file_path
    # Handles multi-line directives with options like :defaultExpanded: and :withExpandedButton:
    pattern = r'^\.\. sourcetabs::(.+?)(?:\n\s+:.+?:.+?)*$'

    # Language mapping for syntax highlighting
    lang_map = {
        'py': 'python', 'pyi': 'python',
        'js': 'javascript', 'jsx': 'jsx',
        'ts': 'typescript', 'tsx': 'tsx',
        'css': 'css', 'scss': 'scss', 'sass': 'sass', 'less': 'less',
        'html': 'html', 'htm': 'html', 'xml': 'xml',
        'json': 'json',
        'yaml': 'yaml', 'yml': 'yaml',
        'md': 'markdown', 'rst': 'rst', 'txt': 'text',
        'sh': 'bash', 'bash': 'bash',
        'sql': 'sql', 'r': 'r',
        'toml': 'toml', 'ini': 'ini', 'conf': 'conf',
    }

    def replace_sourcetabs(match):
        file_path = match.group(1).strip()

        try:
            # Convert dots to slashes if needed (e.g., docs.dash_gauge.example → docs/dash_gauge/example.py)
            if not file_path.endswith('.py'):
                file_path = file_path.replace('.', '/') + '.py'

            # Read the file content
            full_path = Path(file_path)
            content = full_path.read_text()

            # Detect language from extension
            ext = full_path.suffix.lstrip('.').lower()
            language = lang_map.get(ext, ext if ext else 'text')

            # Format as code block with file path annotation
            result = f'\n```{language}\n'
            result += f'# File: {file_path}\n\n'
            result += content
            if not content.endswith('\n'):
                result += '\n'
            result += '```\n'

            return result

        except FileNotFoundError:
            return f'\n<!-- Error: File not found: {file_path} -->\n'
        except Exception as e:
            return f'\n<!-- Error reading {file_path}: {str(e)} -->\n'

    # Replace all sourcetabs directives (including multi-line with options)
    processed = re.sub(pattern, replace_sourcetabs, markdown_content, flags=re.MULTILINE)
    return processed


def get_source_file_metadata(markdown_content: str) -> List[dict]:
    """
    Extract metadata about each source file.

    Args:
        markdown_content: Raw markdown with directives

    Returns:
        List of dicts with file metadata
    """
    file_paths = extract_source_files(markdown_content)
    metadata = []

    for file_path in file_paths:
        try:
            full_path = Path(file_path)
            stat = full_path.stat()

            metadata.append({
                'path': file_path,
                'exists': True,
                'size_bytes': stat.st_size,
                'extension': full_path.suffix.lstrip('.'),
                'filename': full_path.name,
            })
        except FileNotFoundError:
            metadata.append({
                'path': file_path,
                'exists': False,
                'error': 'File not found'
            })
        except Exception as e:
            metadata.append({
                'path': file_path,
                'exists': False,
                'error': str(e)
            })

    return metadata

# ============================================================================
# Custom LLM Routes for Markdown Pages (MUST be registered BEFORE add_llms_routes)
# ============================================================================

@app.server.route("/<path:page_path>/llms.txt")
def serve_markdown_llms_txt(page_path):
    """
    Custom route to serve processed markdown content for documentation pages.
    Source directives are replaced with actual file content.
    """
    # Construct the full path
    full_path = "/" + page_path

    # Find the page in the registry
    for page in dash.page_registry.values():
        if page.get("path") == full_path:
            page_name = page.get("name")
            page_description = page.get("description", "")

            # Check if we have raw markdown content for this page
            if page_name in NAME_CONTENT_MAP:
                markdown_content = NAME_CONTENT_MAP[page_name]

                # Process source directives to include actual file content
                processed_content = process_source_directives(markdown_content)
                # Also process sourcetabs directives
                processed_content = process_sourcetabs_directives(processed_content)

                # Format the output as llms.txt
                output = f"# {page_name}\n\n"

                if page_description:
                    output += f"> {page_description}\n\n"

                output += "---\n\n"
                output += processed_content
                output += "\n\n---\n\n"
                output += f"*Source: {full_path}*\n"
                output += f"*Generated with dash-improve-my-llms*\n"

                return Response(output, mimetype="text/plain")

    # If no markdown content found, let default handler process it
    abort(404)

@app.server.route("/<path:page_path>/page.json")
def serve_markdown_page_json(page_path):
    """
    Custom route to serve JSON with Dash component layout structure.
    Returns a standard Dash layout JSON for LLM consumption.
    """
    from plotly.utils import PlotlyJSONEncoder

    # Construct the full path
    full_path = "/" + page_path

    # Find the page in the registry
    for page in dash.page_registry.values():
        if page.get("path") == full_path:
            page_name = page.get("name")
            page_description = page.get("description", "")
            page_layout = page.get("layout")

            # Check if we have raw markdown content for this page
            if page_name in NAME_CONTENT_MAP:
                markdown_content = NAME_CONTENT_MAP[page_name]

                # Extract source file information
                source_files = extract_source_files(markdown_content)
                source_metadata = get_source_file_metadata(markdown_content)

                # Serialize the Dash layout to JSON
                try:
                    # Convert layout to plotly JSON format
                    if hasattr(page_layout, 'to_plotly_json'):
                        layout_json = page_layout.to_plotly_json()
                    else:
                        # Fallback: use PlotlyJSONEncoder
                        layout_json = json.loads(
                            json.dumps(page_layout, cls=PlotlyJSONEncoder)
                        )
                except Exception as e:
                    # If serialization fails (e.g., DashDock components), provide metadata instead
                    layout_json = {
                        "error": f"Layout contains non-serializable components: {str(e)}",
                        "component_type": type(page_layout).__name__ if page_layout else None,
                        "note": "Full component tree not available in JSON format. Use the rendered page instead."
                    }

                # Create standard JSON response
                response_data = {
                    "page": {
                        "path": full_path,
                        "name": page_name,
                        "description": page_description,
                        "title": page.get("title"),
                    },
                    "layout": layout_json,
                    "code_examples": {
                        "source_files": source_files,
                        "files_metadata": source_metadata,
                        "total_files": len(source_files),
                        "total_size_bytes": sum(
                            m.get('size_bytes', 0) for m in source_metadata if m.get('exists')
                        )
                    },
                    "metadata": {
                        "content_type": "dash_components",
                        "format": "json",
                        "source_markdown": f"docs/{page_path}.md",
                        "has_code_examples": len(source_files) > 0,
                    }
                }

                return jsonify(response_data)

    # If no markdown content found, let default handler process it
    abort(404)

# ============================================================================
# Page Chat SSE Streaming Endpoint
# ============================================================================

from lib.page_chat import PageChatHandler

# Initialize page chat handler
page_chat_handler = PageChatHandler(
    name_content_map=NAME_CONTENT_MAP,
    base_url=app._base_url
)

@app.server.route("/api/page-chat-stream")
def page_chat_stream():
    """
    SSE endpoint for streaming AI chat responses.

    Query parameters:
        - page: Page path (e.g., "/pip/dash_gauge")
        - question: User's question
        - format: Response format ("markdown" or "code")
        - session: Session ID (optional)
    """
    from flask import request, Response

    page_path = request.args.get('page', '')
    question = request.args.get('question', '')
    response_format = request.args.get('format', 'markdown')
    session_id = request.args.get('session', None)

    if not page_path or not question:
        return jsonify({
            'error': 'Missing required parameters: page and question'
        }), 400

    def generate():
        """Generator for SSE stream."""
        try:
            for chunk in page_chat_handler.stream_response(
                page_path=page_path,
                question=question,
                response_format=response_format,
                session_id=session_id
            ):
                # SSE format: data: <json>\n\n
                yield f"data: {chunk}\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

# ============================================================================

# Add LLMS routes - enables llms.txt, page.json, architecture.txt, robots.txt, sitemap.xml
add_llms_routes(app)

# Register metadata for home page (improves SEO and AI understanding)
register_page_metadata(
    path="/",
    name="Dash Documentation Boilerplate",
    description="A modern, responsive documentation system for Dash applications built with Dash Mantine Components"
)

# ============================================================================

# Import chat callbacks to register them (chat-demo now uses unique page name to avoid conflicts)
import callbacks.chat_callbacks  # noqa: F401
import callbacks.advertising_callbacks  # noqa: F401

# ============================================================================
# Advertising Click Tracking API
# ============================================================================
# Note: The /api/track-ad-click endpoint is now defined as a callback with
# api_endpoint parameter in callbacks/advertising_callbacks.py (Dash 3.3.0)
# The app.setup_apis() call below will register it automatically.
# ============================================================================

app.layout = create_appshell(dash.page_registry.values())

server = app.server

# ============================================================================
# Analytics Tracking
# ============================================================================

@server.before_request
def track_visitor():
    """Track visitor analytics before each request."""
    try:
        path = request.path
        user_agent = request.headers.get('User-Agent', '')
        ip_address = request.remote_addr
        tracker.track_visit(path, user_agent, ip_address)
    except Exception as e:
        # Silently fail if tracking encounters an error
        pass

# ============================================================================

# Setup API endpoints (Dash 3.3.0)
# This registers all callbacks with api_endpoint parameter as Flask routes
app.setup_apis()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8502')