"""
Setup Guide Example - Star Micronics POS Printer
Interactive step-by-step configuration guide with visual feedback
"""

import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, ALL
from dash_iconify import DashIconify

# Configuration steps
STEPS = [
    {
        "title": "StarIO.Online Account",
        "description": "Register for a Star Micronics cloud account",
        "icon": "tabler:cloud",
        "details": [
            "Visit www.starmicronicscloud.com",
            "Select your region (US or EU)",
            "Complete registration form",
            "Verify your email address"
        ]
    },
    {
        "title": "Create Device Group",
        "description": "Set up a device group for your printers",
        "icon": "tabler:folder",
        "details": [
            "Log into StarIO.Online dashboard",
            "Navigate to 'Device Groups'",
            "Create new group with your business name",
            "Save the Group Path (e.g., 'yourcompany')",
            "Enable AutoCreateDeviceQueue"
        ]
    },
    {
        "title": "Generate API Key",
        "description": "Create API credentials for your application",
        "icon": "tabler:key",
        "details": [
            "Go to 'API Keys' section",
            "Click 'Create New API Key'",
            "Enable all permissions:",
            "  • PrintToDevice",
            "  • ViewDeviceGroups",
            "  • ViewDevice",
            "  • FlushQueue",
            "Save the API key securely"
        ]
    },
    {
        "title": "Configure Printer",
        "description": "Connect your printer to CloudPRNT",
        "icon": "tabler:printer",
        "details": [
            "Access printer web interface (http://[PRINTER_IP])",
            "Navigate to Settings → CloudPRNT",
            "Enable CloudPRNT",
            "Enter CloudPRNT URL:",
            "  https://api.stario.online/v1/a/[GROUP_PATH]/cloudprnt",
            "Set polling interval to 3-5 seconds",
            "Save and restart printer"
        ]
    },
    {
        "title": "Environment Setup",
        "description": "Configure your application environment",
        "icon": "tabler:settings",
        "details": [
            "Create .env file in project root",
            "Add STAR_MICRONICS=your_api_key",
            "Add STAR_GROUP_PATH=yourcompany",
            "Add STAR_DEVICE_ID=ABC123 (optional)",
            "Install required packages"
        ]
    },
    {
        "title": "Test Connection",
        "description": "Verify everything is working",
        "icon": "tabler:check",
        "details": [
            "Run test script: python printer_service.py",
            "Verify devices appear in list",
            "Send a test print",
            "Check printer receives the job",
            "Monitor print queue status"
        ]
    }
]

# Component layout
component = dmc.Container([
    # Header
    dmc.Stack([
        dmc.Group([
            dmc.ThemeIcon(
                DashIconify(icon="tabler:checklist", width=30),
                size=40,
                radius="md",
                variant="light",
                color="blue"
            ),
            dmc.Title("Setup Guide", order=2)
        ]),
        dmc.Text(
            "Step-by-step configuration guide for Star Micronics printer integration",
            c="dimmed",
            size="sm"
        )
    ], gap="xs", mb="lg"),

    # Progress indicator
    dmc.Card([
        dmc.Stack([
            dmc.Group([
                dmc.Text("Setup Progress", fw=600),
                dmc.Badge(id="progress-badge", color="blue", children="0%")
            ], justify="space-between"),
            dmc.Progress(id="progress-bar", value=0, color="blue", size="lg")
        ])
    ], shadow="sm", padding="md", radius="md", withBorder=True, mb="lg"),

    # Stepper
    dmc.Stepper(
        id="setup-stepper",
        active=0,
        orientation="vertical",
        children=[
            dmc.StepperStep(
                label=step["title"],
                description=step["description"],
                icon=DashIconify(icon=step["icon"], width=20),
                children=[
                    dmc.Card([
                        dmc.Stack([
                            dmc.Text("Instructions:", size="sm", fw=600, c="dimmed"),
                            dmc.List([
                                dmc.ListItem(detail) for detail in step["details"]
                            ], size="sm", spacing="xs"),
                            dmc.Divider(),
                            dmc.Group([
                                dmc.Button(
                                    "Previous",
                                    variant="light",
                                    color="gray",
                                    id={"type": "prev-btn", "index": i},
                                    disabled=i == 0
                                ) if i > 0 else html.Div(),
                                dmc.Button(
                                    "Next" if i < len(STEPS) - 1 else "Complete Setup",
                                    id={"type": "next-btn", "index": i},
                                    color="blue" if i < len(STEPS) - 1 else "green",
                                    leftSection=DashIconify(
                                        icon="tabler:arrow-right" if i < len(STEPS) - 1 else "tabler:check",
                                        width=16
                                    )
                                )
                            ], justify="flex-end")
                        ], gap="sm")
                    ], shadow="xs", padding="md", radius="md", bg="var(--mantine-color-vilot-4)", mb="md")
                ]
            ) for i, step in enumerate(STEPS)
        ] + [
            dmc.StepperCompleted([
                dmc.Card([
                    dmc.Stack([
                        dmc.Center([
                            dmc.ThemeIcon(
                                DashIconify(icon="tabler:circle-check", width=40),
                                size=80,
                                radius="xl",
                                variant="light",
                                color="green"
                            )
                        ]),
                        dmc.Title("Setup Complete!", order=3, ta="center", c="green"),
                        dmc.Text(
                            "Your Star Micronics printer integration is ready to use.",
                            ta="center",
                            c="dimmed"
                        ),
                        dmc.Divider(),
                        dmc.SimpleGrid([
                            dmc.Card([
                                dmc.Stack([
                                    DashIconify(icon="tabler:book", width=24),
                                    dmc.Text("View Docs", size="sm", fw=500),
                                    dmc.Text("Read full documentation", size="xs", c="dimmed")
                                ], align="center")
                            ], padding="md", withBorder=True),
                            dmc.Card([
                                dmc.Stack([
                                    DashIconify(icon="tabler:printer", width=24),
                                    dmc.Text("Test Print", size="sm", fw=500),
                                    dmc.Text("Send a test receipt", size="xs", c="dimmed")
                                ], align="center")
                            ], padding="md", withBorder=True),
                            dmc.Card([
                                dmc.Stack([
                                    DashIconify(icon="tabler:dashboard", width=24),
                                    dmc.Text("Dashboard", size="sm", fw=500),
                                    dmc.Text("Open printer management", size="xs", c="dimmed")
                                ], align="center")
                            ], padding="md", withBorder=True)
                        ], cols=3, spacing="sm"),
                        dmc.Button(
                            "Start Over",
                            variant="light",
                            color="gray",
                            id="restart-btn",
                            fullWidth=True
                        )
                    ])
                ], shadow="sm", padding="lg", radius="md",)
            ])
        ]
    )
], size="md", px="md", py="xl")


@callback(
    [
        Output('setup-stepper', 'active'),
        Output('progress-bar', 'value'),
        Output('progress-badge', 'children')
    ],
    [
        Input({"type": "next-btn", "index": ALL}, 'n_clicks'),
        Input({"type": "prev-btn", "index": ALL}, 'n_clicks'),
        Input('restart-btn', 'n_clicks')
    ],
    State('setup-stepper', 'active'),
    prevent_initial_call=True
)
def handle_navigation(next_clicks, prev_clicks, restart_click, current_step):
    """Handle stepper navigation"""
    from dash import ctx

    if ctx.triggered_id == 'restart-btn':
        return 0, 0, "0%"

    if isinstance(ctx.triggered_id, dict):
        if ctx.triggered_id["type"] == "next-btn":
            new_step = min(current_step + 1, len(STEPS))
        else:  # prev-btn
            new_step = max(current_step - 1, 0)
    else:
        return current_step, current_step / len(STEPS) * 100, f"{int(current_step / len(STEPS) * 100)}%"

    progress = new_step / len(STEPS) * 100
    return new_step, progress, f"{int(progress)}%"