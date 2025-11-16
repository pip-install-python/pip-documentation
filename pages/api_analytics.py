"""
API Analytics Dashboard

Displays comprehensive analytics for API cost breakdown including:
- User questions and responses
- Cost tracking per session
- Model usage statistics
- Temporal trends
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_ag_grid as dag
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Register this page
dash.register_page(
    __name__,
    path="/analytics",
    name="API Analytics",
    title="API Analytics Dashboard",
    description="View API usage and cost analytics",
    icon="mdi:chart-line"
)


def load_api_data():
    """Load API cost breakdown data from JSON file."""
    api_file = Path('api-cost-breakdown.json')
    if not api_file.exists():
        return None

    try:
        with open(api_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading API data: {e}")
        return None


def calculate_summary_stats(data):
    """Calculate summary statistics from API data."""
    if not data or 'sessions' not in data:
        return {}

    sessions = data['sessions']
    total_cost = sum(session.get('total_cost', 0) for session in sessions.values())
    total_tokens = sum(session.get('total_tokens', 0) for session in sessions.values())
    total_sessions = len(sessions)

    # Count total API calls
    total_calls = sum(len(session.get('calls', [])) for session in sessions.values())

    # Extract unique questions (deduplicate by question text)
    unique_questions = set()
    for session in sessions.values():
        for call in session.get('calls', []):
            metadata = call.get('metadata', {})
            if 'question' in metadata:
                unique_questions.add(metadata['question'])

    num_unique_questions = len(unique_questions)

    return {
        'total_cost': total_cost,
        'total_tokens': total_tokens,
        'total_sessions': total_sessions,
        'total_calls': total_calls,
        'unique_questions': num_unique_questions,
        'avg_cost_per_question': total_cost / num_unique_questions if num_unique_questions > 0 else 0,
        'avg_cost_per_session': total_cost / total_sessions if total_sessions > 0 else 0,
        'avg_tokens_per_call': total_tokens / total_calls if total_calls > 0 else 0
    }


def create_sessions_dataframe(data):
    """Create a DataFrame from sessions data for visualization."""
    if not data or 'sessions' not in data:
        return pd.DataFrame()

    sessions_list = []
    for session_id, session in data['sessions'].items():
        for call in session.get('calls', []):
            sessions_list.append({
                'session_id': session_id,
                'timestamp': call.get('timestamp'),
                'model': call.get('model'),
                'call_type': call.get('call_type'),
                'page_path': call.get('page_path'),
                'total_cost': call.get('total_cost', 0),
                'input_tokens': call.get('input_tokens', 0),
                'output_tokens': call.get('output_tokens', 0),
                'total_tokens': call.get('total_tokens', 0),
                'question': call.get('metadata', {}).get('question', 'N/A'),
                'response': call.get('metadata', {}).get('response', 'N/A')
            })

    df = pd.DataFrame(sessions_list)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

    return df


# Layout with improved UI/UX
layout = dmc.Container(
    [
        # Hero Header Section with gradient background
        dmc.Box(
            children=[
                dmc.Group(
                    [
                        dmc.ThemeIcon(
                            DashIconify(icon="tabler:chart-line", width=32),
                            size=60,
                            radius="md",
                            variant="gradient",
                            gradient={"from": "blue", "to": "cyan", "deg": 45}
                        ),
                        dmc.Stack(
                            [
                                dmc.Title("API Analytics Dashboard", order=1, size="h2"),
                                dmc.Text(
                                    "Track API usage, costs, and user interactions in real-time",
                                    size="lg",
                                    c="dimmed"
                                ),
                            ],
                            gap="xs"
                        )
                    ],
                    gap="lg"
                ),
                dmc.Group(
                    [
                        dmc.Badge(
                            [
                                DashIconify(icon="tabler:refresh", width=14, style={"marginRight": "4px"}),
                                "Auto-refresh: 30s"
                            ],
                            size="lg",
                            variant="light",
                            color="blue",
                            radius="md"
                        ),
                        dmc.Badge(
                            html.Span(id="last-updated-badge"),
                            size="lg",
                            variant="dot",
                            color="green",
                            radius="md"
                        )
                    ],
                    gap="sm"
                )
            ],
            p="xl",
            mb="xl",
            style={
                "background": "light-dark(linear-gradient(135deg, var(--mantine-color-indigo-0) 0%, var(--mantine-color-cyan-0) 100%), linear-gradient(135deg, var(--mantine-color-dark-7) 0%, var(--mantine-color-dark-6) 100%))",
                "borderRadius": "var(--mantine-radius-lg)",
                "border": "1px solid light-dark(var(--mantine-color-indigo-2), var(--mantine-color-dark-4))"
            }
        ),

        # Auto-refresh interval
        dcc.Interval(
            id='analytics-refresh-interval',
            interval=30*1000,  # Refresh every 30 seconds
            n_intervals=0
        ),

        # Summary Cards with improved design
        html.Div(id='analytics-summary-cards'),

        # Charts Section with better spacing
        dmc.Stack(
            [
                # Top row: Cost and Tokens charts
                dmc.SimpleGrid(
                    cols={"base": 1, "md": 2},
                    spacing="xl",
                    children=[
                        # Cost Over Time Chart
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:trending-up", width=24, color="var(--mantine-color-blue-6)"),
                                                        dmc.Title("Cost Over Time", order=3, size="h4"),
                                                    ],
                                                    gap="sm"
                                                ),
                                                dmc.Text("Daily API spending trends", size="sm", c="dimmed"),
                                                ],
                                            gap=0
                                        ),
                                    ],
                                    mb="md"
                                ),
                                html.Div(id='cost-over-time-chart')
                            ],
                            p="xl",
                            withBorder=True,
                            radius="lg",
                            shadow="sm"
                        ),

                        # Tokens Usage Chart
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:database", width=24, color="var(--mantine-color-violet-6)"),
                                                        dmc.Title("Token Usage", order=3, size="h4"),
                                                    ],
                                                    gap="sm"
                                                ),
                                                dmc.Text("Input and output token consumption", size="sm", c="dimmed"),
                                            ],
                                            gap=0
                                        ),
                                    ],
                                    mb="md"
                                ),
                                html.Div(id='tokens-chart')
                            ],
                            p="xl",
                            withBorder=True,
                            radius="lg",
                            shadow="sm"
                        ),
                    ]
                ),

                # Bottom row: Model and Page distribution
                dmc.SimpleGrid(
                    cols={"base": 1, "md": 2},
                    spacing="xl",
                    children=[
                        # Call Type Distribution Chart
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:api", width=24, color="var(--mantine-color-indigo-6)"),
                                                        dmc.Title("Cost by API Call Type", order=3, size="h4"),
                                                    ],
                                                    gap="sm"
                                                ),
                                                dmc.Text("Breakdown by response generation, code formatting, section suggestions", size="sm", c="dimmed"),
                                            ],
                                            gap=0
                                        ),
                                    ],
                                    mb="md"
                                ),
                                html.Div(id='model-distribution-chart')
                            ],
                            p="xl",
                            withBorder=True,
                            radius="lg",
                            shadow="sm"
                        ),

                        # Page Usage Chart
                        dmc.Paper(
                            [
                                dmc.Group(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:file-analytics", width=24, color="var(--mantine-color-pink-6)"),
                                                        dmc.Title("Cost by Page", order=3, size="h4"),
                                                    ],
                                                    gap="sm"
                                                ),
                                                dmc.Text("Top 10 pages by API costs", size="sm", c="dimmed"),
                                            ],
                                            gap=0
                                        ),
                                    ],
                                    mb="md"
                                ),
                                html.Div(id='page-usage-chart')
                            ],
                            p="xl",
                            withBorder=True,
                            radius="lg",
                            shadow="sm"
                        ),
                    ]
                ),

                # Recent Questions Table
                dmc.Paper(
                    [
                        dmc.Group(
                            [
                                dmc.Stack(
                                    [
                                        dmc.Group(
                                            [
                                                DashIconify(icon="tabler:messages", width=28, color="var(--mantine-color-indigo-6)"),
                                                dmc.Title("All User Questions", order=3, size="h4"),
                                            ],
                                            gap="sm"
                                        ),
                                        dmc.Text("Complete history of AI chat interactions (click row for details)", size="sm", c="dimmed"),
                                    ],
                                    gap=0
                                ),
                                html.Div(id='questions-count-badge')
                            ],
                            justify="space-between",
                            mb="lg"
                        ),
                        html.Div(id='recent-questions-table')
                    ],
                    p="xl",
                    withBorder=True,
                    radius="lg",
                    shadow="sm"
                ),
            ],
            gap="xl",
            mt="xl"
        ),

        # Modal for question details
        dmc.Modal(
            id="question-detail-modal",
            title="Chat Interaction Details",
            size="xl",
            opened=False,
            children=[
                dmc.Stack(
                    [
                        html.Div(id="modal-question-content"),
                        html.Div(id="modal-response-content"),
                    ],
                    gap="lg"
                )
            ],
        ),
    ],
    size="xl",
    py="xl"
)


@callback(
    Output('analytics-summary-cards', 'children'),
    Output('cost-over-time-chart', 'children'),
    Output('tokens-chart', 'children'),
    Output('model-distribution-chart', 'children'),
    Output('page-usage-chart', 'children'),
    Output('recent-questions-table', 'children'),
    Output('questions-count-badge', 'children'),
    Output('last-updated-badge', 'children'),
    Input('analytics-refresh-interval', 'n_intervals'),
    Input('color-scheme-storage', 'data')
)
def update_analytics(n_intervals, theme):
    """Update all analytics visualizations with enhanced UI/UX."""
    # Load data
    data = load_api_data()

    # Format last updated time
    last_updated = datetime.now().strftime("%I:%M:%S %p")

    if not data:
        # Enhanced empty state
        empty_msg = dmc.Center(
            dmc.Stack(
                [
                    dmc.ThemeIcon(
                        DashIconify(icon="tabler:database-off", width=48),
                        size=100,
                        radius="xl",
                        variant="light",
                        color="gray"
                    ),
                    dmc.Text("No data available yet", size="xl", fw=600, c="dimmed"),
                    dmc.Text("Charts will appear once you start using the chat feature", size="sm", c="dimmed"),
                ],
                align="center",
                gap="md"
            ),
            py="xl"
        )

        return (
            dmc.Alert(
                children=[
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:info-circle", width=24),
                            dmc.Stack(
                                [
                                    dmc.Text("No API Usage Data Found", fw=600, size="lg"),
                                    dmc.Text(
                                        "Start using the AI chat feature on any documentation page to generate analytics. "
                                        "This dashboard will automatically update every 30 seconds.",
                                        size="sm"
                                    )
                                ],
                                gap=4
                            )
                        ],
                        gap="md",
                        align="flex-start"
                    )
                ],
                title=None,
                color="blue",
                variant="light",
                radius="md"
            ),
            empty_msg, empty_msg, empty_msg, empty_msg,
            dmc.Text("No questions logged yet", c="dimmed", ta="center", py="md"),
            dmc.Badge("Total: 0", size="lg", variant="light", color="gray", radius="md"),
            f"Updated {last_updated}"
        )

    # Calculate stats
    stats = calculate_summary_stats(data)
    df = create_sessions_dataframe(data)

    # Summary Cards
    summary_cards = dmc.SimpleGrid(
        cols={"base": 1, "sm": 2, "md": 4},
        spacing="lg",
        children=[
            dmc.Paper(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="mdi:currency-usd", width=30, color="var(--mantine-color-green-6)"),
                            dmc.Stack(
                                [
                                    dmc.Text("Total Cost", size="sm", c="dimmed"),
                                    dmc.Title(f"${stats['total_cost']:.4f}", order=3, c="green"),
                                ],
                                gap=0
                            )
                        ],
                        gap="md"
                    )
                ],
                p="md",
                withBorder=True,
                radius="md",
                className="elevation-1"
            ),
            dmc.Paper(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="mdi:message-text", width=30, color="var(--mantine-color-blue-6)"),
                            dmc.Stack(
                                [
                                    dmc.Text("User Questions", size="sm", c="dimmed"),
                                    dmc.Title(str(stats['unique_questions']), order=3, c="blue"),
                                    dmc.Text(f"Avg: ${stats['avg_cost_per_question']:.4f}/question", size="xs", c="dimmed"),
                                ],
                                gap=0
                            )
                        ],
                        gap="md"
                    )
                ],
                p="md",
                withBorder=True,
                radius="md",
                className="elevation-1"
            ),
            dmc.Paper(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="mdi:chip", width=30, color="var(--mantine-color-teal-6)"),
                            dmc.Stack(
                                [
                                    dmc.Text("Total Tokens", size="sm", c="dimmed"),
                                    dmc.Title(f"{stats['total_tokens']:,}", order=3, c="teal"),
                                ],
                                gap=0
                            )
                        ],
                        gap="md"
                    )
                ],
                p="md",
                withBorder=True,
                radius="md",
                className="elevation-1"
            ),
            dmc.Paper(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="mdi:counter", width=30, color="var(--mantine-color-orange-6)"),
                            dmc.Stack(
                                [
                                    dmc.Text("API Calls", size="sm", c="dimmed"),
                                    dmc.Title(str(stats['total_calls']), order=3, c="orange"),
                                ],
                                gap=0
                            )
                        ],
                        gap="md"
                    )
                ],
                p="md",
                withBorder=True,
                radius="md",
                className="elevation-1"
            ),
        ]
    )

    # Cost Over Time Chart
    if not df.empty:
        # Group by date and prepare data for DMC LineChart
        df_time = df.groupby(df['timestamp'].dt.date)['total_cost'].sum().reset_index()
        df_time['date_str'] = df_time['timestamp'].astype(str)

        chart_data = df_time.to_dict('records')
        for record in chart_data:
            record['date'] = record.pop('date_str')
            record['Cost'] = round(record.pop('total_cost'), 4)
            del record['timestamp']

        cost_chart = dmc.LineChart(
            h=300,
            dataKey="date",
            data=chart_data,
            series=[{"name": "Cost", "color": "blue.6"}],
            curveType="linear",
            withLegend=True,
            yAxisLabel="Cost ($)",
            xAxisLabel="Date"
        )
    else:
        cost_chart = dmc.Text("No data available", c="dimmed", ta="center", py="xl")

    # Tokens Chart
    if not df.empty:
        # Aggregate tokens by timestamp and prepare data for stacked bar chart
        df_tokens = df.groupby(df['timestamp'].dt.date).agg({
            'input_tokens': 'sum',
            'output_tokens': 'sum'
        }).reset_index()
        df_tokens['date_str'] = df_tokens['timestamp'].astype(str)

        tokens_data = df_tokens.to_dict('records')
        for record in tokens_data:
            record['date'] = record.pop('date_str')
            record['Input'] = record.pop('input_tokens')
            record['Output'] = record.pop('output_tokens')
            del record['timestamp']

        tokens_chart = dmc.BarChart(
            h=300,
            dataKey="date",
            data=tokens_data,
            type="stacked",
            series=[
                {"name": "Input", "color": "blue.6"},
                {"name": "Output", "color": "green.6"}
            ],
            withLegend=True,
            yAxisLabel="Tokens",
            xAxisLabel="Date"
        )
    else:
        tokens_chart = dmc.Text("No data available", c="dimmed", ta="center", py="xl")

    # Call Type Distribution Chart
    if not df.empty:
        call_type_costs = df.groupby('call_type')['total_cost'].sum().reset_index()
        call_type_costs = call_type_costs.sort_values('total_cost', ascending=False)

        # Prettify call type names
        call_type_map = {
            'generate_markdown': 'Response Generation',
            'generate_code': 'Code Generation',
            'suggest_sections': 'Section Suggestions',
            'generate_format_instructions': 'Format Instructions',
            'format_code': 'Code Formatting'
        }
        call_type_costs['call_type_pretty'] = call_type_costs['call_type'].map(
            lambda x: call_type_map.get(x, x)
        )

        call_type_data = call_type_costs.to_dict('records')
        for record in call_type_data:
            record['type'] = record.pop('call_type_pretty')
            record['Cost'] = round(record.pop('total_cost'), 4)
            del record['call_type']

        model_chart = dmc.BarChart(
            h=400,
            dataKey="type",
            data=call_type_data,
            series=[{"name": "Cost", "color": "indigo.6"}],
            orientation="vertical",
            withLegend=False,
            yAxisLabel="Cost ($)",
            xAxisLabel="Call Type"
        )
    else:
        model_chart = dmc.Text("No data available", c="dimmed", ta="center", py="xl")

    # Page Usage Chart
    if not df.empty:
        page_costs = df.groupby('page_path')['total_cost'].sum().reset_index()
        page_costs = page_costs.sort_values('total_cost', ascending=False).head(10)
        page_costs['page_short'] = page_costs['page_path'].apply(
            lambda x: x.split('/')[-1] if '/' in x else x
        )

        page_data = page_costs.to_dict('records')
        for record in page_data:
            record['page'] = record.pop('page_short')
            record['Cost'] = round(record.pop('total_cost'), 4)
            del record['page_path']

        page_chart = dmc.BarChart(
            h=400,
            dataKey="page",
            data=page_data,
            series=[{"name": "Cost", "color": "violet.6"}],
            orientation="vertical",
            withLegend=False,
            yAxisLabel="Cost ($)",
            xAxisLabel="Page"
        )
    else:
        page_chart = dmc.Text("No data available", c="dimmed", ta="center", py="xl")

    # Recent Questions Table (grouped by question to show combined costs)
    if not df.empty:
        questions_df = df[df['question'] != 'N/A'].copy()

        # Group by question, page, and timestamp to aggregate all API calls for each question
        grouped = questions_df.groupby(['question', 'page_path', pd.Grouper(key='timestamp', freq='1min')]).agg({
            'total_cost': 'sum',
            'total_tokens': 'sum',
            'model': 'first',  # Get first model used
            'call_type': lambda x: ', '.join(sorted(set(x))),  # List unique call types
            'response': 'first'  # Get the first response (they should be the same for grouped questions)
        }).reset_index()  # IMPORTANT: reset_index() to make grouped columns regular columns

        # Sort by timestamp descending (newest first)
        recent_df = grouped.sort_values('timestamp', ascending=False).copy()
        recent_df['cost_display'] = recent_df['total_cost'].apply(lambda x: f"${x:.4f}")
        recent_df['timestamp_display'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

        # Count number of API calls per question
        call_counts = questions_df.groupby(['question', 'page_path', pd.Grouper(key='timestamp', freq='1min')]).size().reset_index(name='num_calls')

        # Merge call counts into recent_df
        recent_df = recent_df.merge(
            call_counts[['question', 'page_path', 'num_calls']],
            on=['question', 'page_path'],
            how='left'
        )
        recent_df['num_calls'] = recent_df['num_calls'].fillna(0).astype(int)

        # Create count badge
        total_questions = len(recent_df)
        count_badge = dmc.Badge(
            f"Total: {total_questions}",
            size="lg",
            variant="light",
            color="indigo",
            radius="md"
        )

        # Prepare data for AG Grid
        grid_data = recent_df.to_dict('records')

        # Column definitions with enhanced formatting and information
        column_defs = [
            {
                "field": "timestamp_display",
                "headerName": "Time",
                "width": 150,
                "pinned": "left",
                "cellStyle": {"fontWeight": 500}
            },
            {
                "field": "question",
                "headerName": "Question",
                "width": 400,
                "wrapText": True,
                "autoHeight": True,
                "cellStyle": {"lineHeight": "1.5", "paddingTop": "8px", "paddingBottom": "8px"}
            },
            {
                "field": "model",
                "headerName": "Model",
                "width": 180,
                "cellStyle": {"fontFamily": "monospace", "fontSize": "0.9em"}
            },
            {
                "field": "call_type",
                "headerName": "Call Types",
                "width": 220,
                "wrapText": True,
                "autoHeight": True,
                "cellStyle": {"fontSize": "0.85em", "color": "var(--mantine-color-dimmed)"}
            },
            {
                "field": "num_calls",
                "headerName": "API Calls",
                "width": 120,
                "type": "numericColumn",
                "cellStyle": {
                    "textAlign": "center",
                    "fontWeight": 600,
                    "color": "var(--mantine-color-orange-6)"
                }
            },
            {
                "field": "total_cost",
                "headerName": "Total Cost",
                "width": 130,
                "type": "numericColumn",
                "valueFormatter": {"function": "d3.format('$,.4f')(params.value)"},
                "cellStyle": {
                    "fontWeight": 700,
                    "color": "var(--mantine-color-green-6)"
                }
            },
            {
                "field": "total_tokens",
                "headerName": "Tokens",
                "width": 130,
                "type": "numericColumn",
                "valueFormatter": {"function": "d3.format(',')(params.value)"},
                "cellStyle": {
                    "fontWeight": 600,
                    "color": "var(--mantine-color-teal-6)"
                }
            },
            {
                "field": "page_path",
                "headerName": "Page Path",
                "width": 200,
                "cellStyle": {"fontSize": "0.9em"}
            }
        ]

        # Determine theme for AG Grid
        ag_theme = "ag-theme-quartz-dark" if theme == "dark" else "ag-theme-quartz"

        questions_table = dag.AgGrid(
            id="recent-questions-grid",
            rowData=grid_data,
            columnDefs=column_defs,
            columnSize="responsiveSizeToFit",
            defaultColDef={
                "resizable": True,
                "sortable": True,
                "filter": True,
                "floatingFilter": False,
            },
            dashGridOptions={
                "pagination": False,
                "domLayout": "autoHeight",
                "rowSelection": "single",
                "animateRows": True,
                "suppressCellFocus": False,
            },
            className=ag_theme,
            style={"height": "auto", "width": "100%"}
        )
    else:
        questions_table = dmc.Text("No questions logged yet", c="dimmed")
        count_badge = dmc.Badge("Total: 0", size="lg", variant="light", color="gray", radius="md")

    return summary_cards, cost_chart, tokens_chart, model_chart, page_chart, questions_table, count_badge, f"Updated {last_updated}"


# Callback to handle row selection and modal display
@callback(
    Output("question-detail-modal", "opened"),
    Output("modal-question-content", "children"),
    Output("modal-response-content", "children"),
    Input("recent-questions-grid", "selectedRows"),
    prevent_initial_call=True
)
def display_chat_details(selected_rows):
    """Display question and response in modal when row is selected."""
    if not selected_rows or len(selected_rows) == 0:
        return False, None, None

    # Get the first selected row
    row = selected_rows[0]

    question = row.get('question', 'No question available')
    response = row.get('response', 'No response available')
    timestamp = row.get('timestamp_display', 'Unknown time')
    page_path = row.get('page_path', 'Unknown page')
    model = row.get('model', 'Unknown model')
    total_cost = row.get('total_cost', 0)
    total_tokens = row.get('total_tokens', 0)

    # Create question section
    question_content = dmc.Paper(
        [
            dmc.Group(
                [
                    DashIconify(icon="tabler:user", width=24, color="var(--mantine-color-blue-6)"),
                    dmc.Title("User Question", order=4, size="h5"),
                ],
                gap="sm",
                mb="sm"
            ),
            dmc.Text(question, size="sm", style={"whiteSpace": "pre-wrap"}),
            dmc.Divider(my="md"),
            dmc.Group(
                [
                    dmc.Badge(f"Time: {timestamp}", size="sm", variant="light", color="gray"),
                    dmc.Badge(f"Page: {page_path}", size="sm", variant="light", color="indigo"),
                    dmc.Badge(f"Model: {model}", size="sm", variant="light", color="violet"),
                    dmc.Badge(f"Cost: ${total_cost:.4f}", size="sm", variant="light", color="green"),
                    dmc.Badge(f"Tokens: {total_tokens:,}", size="sm", variant="light", color="teal"),
                ],
                gap="xs"
            )
        ],
        p="md",
        withBorder=True,
        radius="md",
    )

    # Create response section
    response_content = dmc.Paper(
        [
            dmc.Group(
                [
                    DashIconify(icon="tabler:robot", width=24, color="var(--mantine-color-teal-6)"),
                    dmc.Title("AI Response", order=4, size="h5"),
                ],
                gap="sm",
                mb="sm"
            ),
            dcc.Markdown(response if response != 'N/A' else '*No response logged for this question.*', style={"whiteSpace": "pre-wrap"}),
        ],
        p="md",
        withBorder=True,
        radius="md",
    )

    return True, question_content, response_content