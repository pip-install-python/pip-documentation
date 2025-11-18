import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, dcc, page_container, State

from components.header import create_header
from components.navbar import create_navbar, create_navbar_drawer
from lib.constants import PRIMARY_COLOR
from dash_iconify import DashIconify

def create_appshell(data):
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        theme={
            # Core Color System
            "primaryColor": PRIMARY_COLOR,
            "primaryShade": {"light": 6, "dark": 8},

            # Typography System
            "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "fontFamilyMonospace": "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Courier New', monospace",
            "headings": {
                "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                "fontWeight": 600,
                "sizes": {
                    "h1": {"fontSize": "2.125rem", "lineHeight": 1.3, "fontWeight": 700},
                    "h2": {"fontSize": "1.625rem", "lineHeight": 1.35, "fontWeight": 700},
                    "h3": {"fontSize": "1.375rem", "lineHeight": 1.4, "fontWeight": 600},
                    "h4": {"fontSize": "1.125rem", "lineHeight": 1.45, "fontWeight": 600},
                    "h5": {"fontSize": "1rem", "lineHeight": 1.5, "fontWeight": 600},
                    "h6": {"fontSize": "0.875rem", "lineHeight": 1.5, "fontWeight": 600},
                }
            },
            "fontSizes": {
                "xs": "0.75rem",    # 12px
                "sm": "0.875rem",   # 14px
                "md": "1rem",       # 16px - base body text
                "lg": "1.125rem",   # 18px
                "xl": "1.25rem",    # 20px
            },
            "lineHeights": {
                "xs": 1.4,
                "sm": 1.45,
                "md": 1.55,  # For body text
                "lg": 1.6,
                "xl": 1.65,
            },

            # Spacing System (based on 4px unit)
            "spacing": {
                "xs": "0.5rem",   # 8px
                "sm": "0.75rem",  # 12px
                "md": "1rem",     # 16px
                "lg": "1.5rem",   # 24px
                "xl": "2rem",     # 32px
            },

            # Border Radius System
            "radius": {
                "xs": "0.25rem",  # 4px
                "sm": "0.375rem", # 6px
                "md": "0.5rem",   # 8px
                "lg": "0.75rem",  # 12px
                "xl": "1rem",     # 16px
            },
            "defaultRadius": "md",

            # Professional Shadow System with Depth
            # Combines inset highlights (light from top) with drop shadows for realistic depth
            # xs: Subtle depth for minimal elevation
            # sm: Standard depth for cards and containers
            # md: Medium depth for elevated panels
            # lg: High depth for floating elements like modals
            # xl: Maximum depth for overlays and popovers
            "shadows": {
                "xs": "0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1)",
                "sm": "inset 0 1px 2px rgba(255, 255, 255, 0.3), 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.3)",
                "md": "inset 0 1px 2px rgba(255, 255, 255, 0.5), 0 4px 12px rgba(0, 0, 0, 0.10), 0 2px 4px rgba(0, 0, 0, 0.3)",
                "lg": "inset 0 1px 2px rgba(255, 255, 255, 0.7), 0 8px 24px rgba(0, 0, 0, 0.12), 0 4px 6px rgba(0, 0, 0, 0.3)",
                "xl": "inset 0 1px 2px rgba(255, 255, 255, 0.7), 0 16px 48px rgba(0, 0, 0, 0.15), 0 6px 10px rgba(0, 0, 0, 0.3)",
            },

            # Color Contrast
            "black": "#1a1b1e",  # Softer black instead of pure #000000
            "white": "#ffffff",
            "autoContrast": True,
            "luminanceThreshold": 0.3,

            # Custom Colors
            "colors": {
                "myColor": [
                    "#F2FFB6",
                    "#DCF97E",
                    "#C3E35B",
                    "#AAC944",
                    "#98BC20",
                    "#86AC09",
                    "#78A000",
                    "#668B00",
                    "#547200",
                    "#455D00",
                ]
            },

            # Global Component Styling
            "components": {
                "Button": {
                    "defaultProps": {
                        "fw": 500,
                        "radius": "md",
                    }
                },
                "Card": {
                    "defaultProps": {
                        "shadow": "sm",
                        "padding": "lg",
                        "radius": "md",
                        "withBorder": True,
                    }
                },
                "Paper": {
                    "defaultProps": {
                        "shadow": "xs",
                        "padding": "md",
                        "radius": "md",
                    }
                },
                "TextInput": {
                    "defaultProps": {
                        "radius": "md",
                    }
                },
                "Select": {
                    "defaultProps": {
                        "radius": "md",
                    }
                },
                "Title": {
                    "styles": {
                        "root": {
                            "marginBottom": "0.75rem"  # sm spacing
                        }
                    }
                },
                "Text": {
                    "defaultProps": {
                        "size": "md",
                    }
                },
                "Alert": {
                    "defaultProps": {
                        "radius": "md",
                    },
                    "styles": {"title": {"fontWeight": 600}}
                },
                "Badge": {
                    "defaultProps": {
                        "radius": "md",
                    },
                    "styles": {"root": {"fontWeight": 600}}
                },
                "Table": {
                    "defaultProps": {
                        "highlightOnHover": True,
                        "withTableBorder": True,
                        "verticalSpacing": "sm",
                        "horizontalSpacing": "md",
                        "striped": True,
                    }
                },
                "Anchor": {
                    "defaultProps": {
                        "underline": "hover",
                    }
                },
            },
        },
        children=[
            dcc.Location(id="url", refresh="callback-nav"),
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            dmc.NotificationContainer(id="notification-container", position="top-right"),
            dmc.AppShell(
                [
                    create_header(data),
                    create_navbar(data),
                    create_navbar_drawer(data),
                    dmc.AppShellMain(
                        children=page_container,
                        style={"minHeight": "calc(100vh - 70px)"}  # Full height minus header
                    ),
                    # Footer
                    dmc.AppShellFooter(
                        dmc.Container(
                            dmc.Group([
                                dmc.Text("© 2025 Pip Install Python LLC", size="sm", c="dimmed", visibleFrom="sm"),
                                dmc.Group([
                                    dmc.Anchor(
                                        dmc.ActionIcon(
                                            DashIconify(icon="tabler:brand-github"),
                                            size="lg",
                                            variant="subtle",
                                            color="gray.4"
                                        ),
                                        href="https://github.com/pip-install-python",
                                        target="_blank"
                                    ),
                                    dmc.Anchor(
                                        dmc.ActionIcon(
                                            DashIconify(icon="icomoon-free:youtube2"),
                                            size="lg",
                                            variant="subtle",
                                            color="gray.4"
                                        ),
                                        href="https://www.youtube.com/@pipinstallpython/videos",
                                        target="_blank"
                                    ),
                                    dmc.Anchor(
                                        dmc.ActionIcon(
                                            DashIconify(icon="tabler:mail"),
                                            size="lg",
                                            variant="subtle",
                                            color="gray.4"
                                        ),
                                        href="mailto:pipinstallpython@gmail.com"
                                    ),
                                    dmc.Anchor("Terms", href="/terms", size="sm", visibleFrom="sm", c='light-dark(rgb(28, 126, 214), rgb(116, 192, 252))'),
                                    dmc.Anchor("Privacy Policy", href="/privacy", size="sm", visibleFrom="sm", c='light-dark(rgb(28, 126, 214), rgb(116, 192, 252))'),

                                ], gap="lg")
                            ], justify="space-between"),
                            fluid=True,
                            px="md",
                            h="100%",
                            style={"display": "flex", "alignItems": "center"}
                        ),
                        h=60,
                        withBorder=True
                    )
                ],
                header={"height": 70},
                footer={"height": 60},
                padding="xl",
                navbar={
                    "width": 280,
                    "breakpoint": "md",  # Collapse on medium screens and below
                    "collapsed": {"mobile": True},
                },
                aside={
                    "width": 280,
                    "breakpoint": "xl",
                    "collapsed": {"desktop": True, "mobile": True},
                },
                withBorder=True,
            ),
        ],
    )


# Initialize theme from browser preference on first load
clientside_callback(
    """
    function(pathname, currentTheme) {
        // If theme is already set, keep it
        if (currentTheme) {
            return currentTheme;
        }

        // Check browser preference for initial load
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }

        // Default to light theme
        return 'light';
    }
    """,
    Output("color-scheme-storage", "data"),
    Input("url", "pathname"),
    State("color-scheme-storage", "data"),
)

# Apply theme from storage to MantineProvider
clientside_callback(
    """
    function(colorScheme) {
        // Default to light if no theme is set
        return colorScheme || 'light';
    }
    """,
    Output("m2d-mantine-provider", "forceColorScheme"),
    Input("color-scheme-storage", "data")
)

# Toggle theme when button is clicked
clientside_callback(
    """
    function(n_clicks, currentTheme) {
        // Toggle between light and dark
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        return newTheme;
    }
    """,
    Output("color-scheme-storage", "data", allow_duplicate=True),
    Input("color-scheme-toggle", "n_clicks"),
    State("color-scheme-storage", "data"),
    prevent_initial_call=True,
)