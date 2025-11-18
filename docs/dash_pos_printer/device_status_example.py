"""
Device Status Example - Star Micronics POS Printer
Displays real-time printer status with health diagnostics
"""

import dash_mantine_components as dmc
from dash import html, callback, Input, Output, no_update, ALL
from dash_iconify import DashIconify

# Mock device data for demonstration
MOCK_DEVICES = [
    {
        'Id': 'Kitchen-Printer-01',
        'AccessIdentifier': 'ABC123DEF456',
        'Mac': '00:11:62:XX:XX:XX',
        'ClientType': 'mC-Print3',
        'Status': {
            'Online': True,
            'PaperEmpty': False,
            'PaperLow': False,
            'CoverOpen': False,
            'MechanicalError': False,
            'CutterError': False,
            'HoldPrint': False
        },
        'QueuedJobs': 0,
        'LastConnection': 0,  # MQTT mode
        'PaperWidthMM': 72,
        'PollingInterval': 0
    },
    {
        'Id': 'Front-Desk-Printer',
        'AccessIdentifier': 'XYZ789GHI012',
        'Mac': '00:11:62:YY:YY:YY',
        'ClientType': 'TSP100IV',
        'Status': {
            'Online': True,
            'PaperEmpty': False,
            'PaperLow': True,  # Warning
            'CoverOpen': False,
            'MechanicalError': False,
            'CutterError': False,
            'HoldPrint': False
        },
        'QueuedJobs': 3,  # Some jobs pending
        'LastConnection': 4,  # HTTP polling
        'PaperWidthMM': 80,
        'PollingInterval': 3
    },
    {
        'Id': 'Bar-Printer',
        'AccessIdentifier': 'JKL345MNO678',
        'Mac': '00:11:62:ZZ:ZZ:ZZ',
        'ClientType': 'mC-Print2',
        'Status': {
            'Online': False,  # Offline
            'PaperEmpty': False,
            'PaperLow': False,
            'CoverOpen': False,
            'MechanicalError': False,
            'CutterError': False,
            'HoldPrint': False
        },
        'QueuedJobs': 0,
        'LastConnection': 325,  # Not seen in 5+ minutes
        'PaperWidthMM': 72,
        'PollingInterval': 5
    }
]


def analyze_device_status(device):
    """Analyze device status and return diagnostic info"""
    status = device.get('Status', {})
    issues = []
    warnings = []

    # Check critical issues
    if not status.get('Online', False):
        issues.append("Printer is offline")
    if status.get('PaperEmpty', False):
        issues.append("Paper is empty")
    if status.get('CoverOpen', False):
        issues.append("Cover is open")
    if status.get('MechanicalError', False):
        issues.append("Mechanical error detected")
    if status.get('CutterError', False):
        issues.append("Cutter error")

    # Check warnings
    if status.get('PaperLow', False):
        warnings.append("Paper is low")
    if device.get('QueuedJobs', 0) > 5:
        warnings.append(f"{device.get('QueuedJobs')} jobs in queue")
    if status.get('HoldPrint', False):
        warnings.append("Print is on hold")

    # Check connection
    last_conn = device.get('LastConnection', -1)
    if last_conn == 0:
        connection_mode = "MQTT"
    elif last_conn > 0:
        if last_conn > 120:
            warnings.append(f"Last seen {last_conn}s ago")
        connection_mode = "HTTP Polling"
    else:
        connection_mode = "Unknown"

    return {
        'issues': issues,
        'warnings': warnings,
        'connection_mode': connection_mode,
        'healthy': len(issues) == 0
    }


def create_device_card(device):
    """Create a status card for a single device"""
    analysis = analyze_device_status(device)

    # Determine overall status
    if not analysis['healthy']:
        status_color = "red"
        status_icon = "tabler:alert-circle"
        status_text = "Issues Detected"
    elif analysis['warnings']:
        status_color = "yellow"
        status_icon = "tabler:alert-triangle"
        status_text = "Warnings"
    else:
        status_color = "green"
        status_icon = "tabler:circle-check"
        status_text = "Healthy"

    # Build diagnostic messages
    diagnostic_items = []

    # Issues (red)
    for issue in analysis['issues']:
        diagnostic_items.append(
            dmc.Group([
                DashIconify(icon="tabler:x", width=16, color="#dc2626"),
                dmc.Text(issue, size="sm", c="red")
            ], gap="xs")
        )

    # Warnings (yellow)
    for warning in analysis['warnings']:
        diagnostic_items.append(
            dmc.Group([
                DashIconify(icon="tabler:alert-triangle", width=16, color="#eab308"),
                dmc.Text(warning, size="sm", c="yellow.8")
            ], gap="xs")
        )

    # If healthy
    if not diagnostic_items:
        diagnostic_items.append(
            dmc.Group([
                DashIconify(icon="tabler:check", width=16, color="#16a34a"),
                dmc.Text("All systems operational", size="sm", c="green")
            ], gap="xs")
        )

    return dmc.Card([
        dmc.Stack([
            # Device header with status
            dmc.Group([
                dmc.Group([
                    dmc.ThemeIcon(
                        DashIconify(icon=status_icon, width=24),
                        size=40,
                        radius="xl",
                        variant="light",
                        color=status_color
                    ),
                    dmc.Stack([
                        dmc.Text(device.get('Id', 'Unknown Device'), fw=600),
                        dmc.Group([
                            dmc.Badge(
                                status_text,
                                color=status_color,
                                variant="light",
                                size="sm"
                            ),
                            dmc.Badge(
                                analysis['connection_mode'],
                                color="blue",
                                variant="outline",
                                size="sm"
                            )
                        ], gap="xs")
                    ], gap=0)
                ])
            ], justify="space-between"),

            dmc.Divider(variant="dashed"),

            # Device info grid
            dmc.SimpleGrid([
                dmc.Stack([
                    dmc.Text("Access ID", size="xs", c="dimmed"),
                    dmc.Code(device.get('AccessIdentifier', 'N/A'), style={"fontSize": "11px"})
                ], gap=2),
                dmc.Stack([
                    dmc.Text("Model", size="xs", c="dimmed"),
                    dmc.Text(device.get('ClientType', 'Unknown'), size="sm", fw=500)
                ], gap=2),
                dmc.Stack([
                    dmc.Text("Queue", size="xs", c="dimmed"),
                    dmc.Badge(
                        f"{device.get('QueuedJobs', 0)} jobs",
                        color="blue" if device.get('QueuedJobs', 0) == 0 else "yellow",
                        variant="filled"
                    )
                ], gap=2),
                dmc.Stack([
                    dmc.Text("Paper", size="xs", c="dimmed"),
                    dmc.Text(
                        f"{device.get('PaperWidthMM', 'N/A')}mm",
                        size="sm",
                        fw=500
                    )
                ], gap=2),
            ], cols=2, spacing="sm", verticalSpacing="sm"),

            # Diagnostics section
            dmc.Paper(
                dmc.Stack(diagnostic_items, gap="xs"),
                p="sm",
                radius="sm",
                withBorder=True
            ),

            # Action buttons
            dmc.Group([
                dmc.Button(
                    "Test Print",
                    size="sm",
                    variant="light",
                    color="blue",
                    leftSection=DashIconify(icon="tabler:printer", width=16),
                    id={'type': 'test-print', 'index': device.get('AccessIdentifier', '')}
                ),
                dmc.Button(
                    "Clear Queue",
                    size="sm",
                    variant="subtle",
                    color="red",
                    leftSection=DashIconify(icon="tabler:trash", width=16),
                    id={'type': 'clear-queue', 'index': device.get('AccessIdentifier', '')},
                    disabled=device.get('QueuedJobs', 0) == 0
                )
            ], grow=True)
        ])
    ], shadow="sm", padding="lg", radius="md", withBorder=True,
        style={"borderColor": f"var(--mantine-color-{status_color}-2)"})


# Component layout
component = dmc.Container([
    # Header
    dmc.Stack([
        dmc.Group([
            dmc.ThemeIcon(
                DashIconify(icon="tabler:printer", width=30),
                size=40,
                radius="md",
                variant="light",
                color="blue"
            ),
            dmc.Title("Device Status Monitor", order=2)
        ]),
        dmc.Text(
            "Real-time printer health monitoring with diagnostics",
            c="dimmed",
            size="sm"
        )
    ], gap="xs", mb="lg"),

    # Summary badges
    dmc.Group([
        dmc.Badge(
            f"{len(MOCK_DEVICES)} Devices",
            size="lg",
            variant="filled",
            color="blue"
        ),
        dmc.Badge(
            f"{sum(1 for d in MOCK_DEVICES if d['Status']['Online'])} Online",
            size="lg",
            variant="filled",
            color="green"
        ),
        dmc.Badge(
            f"{sum(d.get('QueuedJobs', 0) for d in MOCK_DEVICES)} Queued Jobs",
            size="lg",
            variant="filled",
            color="yellow"
        ),
        dmc.Button(
            "Refresh",
            variant="light",
            color="blue",
            leftSection=DashIconify(icon="tabler:refresh", width=20),
            id="refresh-btn"
        )
    ], mb="lg"),

    # Device grid
    dmc.Grid([
        dmc.GridCol(
            create_device_card(device),
            span={"base": 12, "md": 6, "lg": 4}
        ) for device in MOCK_DEVICES
    ], gutter="md")
], size="xl", px="md", py="xl")


# Callbacks for button actions
@callback(
    Output('notification-container', 'sendNotifications'),
    Input('refresh-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_refresh_device_status(n_clicks):
    """Handle refresh button click"""
    return [{
        "id": "refresh",
        "title": "Status Updated",
        "message": "All device statuses have been refreshed",
        "action": "show",
        "color": "blue",
        "icon": DashIconify(icon="tabler:refresh", width=20),
        "autoClose": 2000
    }]


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input({'type': 'test-print', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_test_print_device_status(n_clicks):
    """Handle test print button clicks"""
    if not any(n_clicks):
        return no_update

    return [{
        "id": "test-print",
        "title": "Test Print Sent",
        "message": "Receipt has been sent to the print queue",
        "action": "show",
        "color": "green",
        "icon": DashIconify(icon="tabler:printer-check", width=20),
        "autoClose": 3000
    }]


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input({'type': 'clear-queue', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_clear_queue_device_status(n_clicks):
    """Handle clear queue button clicks"""
    if not any(n_clicks):
        return no_update

    return [{
        "id": "clear-queue",
        "title": "Queue Cleared",
        "message": "All pending print jobs have been removed",
        "action": "show",
        "color": "orange",
        "icon": DashIconify(icon="tabler:trash-check", width=20),
        "autoClose": 2000
    }]