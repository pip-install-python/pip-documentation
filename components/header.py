import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, html, get_asset_url
from dash_iconify import DashIconify


def create_link(icon, href):
    """Create an external link icon button"""
    return dmc.Anchor(
        dmc.ActionIcon(
            DashIconify(icon=icon, width=22),
            variant="subtle",
            size="lg",
            color="gray",
        ),
        href=href,
        target="_blank",
    )


def create_other_apps_menu():
    """Create menu for other Pip Install Python applications"""
    return dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.Button(
                    "Other Apps",
                    variant="subtle",
                    color="gray",
                    size="sm",
                    leftSection=DashIconify(icon="svg-spinners:blocks-scale", width=18),
                )
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuItem(
                        "Plotly.pro",
                        leftSection=DashIconify(icon="simple-icons:plotly", width=16),
                        href="https://plotly.pro",
                        target="_blank",
                    ),
                    dmc.MenuItem(
                        "ai-agent.buzz",
                        leftSection=DashIconify(icon="mdi:robot-outline", width=16),
                        href="https://ai-agent.buzz",
                        target="_blank",
                    ),
                    dmc.MenuItem(
                        "GeoMapIndex",
                        leftSection=DashIconify(icon="mdi:map-marker-outline", width=16),
                        href="https://dash.geomapindex.com",
                        target="_blank",
                    ),
                ]
            ),
        ],
        trigger="hover",
        openDelay=100,
        closeDelay=200,
    )


def create_search(data):
    """Create searchable dropdown for component navigation"""
    return dmc.Select(
        id="select-component",
        placeholder="Search pages...",
        searchable=True,
        clearable=True,
        w=240,
        size="sm",
        mb=10,
        nothingFoundMessage="No pages found",
        leftSection=DashIconify(icon="mingcute:search-3-line", width=18),
        data=[
            {"label": component["name"], "value": component["path"]}
            for component in data
            if component["name"] not in ["Home", "Not found 404"]
        ],
        visibleFrom="sm",
        comboboxProps={"zIndex": 2000},
        styles={
            "input": {
                "borderColor": "var(--mantine-color-gray-4)",
            }
        }
    )


def create_header(data):
    """Create application header with logo, search, and theme toggle"""
    return dmc.AppShellHeader(
        dmc.Group(
            [
                # Left section: Hamburger menu + Logo
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            DashIconify(icon="radix-icons:hamburger-menu", width=22),
                            id="drawer-hamburger-button",
                            variant="subtle",
                            size="lg",
                            color="#03c7e5",
                            hiddenFrom="md",
                        ),
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    dmc.Image(
                                        src=get_asset_url('apple-touch-icon.png'),
                                        h='36px',
                                        w='36px',
                                        visibleFrom="sm",
                                    ),
                                    dmc.Text(
                                        "Pip Docs",
                                        size="lg",
                                        fw=700,
                                        c="light-dark(rgb(28, 126, 214), #74c0fc)",
                                        id="dash-docs-title",
                                        visibleFrom="sm",
                                    ),
                                ],
                                gap="sm",
                            ),
                            href="/",
                            underline=False,
                        ),
                    ],
                    gap="md",
                ),

                # Right section: Other Apps + Search + Discord + GitHub + Theme toggle
                dmc.Group(
                    [
                        create_other_apps_menu(),
                        create_search(data),
                        create_link(
                            "qlementine-icons:discord-fill-24",
                            "https://discord.gg/e5s5uHWUHH",
                        ),
                        create_link(
                            "radix-icons:github-logo",
                            "https://github.com/pip-install-python/Dash-Documentation-Boilerplate",
                        ),
                        dmc.ActionIcon(
                            [
                                DashIconify(
                                    icon="radix-icons:sun",
                                    width=22,
                                    id="light-theme-icon",
                                ),
                                DashIconify(
                                    icon="radix-icons:moon",
                                    width=22,
                                    id="dark-theme-icon",
                                ),
                            ],
                            variant="subtle",
                            color="yellow",
                            id="color-scheme-toggle",
                            size="lg",
                        ),
                    ],
                    gap="sm",
                ),
            ],
            justify="space-between",
            h=70,
            px="xl",
        ),
    )


clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "href"),
    Input("select-component", "value"),
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)
