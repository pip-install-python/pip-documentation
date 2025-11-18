"""
Live Print Example - Star Micronics POS Printer
Send a message directly to the creator of this documentation via their printer
"""

import os
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import html, callback, Input, Output, State, no_update, dcc
from dash_iconify import DashIconify
from datetime import datetime

# Import printer service module but don't instantiate yet
printer_service = None
PRINTER_SERVICE_AVAILABLE = False
PRINTER_IMPORT_ERROR = None

try:
    # Import from support_files
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from support_files.printer_service import StarPrinterService
    PRINTER_SERVICE_AVAILABLE = True
except Exception as e:
    PRINTER_IMPORT_ERROR = str(e)
    print(f"Warning: Printer service module not available: {e}")
    StarPrinterService = None

# Get device ID from environment
STAR_API_KEY = os.environ.get('STAR_MICRONICS')
DEVICE_ID = os.environ.get('STAR_DEVICE_ID')
GROUP_PATH = os.environ.get('STAR_GROUP_PATH', 'pipinstallpython')
REGION = os.environ.get('STAR_REGION', 'US')

# Diagnostic logging on startup
print("\n" + "="*60)
print("PRINTER SERVICE ENVIRONMENT CHECK")
print("="*60)
print(f"STAR_MICRONICS API Key: {'✅ SET' if STAR_API_KEY else '❌ NOT SET'}")
print(f"STAR_DEVICE_ID: {'✅ ' + DEVICE_ID if DEVICE_ID else '❌ NOT SET'}")
print(f"STAR_GROUP_PATH: {GROUP_PATH}")
print(f"STAR_REGION: {REGION}")
print(f"Service Import: {'✅ SUCCESS' if PRINTER_SERVICE_AVAILABLE else '❌ FAILED: ' + str(PRINTER_IMPORT_ERROR)}")
print("="*60 + "\n")

PRINTER_AVAILABLE = PRINTER_SERVICE_AVAILABLE and DEVICE_ID is not None and STAR_API_KEY is not None
MISSING_ENV_VARS = []
if not STAR_API_KEY:
    MISSING_ENV_VARS.append('STAR_MICRONICS')
if not DEVICE_ID:
    MISSING_ENV_VARS.append('STAR_DEVICE_ID')


def get_printer_service():
    """Lazy initialization of printer service - only create when needed"""
    global printer_service
    if not PRINTER_SERVICE_AVAILABLE:
        return None

    if printer_service is None:
        try:
            printer_service = StarPrinterService()
        except Exception as e:
            print(f"Error initializing printer service: {e}")
            return None

    return printer_service

# Component layout
component = dmc.Container([
    # Interval for queue updates (disabled by default to prevent auto-refresh)
    dcc.Interval(id='queue-refresh-interval', interval=5000, disabled=True, n_intervals=0),

    # Header
    dmc.Stack([
        dmc.Group([
            dmc.ThemeIcon(
                DashIconify(icon="tabler:send", width=30),
                size=40,
                radius="md",
                variant="light",
                color="blue" if PRINTER_AVAILABLE else "red"
            ),
            dmc.Title("Message the Creator", order=2)
        ]),
        dmc.Text(
            "Send a message directly to the creator of this documentation" if PRINTER_AVAILABLE else "Printer not configured - check environment variables",
            c="dimmed" if PRINTER_AVAILABLE else "red",
            size="sm"
        )
    ], gap="xs", mb="lg"),

    # Status indicator with detailed environment variable diagnostics
    dmc.Card([
        dmc.Stack([
            # Overall status
            dmc.Group([
                DashIconify(
                    icon="tabler:circle-check" if PRINTER_AVAILABLE else "tabler:alert-circle",
                    width=20,
                    color="#16a34a" if PRINTER_AVAILABLE else "#dc2626"
                ),
                dmc.Text(
                    "Printer Connected" if PRINTER_AVAILABLE else "Printer Not Available",
                    fw=600,
                    c="green" if PRINTER_AVAILABLE else "red"
                )
            ]),

            dmc.Divider(variant="dashed"),

            # Environment variable status
            dmc.Stack([
                dmc.Text("Environment Variables", size="xs", fw=600, c="dimmed", tt="uppercase"),
                dmc.Group([
                    DashIconify(
                        icon="tabler:check" if STAR_API_KEY else "tabler:x",
                        width=14,
                        color="#16a34a" if STAR_API_KEY else "#dc2626"
                    ),
                    dmc.Text(
                        f"STAR_MICRONICS: {'Set (***{STAR_API_KEY[-4:]})' if STAR_API_KEY else '❌ NOT SET'}",
                        size="sm",
                        c="dimmed" if STAR_API_KEY else "red"
                    )
                ], gap="xs"),
                dmc.Group([
                    DashIconify(
                        icon="tabler:check" if DEVICE_ID else "tabler:x",
                        width=14,
                        color="#16a34a" if DEVICE_ID else "#dc2626"
                    ),
                    dmc.Text(
                        f"STAR_DEVICE_ID: {DEVICE_ID if DEVICE_ID else '❌ NOT SET'}",
                        size="sm",
                        c="dimmed" if DEVICE_ID else "red"
                    )
                ], gap="xs"),
                dmc.Group([
                    DashIconify(icon="tabler:check", width=14, color="#16a34a"),
                    dmc.Text(f"STAR_GROUP_PATH: {GROUP_PATH}", size="sm", c="dimmed")
                ], gap="xs"),
                dmc.Group([
                    DashIconify(icon="tabler:check", width=14, color="#16a34a"),
                    dmc.Text(f"STAR_REGION: {REGION}", size="sm", c="dimmed")
                ], gap="xs"),
            ], gap="xs"),

            # Missing variables alert
            dmc.Alert(
                [
                    dmc.Stack([
                        dmc.Text("Missing Environment Variables", size="sm", fw=600),
                        dmc.Text(
                            f"Please configure: {', '.join(MISSING_ENV_VARS)}",
                            size="xs"
                        ),
                        dmc.Text(
                            "On Render: Dashboard → Environment → Add Variable",
                            size="xs",
                            c="dimmed"
                        )
                    ], gap="xs")
                ],
                title="Configuration Required",
                icon=DashIconify(icon="tabler:alert-triangle", width=20),
                color="red",
                variant="light"
            ) if MISSING_ENV_VARS else None,
        ], gap="sm")
    ], shadow="sm", padding="md", radius="md", withBorder=True, mb="lg"),

    # Message composer
    dmc.Grid([
        # Left column - Message input
        dmc.GridCol([
            dmc.Card([
                dmc.Stack([
                    dmc.Title("Compose Message", order=3, c="dimmed", size="h4"),

                    # Message template selector
                    dmc.Select(
                        id="message-template",
                        label="Message Type",
                        placeholder="Custom message",
                        data=[
                            {"value": "custom", "label": "Custom Message"},
                        ],
                        value="custom",
                        leftSection=DashIconify(icon="tabler:message", width=16),
                        disabled=True
                    ),

                    dmc.Divider(),

                    # Message editor
                    dmc.Textarea(
                        id="message-content",
                        label="Your Message",
                        description="Write your message to the creator - supports formatting like [bold], [align: center]",
                        placeholder="Write your message to the creator...",
                        minRows=10,
                        maxRows=15,
                        autosize=True,
                        value="[align: center]\n[bold][mag: w 2; h 2]Hello![normal][mag: w 1; h 1]\n\n[align: left]\nGreat documentation!\n\nI'm exploring dash-pos-printer and wanted to say hi.\n\n[align: center]\n{date} • {time}\n\n[cut]",
                    ),

                    # Print settings
                    dmc.Group([
                        dmc.NumberInput(
                            id="live-copies",
                            label="Copies",
                            value=1,
                            min=1,
                            max=10,
                            step=1,
                            style={"flex": 1}
                        ),
                        dmc.NumberInput(
                            id="live-buzzer",
                            label="Buzzer",
                            value=1,
                            min=0,
                            max=3,
                            step=1,
                            style={"flex": 1}
                        ),
                    ]),
                ])
            ], shadow="sm", padding="lg", radius="md", withBorder=True)
        ], span={"base": 12, "md": 6}),

        # Right column - Tabs with Preview and Queue
        dmc.GridCol([
            dmc.Card([
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.TabsTab(
                            "Preview & Actions",
                            value="preview",
                            leftSection=DashIconify(icon="tabler:eye", width=16)
                        ),
                        dmc.TabsTab(
                            "Queue Monitor",
                            value="queue",
                            leftSection=DashIconify(icon="tabler:list", width=16)
                        ),
                    ]),

                    # Preview tab
                    dmc.TabsPanel(value="preview", children=[
                        dmc.Stack([
                            # Preview area
                            dmc.Stack([
                                dmc.Text("Message Preview", size="sm", fw=600, c="dimmed"),
                                dmc.ScrollArea(
                                    dmc.Code(
                                        id="message-preview",
                                        block=True,
                                        style={
                                            "whiteSpace": "pre",
                                            "fontFamily": "monospace",
                                            "fontSize": "12px",
                                            "lineHeight": "1.4",
                                            "minHeight": "200px"
                                        }
                                    ),
                                    h=200,
                                    style={
                                        "border": "1px solid var(--mantine-color-gray-3)",
                                        "borderRadius": "var(--mantine-radius-sm)"
                                    }
                                )
                            ]),

                            dmc.Divider(),

                            # Action buttons
                            dmc.Stack([
                                dmc.Button(
                                    "Send to Printer",
                                    id="live-print-btn",
                                    color="blue",
                                    leftSection=DashIconify(icon="tabler:printer-check", width=20),
                                    fullWidth=True,
                                    size="lg",
                                    disabled=not PRINTER_AVAILABLE
                                ),
                                dmc.Button(
                                    "Clear Message",
                                    id="clear-message-btn",
                                    variant="light",
                                    color="gray",
                                    leftSection=DashIconify(icon="tabler:eraser", width=20),
                                    fullWidth=True
                                ),
                            ]),

                            # Info alert
                            dmc.Alert(
                                [
                                    dmc.Stack([
                                        dmc.Text("Message the Creator", size="sm", fw=600),
                                        dmc.Text(
                                            "Your message will be sent to the creator's printer via the Star Micronics CloudPRNT API. Make it fun!",
                                            size="xs"
                                        )
                                    ])
                                ],
                                title="Direct to Creator",
                                icon=DashIconify(icon="tabler:info-circle", width=20),
                                color="blue" if PRINTER_AVAILABLE else "red",
                                variant="light"
                            )
                        ], gap="md")
                    ]),

                    # Queue tab
                    dmc.TabsPanel(value="queue", children=[
                        dmc.Stack([
                            dmc.Group([
                                dmc.Text("Current Queued Jobs", size="sm", fw=600, c="dimmed"),
                                dmc.Group([
                                    dmc.Button(
                                        "Refresh",
                                        id="queue-refresh-btn",
                                        size="xs",
                                        variant="light",
                                        leftSection=DashIconify(icon="tabler:refresh", width=14),
                                        disabled=not PRINTER_AVAILABLE
                                    ),
                                    dmc.Button(
                                        "Clear Queue",
                                        id="queue-clear-btn",
                                        size="xs",
                                        variant="light",
                                        color="red",
                                        leftSection=DashIconify(icon="tabler:trash", width=14),
                                        disabled=not PRINTER_AVAILABLE
                                    ),
                                ], gap="xs")
                            ], justify="space-between"),

                            # Queue grid
                            dag.AgGrid(
                                id="queue-grid",
                                columnDefs=[
                                    {"headerName": "Job ID", "field": "JobId", "flex": 1},
                                    {"headerName": "Name", "field": "JobName", "flex": 1},
                                    {"headerName": "Status", "field": "Status", "flex": 1},
                                    {"headerName": "Created", "field": "Created", "flex": 1},
                                ],
                                rowData=[],
                                defaultColDef={
                                    "sortable": True,
                                    "filter": True,
                                    "resizable": True,
                                },
                                dashGridOptions={
                                    "pagination": False,
                                    "domLayout": "autoHeight",
                                },
                                style={"height": "250px"},
                            ),

                            dmc.Text(
                                id="queue-status",
                                size="xs",
                                c="dimmed",
                                ta="center"
                            )
                        ], gap="sm")
                    ]),
                ], id="live-print-tabs", value="preview")
            ], shadow="sm", padding="lg", radius="md", withBorder=True)
        ], span={"base": 12, "md": 6})
    ], gutter="md"),

    # Star Document Markup reference
    dmc.Card([
        dmc.Stack([
            dmc.Title("Star Document Markup Quick Reference", order=4),
            dmc.SimpleGrid([
                dmc.Stack([
                    dmc.Text("Formatting", size="sm", fw=600, c="blue"),
                    dmc.Code("[bold]Bold text[normal]", block=True),
                    dmc.Code("[align: center]Centered", block=True),
                    dmc.Code("[align: left]Left aligned", block=True),
                    dmc.Code("[align: right]Right aligned", block=True),
                ], gap="xs"),
                dmc.Stack([
                    dmc.Text("Size", size="sm", fw=600, c="blue"),
                    dmc.Code("[mag: w 2; h 2]Big text", block=True),
                    dmc.Code("[mag: w 1; h 1]Normal", block=True),
                    dmc.Code("[invert]Inverted colors", block=True),
                    dmc.Code("[ul]Underlined text", block=True),
                ], gap="xs"),
                dmc.Stack([
                    dmc.Text("Special", size="sm", fw=600, c="blue"),
                    dmc.Code("[cut]Cut paper", block=True),
                    dmc.Code("[buzzer: pattern=A]Beep", block=True),
                    dmc.Code("---Dashed line---", block=True),
                    dmc.Code("===Double line===", block=True),
                ], gap="xs"),
            ], cols=3, spacing="md")
        ])
    ], shadow="sm", padding="lg", radius="md", withBorder=True, mt="lg")
], size="xl", px="md", py="xl")


@callback(
    Output('message-preview', 'children'),
    Input('message-content', 'value'),
)
def update_preview(content):
    """Update preview with formatted date/time"""
    if not content:
        return "No content to preview..."

    now = datetime.now()
    try:
        preview = content.format(
            date=now.strftime('%m/%d/%Y'),
            time=now.strftime('%I:%M %p')
        )
    except Exception:
        preview = content
    return preview


@callback(
    Output('message-content', 'value'),
    Input('message-template', 'value'),
    prevent_initial_call=True
)
def load_template(template):
    """Load default message template"""
    # Only one template now - custom message for creator
    return "[align: center]\n[bold][mag: w 2; h 2]Hello![normal][mag: w 1; h 1]\n\n[align: left]\nGreat documentation!\n\nI'm exploring dash-pos-printer and wanted to say hi.\n\n[align: center]\n{date} • {time}\n\n[cut]"


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input('live-print-btn', 'n_clicks'),
    State('message-content', 'value'),
    State('live-copies', 'value'),
    State('live-buzzer', 'value'),
    prevent_initial_call=True
)
def handle_live_print(n_clicks, content, copies, buzzer):
    """Send message to actual printer"""
    # Explicitly check if button was clicked (prevent auto-fire on page load)
    if not n_clicks or n_clicks == 0:
        return no_update

    if not PRINTER_AVAILABLE:
        return [{
            "id": "printer-error",
            "title": "Printer Not Available",
            "message": "Please configure environment variables: STAR_MICRONICS, STAR_GROUP_PATH, STAR_DEVICE_ID",
            "action": "show",
            "color": "red",
            "icon": DashIconify(icon="tabler:alert-circle", width=20),
            "autoClose": 5000
        }]

    if not content:
        return [{
            "id": "no-content",
            "title": "No Content",
            "message": "Please enter a message to print",
            "action": "show",
            "color": "yellow",
            "icon": DashIconify(icon="tabler:alert-triangle", width=20),
            "autoClose": 3000
        }]

    try:
        # Get printer service (lazy initialization)
        service = get_printer_service()
        if not service:
            return [{
                "id": "service-init-error",
                "title": "Service Initialization Failed",
                "message": "Could not initialize printer service",
                "action": "show",
                "color": "red",
                "icon": DashIconify(icon="tabler:alert-circle", width=20),
                "autoClose": 5000
            }]

        # Format message with current date/time
        now = datetime.now()
        try:
            formatted_content = content.format(
                date=now.strftime('%m/%d/%Y'),
                time=now.strftime('%I:%M %p')
            )
        except Exception:
            formatted_content = content

        # Send to printer
        result = service.print_receipt(
            content=formatted_content,
            job_name=f"Visitor Message {now.strftime('%H:%M:%S')}",
            device_id=DEVICE_ID,
            copies=copies or 1,
            endbuzzer=buzzer or 0
        )

        # Check result
        if "error" in result:
            return [{
                "id": "print-error",
                "title": "Print Failed",
                "message": f"Error: {result['error']}",
                "action": "show",
                "color": "red",
                "icon": DashIconify(icon="tabler:alert-circle", width=20),
                "autoClose": 5000
            }]

        return [{
            "id": "print-success",
            "title": "Message Sent!",
            "message": f"Your message has been sent to the creator's printer!",
            "action": "show",
            "color": "green",
            "icon": DashIconify(icon="tabler:circle-check", width=20),
            "autoClose": 3000
        }]

    except Exception as e:
        return [{
            "id": "print-exception",
            "title": "Print Error",
            "message": f"Exception: {str(e)}",
            "action": "show",
            "color": "red",
            "icon": DashIconify(icon="tabler:bug", width=20),
            "autoClose": 5000
        }]


@callback(
    Output('message-content', 'value', allow_duplicate=True),
    Input('clear-message-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_message(n_clicks):
    """Clear the message content"""
    return ""


@callback(
    [Output('queue-grid', 'rowData'),
     Output('queue-status', 'children')],
    [Input('queue-refresh-btn', 'n_clicks'),
     Input('queue-refresh-interval', 'n_intervals')],
    prevent_initial_call=True
)
def update_queue(n_clicks, n_intervals):
    """Fetch and update queue data"""
    if not PRINTER_AVAILABLE:
        return [], "Printer not available"

    try:
        # Get printer service (lazy initialization)
        service = get_printer_service()
        if not service:
            return [], "Service initialization failed"

        queue_data = service.get_queue(DEVICE_ID)

        if not queue_data or len(queue_data) == 0:
            return [], f"No jobs in queue - Last checked: {datetime.now().strftime('%I:%M:%S %p')}"

        # Format queue data for AG Grid
        rows = []
        for job in queue_data:
            rows.append({
                "JobId": job.get("JobId", "N/A"),
                "JobName": job.get("JobName", "Unnamed"),
                "Status": job.get("Status", "Pending"),
                "Created": job.get("Created", "Unknown"),
            })

        return rows, f"{len(rows)} job(s) in queue - Last updated: {datetime.now().strftime('%I:%M:%S %p')}"

    except Exception as e:
        return [], f"Error fetching queue: {str(e)}"


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input('queue-clear-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_clear_queue(n_clicks):
    """Clear all pending print jobs from queue"""
    # Explicitly check if button was clicked (prevent auto-fire on page load)
    if not n_clicks or n_clicks == 0:
        return no_update

    if not PRINTER_AVAILABLE:
        return [{
            "id": "queue-clear-error",
            "title": "Printer Not Available",
            "message": "Cannot clear queue - printer not configured",
            "action": "show",
            "color": "red",
            "icon": DashIconify(icon="tabler:alert-circle", width=20),
            "autoClose": 3000
        }]

    try:
        # Get printer service (lazy initialization)
        service = get_printer_service()
        if not service:
            return [{
                "id": "service-init-error",
                "title": "Service Initialization Failed",
                "message": "Could not initialize printer service",
                "action": "show",
                "color": "red",
                "icon": DashIconify(icon="tabler:alert-circle", width=20),
                "autoClose": 3000
            }]

        success = service.clear_queue(DEVICE_ID)

        if success:
            return [{
                "id": "queue-cleared",
                "title": "Queue Cleared",
                "message": "All pending print jobs have been cleared",
                "action": "show",
                "color": "green",
                "icon": DashIconify(icon="tabler:check", width=20),
                "autoClose": 2000
            }]
        else:
            return [{
                "id": "queue-clear-failed",
                "title": "Clear Failed",
                "message": "Could not clear the print queue",
                "action": "show",
                "color": "red",
                "icon": DashIconify(icon="tabler:alert-circle", width=20),
                "autoClose": 3000
            }]
    except Exception as e:
        return [{
            "id": "queue-clear-exception",
            "title": "Clear Error",
            "message": f"Error clearing queue: {str(e)}",
            "action": "show",
            "color": "red",
            "icon": DashIconify(icon="tabler:bug", width=20),
            "autoClose": 3000
        }]


@callback(
    [Output('queue-grid', 'rowData', allow_duplicate=True),
     Output('queue-status', 'children', allow_duplicate=True)],
    Input('live-print-tabs', 'value'),
    prevent_initial_call=True
)
def load_queue_on_tab_change(tab_value):
    """Load queue data when Queue Monitor tab is selected"""
    if tab_value != "queue":
        return no_update, no_update

    if not PRINTER_AVAILABLE:
        return [], "Printer not available"

    try:
        # Get printer service (lazy initialization)
        service = get_printer_service()
        if not service:
            return [], "Service initialization failed"

        queue_data = service.get_queue(DEVICE_ID)

        if not queue_data or len(queue_data) == 0:
            return [], f"No jobs in queue - Last checked: {datetime.now().strftime('%I:%M:%S %p')}"

        # Format queue data for AG Grid
        rows = []
        for job in queue_data:
            rows.append({
                "JobId": job.get("JobId", "N/A"),
                "JobName": job.get("JobName", "Unnamed"),
                "Status": job.get("Status", "Pending"),
                "Created": job.get("Created", "Unknown"),
            })

        return rows, f"{len(rows)} job(s) in queue - Last checked: {datetime.now().strftime('%I:%M:%S %p')}"

    except Exception as e:
        return [], f"Error fetching queue: {str(e)}"