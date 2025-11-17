import logging
from pathlib import Path
from typing import Optional

import dash
import dash_mantine_components as dmc
import dash_dock
from dash import html, dcc
import frontmatter
from markdown2dash import Admonition, BlockExec, Divider, Image, create_parser
from pydantic import BaseModel
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
from dash_iconify import DashIconify

from lib.constants import PAGE_TITLE_PREFIX, NAME_CONTENT_MAP
from lib.directives.kwargs import Kwargs
from lib.directives.llms_copy import LlmsCopy
from lib.directives.source import SC, SourceTabs
from lib.directives.toc import TOC
from lib.advertising import create_ad_component

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

directory = "docs"

# read all markdown files
files = Path(directory).glob("**/*.md")


class Meta(BaseModel):
    name: str
    description: str
    endpoint: str
    package: str = "dash_pydantic_form"
    category: Optional[str] = None
    icon: Optional[str] = None


def make_endpoint(name):
    return "-".join(name.lower().split())


def create_chat_panel(page_name, page_path, viewport="desktop", include_stores=True):
    """Helper function to create a chat panel with all required components.

    Args:
        page_name: The page identifier for IDs (e.g., "gauge")
        page_path: The full page path (e.g., "/pip/dash_gauge")
        viewport: "mobile" or "desktop" to create unique IDs
        include_stores: Whether to include the shared stores (only include once)
    """
    stores = []
    if include_stores:
        stores = [
            # Shared store for page path (used by callbacks)
            dcc.Store(
                id={"type": "page-path-store", "page": page_name},
                data=page_path  # Use the full path!
            ),
        ]

    # Always include viewport-specific stores
    stores.extend([
        # Store to trigger SSE
        dcc.Store(
            id={"type": "chat-sse-trigger", "page": page_name, "viewport": viewport},
        ),
    ])

    return html.Div(
        className="chat-tab-container",
        style={"height": "100%", "display": "flex", "flexDirection": "column"},
        children=stores + [
            PanelGroup(
                id=f"chat-panel-group-{page_name}-{viewport}",
                children=[
                    Panel(
                        id=f"chat-messages-panel-{page_name}-{viewport}",
                        children=[
                            dmc.ScrollArea(
                                id=f"chat-area-{page_name}-{viewport}",
                                h="100%",
                                children=dmc.Stack(
                                    id={"type": "chat-messages", "page": page_name, "viewport": viewport},
                                    gap="md",
                                    p="md",
                                    children=[
                                        dmc.Paper(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(
                                                            icon="tabler:info-circle",
                                                            width=20,
                                                            color="var(--mantine-color-blue-6)"
                                                        ),
                                                        dmc.Text(
                                                            "Ask questions about this documentation page",
                                                            size="sm",
                                                            fw=500,
                                                        ),
                                                    ],
                                                    gap="xs",
                                                ),
                                                dmc.Text(
                                                    "Your conversation history will appear here. Use the input below to start chatting.",
                                                    size="xs",
                                                    c="dimmed",
                                                    mt="xs",
                                                ),
                                            ],
                                            p="md",
                                            withBorder=True,
                                            radius="md",
                                            className="elevation-1 info-message",
                                        )
                                    ]
                                ),
                                className="chat-messages-container elevation-inset",
                            ),
                        ],
                        defaultSizePercentage=65,
                        minSizePercentage=20,
                    ),
                    PanelResizeHandle(
                        html.Div(
                            style={
                                "backgroundColor": "var(--mantine-color-gray-4)",
                                "height": "6px",
                                "width": "100%",
                                "cursor": "row-resize",
                                "transition": "background-color 0.2s ease",
                                "position": "relative",
                            },
                            className="resize-divider",
                        )
                    ),
                    Panel(
                        id=f"chat-input-panel-{page_name}",
                        children=[
                            dmc.Stack(
                                [
                                    dmc.Card(
                                        [
                                            dmc.Stack(
                                                [
                                                    # Page context indicator
                                                    dmc.Group(
                                                        [
                                                            DashIconify(
                                                                icon="tabler:book",
                                                                width=16,
                                                            ),
                                                            dmc.Text(
                                                                f"Context: {page_name}",
                                                                size="sm",
                                                                fw=500,
                                                            ),
                                                        ],
                                                        gap="xs",
                                                    ),
                                                    dmc.Textarea(
                                                        id={"type": "chat-input", "page": page_name, "viewport": viewport},
                                                        placeholder="Ask a question about this documentation page...",
                                                        minRows=3,
                                                        autosize=True,
                                                        maxRows=8,
                                                    ),
                                                    dmc.Group(
                                                        [
                                                            dmc.Button(
                                                                "Clear Chat",
                                                                leftSection=DashIconify(
                                                                    icon="tabler:trash"
                                                                ),
                                                                variant="light",
                                                                color="gray",
                                                                size="sm",
                                                                id={"type": "chat-clear-btn", "page": page_name, "viewport": viewport},
                                                            ),
                                                            dmc.Button(
                                                                "Send Message",
                                                                id={"type": "chat-send-btn", "page": page_name, "viewport": viewport},
                                                                leftSection=DashIconify(
                                                                    icon="tabler:send"
                                                                ),
                                                                loading=False,
                                                                loaderProps={
                                                                    "type": "dots"
                                                                },
                                                                gradient={
                                                                    "from": "teal",
                                                                    "to": "cyan",
                                                                },
                                                                variant="gradient",
                                                                size="md",
                                                                style={
                                                                    "marginLeft": "auto"
                                                                },
                                                                className="elevation-2",
                                                            ),
                                                        ],
                                                        justify="space-between",
                                                    ),
                                                ],
                                                gap="md",
                                            )
                                        ],
                                        withBorder=True,
                                        p="md",
                                        className="chat-input-card elevation-2",
                                    ),
                                ],
                                gap="sm",
                                p="sm",
                            )
                        ],
                        defaultSizePercentage=35,
                        minSizePercentage=20,
                    ),
                ],
                direction="vertical",
                style={"height": "100%", "flex": 1},
            )
        ],
    )


def create_dock_layout(content_components, toc_component, page_name, page_path):
    """
    Wraps the markdown content in a dash-dock layout with:
    - Mobile (< 768px): Single tabset with all three tabs
    - Tablet/Desktop (>= 768px): Split layout (70/30)
      - Left side (70%): Documentation content
      - Right side (30%): Two tabs (Table of Contents and Chat)

    Args:
        content_components: List of content components
        toc_component: Table of contents component
        page_name: Short page identifier for IDs (e.g., "gauge")
        page_path: Full page path (e.g., "/pip/dash_gauge")
    """
    print(f"[Dock Layout] Creating layout for page_name='{page_name}', page_path='{page_path}'")

    # Mobile configuration: Single tabset with all tabs
    mobile_dock_config = {
        "global": {
            "tabEnableClose": False,
            "tabEnableFloat": False
        },
        "layout": {
            "type": "row",
            "children": [
                {
                    "type": "tabset",
                    "weight": 100,
                    "children": [
                        {
                            "type": "tab",
                            "name": "Documentation",
                            "component": "markdown-content",
                            "id": f"markdown-content-mobile-{page_name}",
                            "enableClose": False
                        },
                        {
                            "type": "tab",
                            "name": "Table of Contents",
                            "component": "toc",
                            "id": f"toc-mobile-{page_name}",
                            "enableClose": False
                        },
                        {
                            "type": "tab",
                            "name": "AI Chat",
                            "component": "chat",
                            "id": f"chat-mobile-{page_name}",
                            "enableClose": False
                        }
                    ]
                }
            ]
        }
    }

    # Desktop/Tablet configuration: Split layout (70/30)
    desktop_dock_config = {
        "global": {
            "tabEnableClose": False,
            "tabEnableFloat": True
        },
        "layout": {
            "type": "row",
            "children": [
                {
                    "type": "tabset",
                    "weight": 70,
                    "children": [
                        {
                            "type": "tab",
                            "name": "Documentation",
                            "component": "markdown-content",
                            "id": f"markdown-content-desktop-{page_name}",
                            "enableClose": False
                        }
                    ]
                },
                {
                    "type": "tabset",
                    "weight": 30,
                    "children": [
                        {
                            "type": "tab",
                            "name": "Table of Contents",
                            "component": "toc",
                            "id": f"toc-desktop-{page_name}",
                            "enableClose": False
                        },
                        {
                            "type": "tab",
                            "name": "AI Chat",
                            "component": "chat",
                            "id": f"chat-desktop-{page_name}",
                            "enableClose": False
                        }
                    ]
                }
            ]
        }
    }

    # Extract TOC content if it exists
    if toc_component and hasattr(toc_component, 'children'):
        # The TOC component is an AppShellAside with a ScrollArea child
        toc_content = toc_component.children
    else:
        toc_content = dmc.Text("No table of contents available", c="dimmed", size="sm")

    # Create advertisement component
    mobile_ad = create_ad_component(page_name, viewport="mobile")
    desktop_ad = create_ad_component(page_name, viewport="desktop")

    # Create tab components WITH children
    # Each tab gets its own instance of the content (can't reuse component instances)
    mobile_tab_components = [
        dash_dock.Tab(
            id=f"markdown-content-mobile-{page_name}",
            children=dmc.Box(
                children=content_components,
                p="md",
                style={"height": "100%", "overflow": "auto"}
            )
        ),
        dash_dock.Tab(
            id=f"toc-mobile-{page_name}",
            children=dmc.Box(
                children=[
                    # TOC content
                    toc_content,
                    # Advertisement below TOC
                    mobile_ad
                ],
                p="md",
                style={"height": "100%", "overflow": "auto"}
            )
        ),
        dash_dock.Tab(
            id=f"chat-mobile-{page_name}",
            children=create_chat_panel(page_name, page_path, viewport="mobile", include_stores=False)
        )
    ]

    desktop_tab_components = [
        dash_dock.Tab(
            id=f"markdown-content-desktop-{page_name}",
            children=dmc.Box(
                children=content_components,
                p="md",
                style={"height": "100%", "overflow": "auto"}
            )
        ),
        dash_dock.Tab(
            id=f"toc-desktop-{page_name}",
            children=dmc.Box(
                children=[
                    # TOC content
                    toc_content,
                    # Advertisement below TOC
                    desktop_ad
                ],
                p="md",
                style={"height": "100%", "overflow": "auto"}
            )
        ),
        dash_dock.Tab(
            id=f"chat-desktop-{page_name}",
            children=create_chat_panel(page_name, page_path, viewport="desktop", include_stores=True)
        )
    ]

    # Create mobile dock layout (visible only on screens < 768px)
    mobile_dock = dmc.Box(
        dash_dock.DashDock(
            id=f'dock-layout-mobile-{page_name}',
            model=mobile_dock_config,
            children=mobile_tab_components,
            useStateForModel=True,
            style={
                'position': 'relative',
                'height': '100%',
                'width': '100%',
                'overflow': 'hidden'
            }
        ),
        hiddenFrom="sm",  # Hide on screens >= 768px (sm breakpoint)
        style={
            'height': 'calc(100vh - 200px)',
            'width': '100%',
            'position': 'relative',
            'overflow': 'hidden'
        }
    )

    # Create desktop/tablet dock layout (visible only on screens >= 768px)
    desktop_dock = dmc.Box(
        dash_dock.DashDock(
            id=f'dock-layout-desktop-{page_name}',
            model=desktop_dock_config,
            children=desktop_tab_components,
            useStateForModel=True,
            style={
                'position': 'relative',
                'height': '100%',
                'width': '100%',
                'overflow': 'hidden'
            }
        ),
        visibleFrom="sm",  # Show on screens >= 768px (sm breakpoint)
        style={
            'height': 'calc(100vh - 200px)',
            'width': '100%',
            'position': 'relative',
            'overflow': 'hidden'
        }
    )

    # Return both dock layouts (mobile and desktop)
    # Content is now directly in Tab children, so callbacks can find it
    return dmc.Box([mobile_dock, desktop_dock])


directives = [Admonition(), BlockExec(), Divider(), Image(), Kwargs(), LlmsCopy(), SC(), SourceTabs(), TOC()]
parse = create_parser(directives)

for file in files:
    logger.info("Loading %s..", file)
    metadata, content = frontmatter.parse(file.read_text())
    metadata = Meta(**metadata)
    logger.info("Type of content: %s", type(content))

    # Store raw markdown content in NAME_CONTENT_MAP for LLM copy button
    NAME_CONTENT_MAP[metadata.name] = content

    layout = parse(content)

    # add heading and description to the layout
    section = [
        dmc.Title(metadata.name, order=2, className="m2d-heading"),
        dmc.Text(metadata.description, className="m2d-paragraph"),
    ]
    markdown_content = section + layout

    # Extract TOC component from layout (TOC renders as AppShellAside)
    toc_component = None
    filtered_content = []
    for component in markdown_content:
        if isinstance(component, dmc.AppShellAside):
            toc_component = component
        else:
            filtered_content.append(component)

    # Wrap the content in a dock layout
    final_layout = create_dock_layout(filtered_content, toc_component, make_endpoint(metadata.name), metadata.endpoint)

    # register with dash
    dash.register_page(
        metadata.name,
        metadata.endpoint,
        name=metadata.name,
        title=PAGE_TITLE_PREFIX + metadata.name,
        description=metadata.description,
        layout=final_layout,
        category=metadata.category,
        icon=metadata.icon,
    )