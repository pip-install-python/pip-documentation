"""
Printer Dashboard Example - Star Micronics POS Printer
Mini dashboard with tabbed interface for printer management
"""

import dash_mantine_components as dmc
from dash import html, callback, Input, Output, no_update
from dash_iconify import DashIconify

# Component layout
component = dmc.Container([
        # Header
        dmc.Stack([
            dmc.Group([
                dmc.ThemeIcon(
                    DashIconify(icon="tabler:layout-dashboard", width=30),
                    size=40,
                    radius="md",
                    variant="light",
                    color="blue"
                ),
                dmc.Title("Printer Management Dashboard", order=2)
            ]),
            dmc.Text(
                "Comprehensive printer control and monitoring interface",
                c="dimmed",
                size="sm"
            )
        ], gap="xs", mb="lg"),

        # Status summary
        dmc.Group([
            dmc.Badge("3 Devices", size="lg", variant="filled", color="blue"),
            dmc.Badge("2 Online", size="lg", variant="filled", color="green"),
            dmc.Badge("3 Queued Jobs", size="lg", variant="filled", color="yellow"),
            dmc.Button(
                "Refresh All",
                variant="light",
                color="blue",
                leftSection=DashIconify(icon="tabler:refresh", width=20),
                id="refresh-all"
            )
        ], mb="lg"),

        # Tabbed interface
        dmc.Tabs([
            dmc.TabsList([
                dmc.TabsTab(
                    "Overview",
                    value="overview",
                    leftSection=DashIconify(icon="tabler:layout", width=16)
                ),
                dmc.TabsTab(
                    "Print Queue",
                    value="queue",
                    leftSection=DashIconify(icon="tabler:list", width=16)
                ),
                dmc.TabsTab(
                    "Quick Print",
                    value="print",
                    leftSection=DashIconify(icon="tabler:printer", width=16)
                ),
                dmc.TabsTab(
                    "History",
                    value="history",
                    leftSection=DashIconify(icon="tabler:history", width=16)
                )
            ]),

            # Overview Tab
            dmc.TabsPanel(value="overview", children=[
                dmc.SimpleGrid([
                    # Printer 1 - Healthy
                    dmc.Card([
                        dmc.Stack([
                            dmc.Group([
                                dmc.ThemeIcon(
                                    DashIconify(icon="tabler:circle-check", width=20),
                                    color="green",
                                    variant="light",
                                    size="lg"
                                ),
                                dmc.Stack([
                                    dmc.Text("Kitchen Printer", fw=600),
                                    dmc.Badge("Healthy", color="green", size="sm")
                                ], gap=0)
                            ]),
                            dmc.Text("mC-Print3 • MQTT • 0 jobs", size="sm", c="dimmed"),
                            dmc.Button(
                                "Test Print",
                                size="sm",
                                variant="light",
                                fullWidth=True,
                                leftSection=DashIconify(icon="tabler:printer", width=16)
                            )
                        ])
                    ], shadow="sm", padding="md", radius="md", withBorder=True),

                    # Printer 2 - Warning
                    dmc.Card([
                        dmc.Stack([
                            dmc.Group([
                                dmc.ThemeIcon(
                                    DashIconify(icon="tabler:alert-triangle", width=20),
                                    color="yellow",
                                    variant="light",
                                    size="lg"
                                ),
                                dmc.Stack([
                                    dmc.Text("Front Desk", fw=600),
                                    dmc.Badge("Paper Low", color="yellow", size="sm")
                                ], gap=0)
                            ]),
                            dmc.Text("TSP100IV • HTTP • 3 jobs", size="sm", c="dimmed"),
                            dmc.Button(
                                "Clear Queue",
                                size="sm",
                                variant="light",
                                color="orange",
                                fullWidth=True,
                                leftSection=DashIconify(icon="tabler:trash", width=16)
                            )
                        ])
                    ], shadow="sm", padding="md", radius="md", withBorder=True),

                    # Printer 3 - Offline
                    dmc.Card([
                        dmc.Stack([
                            dmc.Group([
                                dmc.ThemeIcon(
                                    DashIconify(icon="tabler:alert-circle", width=20),
                                    color="red",
                                    variant="light",
                                    size="lg"
                                ),
                                dmc.Stack([
                                    dmc.Text("Bar Printer", fw=600),
                                    dmc.Badge("Offline", color="red", size="sm")
                                ], gap=0)
                            ]),
                            dmc.Text("mC-Print2 • Last seen 5m ago", size="sm", c="dimmed"),
                            dmc.Button(
                                "Diagnose",
                                size="sm",
                                variant="light",
                                color="red",
                                fullWidth=True,
                                leftSection=DashIconify(icon="tabler:stethoscope", width=16)
                            )
                        ])
                    ], shadow="sm", padding="md", radius="md", withBorder=True)
                ], cols={"base": 1, "sm": 2, "lg": 3}, spacing="md", mt="md")
            ]),

            # Print Queue Tab
            dmc.TabsPanel(value="queue", children=[
                dmc.Card([
                    dmc.Stack([
                        dmc.Title("Active Print Queue", order=4),
                        dmc.Text("3 jobs pending across all devices", size="sm", c="dimmed"),
                        dmc.Divider(),

                        # Queue items
                        dmc.Paper([
                            dmc.Group([
                                dmc.Stack([
                                    dmc.Text("Order #12345", fw=500),
                                    dmc.Text("Front Desk Printer", size="xs", c="dimmed")
                                ], gap=0),
                                dmc.Badge("Pending", color="yellow")
                            ], justify="space-between")
                        ], p="sm", withBorder=True, mb="xs"),

                        dmc.Paper([
                            dmc.Group([
                                dmc.Stack([
                                    dmc.Text("Order #12346", fw=500),
                                    dmc.Text("Front Desk Printer", size="xs", c="dimmed")
                                ], gap=0),
                                dmc.Badge("Pending", color="yellow")
                            ], justify="space-between")
                        ], p="sm", withBorder=True, mb="xs"),

                        dmc.Paper([
                            dmc.Group([
                                dmc.Stack([
                                    dmc.Text("Test Print", fw=500),
                                    dmc.Text("Front Desk Printer", size="xs", c="dimmed")
                                ], gap=0),
                                dmc.Badge("Pending", color="yellow")
                            ], justify="space-between")
                        ], p="sm", withBorder=True, mb="md"),

                        dmc.Button(
                            "Clear All Queues",
                            color="red",
                            variant="outline",
                            fullWidth=True,
                            leftSection=DashIconify(icon="tabler:trash", width=16)
                        )
                    ])
                ], shadow="sm", padding="lg", radius="md", withBorder=True, mt="md")
            ]),

            # Quick Print Tab
            dmc.TabsPanel(value="print", children=[
                dmc.Card([
                    dmc.Stack([
                        dmc.Title("Print Templates", order=4),
                        dmc.SimpleGrid([
                            dmc.Button(
                                "Test Receipt",
                                color="blue",
                                variant="light",
                                h=60,
                                leftSection=DashIconify(icon="tabler:receipt", width=20)
                            ),
                            dmc.Button(
                                "Sample Order",
                                color="blue",
                                variant="light",
                                h=60,
                                leftSection=DashIconify(icon="tabler:shopping-cart", width=20)
                            ),
                            dmc.Button(
                                "Test Pattern",
                                color="blue",
                                variant="light",
                                h=60,
                                leftSection=DashIconify(icon="tabler:grid-pattern", width=20)
                            ),
                            dmc.Button(
                                "Buzzer Test",
                                color="blue",
                                variant="light",
                                h=60,
                                leftSection=DashIconify(icon="tabler:bell", width=20)
                            )
                        ], cols=2, spacing="sm")
                    ])
                ], shadow="sm", padding="lg", radius="md", withBorder=True, mt="md")
            ]),

            # History Tab
            dmc.TabsPanel(value="history", children=[
                dmc.Card([
                    dmc.Stack([
                        dmc.Group([
                            dmc.Title("Print History", order=4),
                            dmc.Button(
                                "Clear",
                                size="sm",
                                variant="subtle",
                                color="red",
                                leftSection=DashIconify(icon="tabler:trash", width=16)
                            )
                        ], justify="space-between"),

                        # History items
                        dmc.Timeline([
                            dmc.TimelineItem(
                                [
                                    dmc.Text("Order #12347 printed", fw=500, size="sm"),
                                    dmc.Text("Kitchen Printer • 2 minutes ago", size="xs", c="dimmed")
                                ],
                                bullet=DashIconify(icon="tabler:check", width=12, color="green"),
                                # bulletSize=24
                            ),
                            dmc.TimelineItem(
                                [
                                    dmc.Text("Test Print sent", fw=500, size="sm"),
                                    dmc.Text("Front Desk • 5 minutes ago", size="xs", c="dimmed")
                                ],
                                bullet=DashIconify(icon="tabler:check", width=12, color="green"),
                                # bulletSize=24
                            ),
                            dmc.TimelineItem(
                                [
                                    dmc.Text("Order #12346 failed", fw=500, size="sm"),
                                    dmc.Text("Bar Printer • 10 minutes ago", size="xs", c="dimmed")
                                ],
                                bullet=DashIconify(icon="tabler:x", width=12, color="red"),
                                # bulletSize=24
                            )
                        ])
                    ])
                ], shadow="sm", padding="lg", radius="md", withBorder=True, mt="md")
            ])
        ], value="overview")
], size="xl", px="md", py="xl")


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input('refresh-all', 'n_clicks'),
    prevent_initial_call=True
)
def handle_refresh_dashboard(n_clicks):
    return [{
        "id": "refresh",
        "title": "Dashboard Refreshed",
        "message": "All printer statuses updated",
        "action": "show",
        "color": "blue",
        "icon": DashIconify(icon="tabler:refresh", width=20),
        "autoClose": 2000
    }]