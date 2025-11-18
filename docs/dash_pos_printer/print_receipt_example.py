"""
Print Receipt Example - Star Micronics POS Printer
Interactive receipt printing with Star Document Markup
"""

import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, no_update
from dash_iconify import DashIconify
from datetime import datetime

# Sample receipt templates
RECEIPT_TEMPLATES = {
    "simple": """[align: center]
[bold][mag: w 2; h 2]YOUR STORE NAME[normal][mag: w 1; h 1]
================================

[align: left]
Order #: ORD-12345
Date: {date}
Time: {time}

================================
[bold]ITEMS:[normal]
2x Lobster Roll         $35.98
1x Clam Chowder         $12.99
--------------------------------
Subtotal:               $48.97
Tax (8.25%):            $4.04
================================
[bold]TOTAL:                  $52.01[normal]

Payment: Credit Card

[align: center]
Thank you for your order!
Visit us again soon!

[cut]""",

    "detailed": """[align: center]
[bold][mag: w 2; h 2]RESTAURANT NAME[normal][mag: w 1; h 1]
123 Main Street
City, State 12345
Phone: (555) 123-4567
================================

[align: left]
Order #: ORD-12345
Server: John Doe
Table: 5
Date: {date}
Time: {time}

================================
[bold]ITEMS:[normal]
Qty  Item           Price  Total
--------------------------------
2    Lobster Roll   17.99  35.98
     - Extra Mayo
1    Clam Chowder   12.99  12.99
     - Bread Bowl
1    Iced Tea        2.99   2.99
--------------------------------
Subtotal:                  $51.96
Tax (8.25%):               $4.29
Tip (18%):                 $9.35
================================
[bold]TOTAL:                     $65.60[normal]

Payment: Credit Card ****1234
Auth Code: 123456

[align: center]
★★★ Thank You! ★★★
Please visit us again soon!

Rate your experience:
www.yourrestaurant.com/review

[cut]""",

    "minimal": """[align: center]
QUICK RECEIPT

[align: left]
Order: #{order_num}
Items: 3
Total: $52.01

{date} {time}

[align: center]
Thank you!
[cut]"""
}

# Component layout
component = dmc.Container([
        # Header
        dmc.Stack([
            dmc.Group([
                dmc.ThemeIcon(
                    DashIconify(icon="tabler:receipt", width=30),
                    size=40,
                    radius="md",
                    variant="light",
                    color="blue"
                ),
                dmc.Title("Print Receipt", order=2)
            ]),
            dmc.Text(
                "Create and send formatted receipts using Star Document Markup",
                c="dimmed",
                size="sm"
            )
        ], gap="xs", mb="lg"),

        dmc.Grid([
            # Left column - Template selection and preview
            dmc.GridCol([
                dmc.Card([
                    dmc.Stack([
                        dmc.Title("Receipt Template", order=3, c="dimmed", size="h4"),

                        # Template selector
                        dmc.SegmentedControl(
                            id="template-selector",
                            data=[
                                {"value": "simple", "label": "Simple"},
                                {"value": "detailed", "label": "Detailed"},
                                {"value": "minimal", "label": "Minimal"},
                            ],
                            value="simple",
                            fullWidth=True,
                            color="blue"
                        ),

                        dmc.Divider(),

                        # Preview
                        dmc.Stack([
                            dmc.Group([
                                DashIconify(icon="tabler:eye", width=16),
                                dmc.Text("Preview", size="sm", fw=500)
                            ]),
                            dmc.ScrollArea(
                                dmc.Code(
                                    id="receipt-preview",
                                    block=True,
                                    style={
                                        "whiteSpace": "pre",
                                        "fontFamily": "monospace",
                                        "fontSize": "12px",
                                        "lineHeight": "1.4"
                                    }
                                ),
                                h=400,
                                style={
                                    "border": "1px solid var(--mantine-color-gray-3)",
                                    "borderRadius": "var(--mantine-radius-sm)"
                                }
                            )
                        ])
                    ])
                ], shadow="sm", padding="lg", radius="md", withBorder=True)
            ], span={"base": 12, "md": 6}),

            # Right column - Print options and controls
            dmc.GridCol([
                dmc.Card([
                    dmc.Stack([
                        dmc.Title("Print Options", order=3, c="dimmed", size="h4"),

                        # Device selector
                        dmc.Select(
                            id="device-select",
                            label="Target Printer",
                            placeholder="Select a printer",
                            data=[
                                {"value": "ABC123", "label": "🟢 Kitchen Printer (ABC123)"},
                                {"value": "XYZ789", "label": "🟢 Front Desk (XYZ789)"},
                                {"value": "JKL345", "label": "🔴 Bar Printer (JKL345) - Offline"},
                            ],
                            value="ABC123",
                            leftSection=DashIconify(icon="tabler:printer", width=16)
                        ),

                        # Print settings
                        dmc.NumberInput(
                            id="copies-input",
                            label="Number of Copies",
                            description="Print 1-10 copies",
                            value=1,
                            min=1,
                            max=10,
                            step=1,
                            leftSection=DashIconify(icon="tabler:copy", width=16)
                        ),

                        dmc.Group([
                            dmc.NumberInput(
                                id="buzzer-before",
                                label="Buzzer Before",
                                description="Beeps before printing",
                                value=0,
                                min=0,
                                max=3,
                                step=1,
                                style={"flex": 1}
                            ),
                            dmc.NumberInput(
                                id="buzzer-after",
                                label="Buzzer After",
                                description="Beeps after printing",
                                value=1,
                                min=0,
                                max=3,
                                step=1,
                                style={"flex": 1}
                            )
                        ]),

                        dmc.Divider(),

                        # Action buttons
                        dmc.Stack([
                            dmc.Button(
                                "Send to Printer",
                                id="print-btn",
                                color="blue",
                                leftSection=DashIconify(icon="tabler:send", width=20),
                                fullWidth=True,
                                size="lg"
                            ),
                            dmc.Button(
                                "Test Print",
                                id="test-print-btn",
                                variant="light",
                                color="blue",
                                leftSection=DashIconify(icon="tabler:printer", width=20),
                                fullWidth=True
                            )
                        ]),

                        # Info alert
                        dmc.Alert(
                            [
                                dmc.Stack([
                                    dmc.Text("Star Document Markup", size="sm", fw=600),
                                    dmc.Text(
                                        "Use markup commands like [bold], [align: center], and [mag: w 2; h 2] to format your receipts.",
                                        size="xs"
                                    )
                                ])
                            ],
                            title="Formatting Guide",
                            icon=DashIconify(icon="tabler:info-circle", width=20),
                            color="blue",
                            variant="light"
                        )
                    ])
                ], shadow="sm", padding="lg", radius="md", withBorder=True)
            ], span={"base": 12, "md": 6})
        ], gutter="md")
], size="xl", px="md", py="xl")


@callback(
    Output('receipt-preview', 'children'),
    Input('template-selector', 'value')
)
def update_preview(template_key):
    """Update receipt preview based on selected template"""
    now = datetime.now()
    receipt = RECEIPT_TEMPLATES.get(template_key, RECEIPT_TEMPLATES['simple'])

    # Fill in dynamic values
    receipt = receipt.format(
        date=now.strftime('%m/%d/%Y'),
        time=now.strftime('%I:%M %p'),
        order_num="12345"
    )

    return receipt


@callback(
    Output('notification-container', 'sendNotifications', allow_duplicate=True),
    Input('print-btn', 'n_clicks'),
    Input('test-print-btn', 'n_clicks'),
    State('template-selector', 'value'),
    State('device-select', 'value'),
    State('copies-input', 'value'),
    State('buzzer-before', 'value'),
    State('buzzer-after', 'value'),
    prevent_initial_call=True
)
def handle_print_receipt(print_clicks, test_clicks, template, device, copies, buzzer_before, buzzer_after):
    """Handle print and test print button clicks"""
    from dash import ctx

    if ctx.triggered_id == 'print-btn':
        return [{
            "id": "print-success",
            "title": "Receipt Sent",
            "message": f"Print job sent to {device} ({copies} copies)",
            "action": "show",
            "color": "green",
            "icon": DashIconify(icon="tabler:printer-check", width=20),
            "autoClose": 3000
        }]
    elif ctx.triggered_id == 'test-print-btn':
        return [{
            "id": "test-print",
            "title": "Test Print Sent",
            "message": f"Test receipt sent to {device}",
            "action": "show",
            "color": "blue",
            "icon": DashIconify(icon="tabler:printer", width=20),
            "autoClose": 2000
        }]

    return no_update