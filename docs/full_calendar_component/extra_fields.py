from datetime import datetime, timedelta

import dash_fullcalendar as dcal
import dash_mantine_components as dmc
from dash import Input, Output, callback, callback_context, html, no_update
from dash.exceptions import PreventUpdate

BUSINESS_HOURS = [
    {"daysOfWeek": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00"},
]

CARD_STYLE = {
    "backgroundColor": "var(--mantine-color-dark-6)",
    "border": "1px solid var(--mantine-color-dark-4)",
    "color": "var(--mantine-color-gray-0)",
}

FIELDSET_STYLES = {
    "root": {
        **CARD_STYLE,
        "borderRadius": "var(--mantine-radius-md)",
        "padding": "var(--mantine-spacing-lg)",
    }
}

ALERT_STYLES = {"root": {"color": "var(--mantine-color-dark-9)"}}

DARK_CALENDAR_STYLE = {
    "--fc-page-bg-color": "#101113",
    "--fc-neutral-bg-color": "#1a1b1e",
    "--fc-neutral-text-color": "#f1f3f5",
    "--fc-border-color": "#2c2e33",
    "--fc-button-text-color": "#f1f3f5",
    "--fc-button-bg-color": "#2c2e33",
    "--fc-button-border-color": "#373a40",
    "--fc-event-text-color": "#f8f9fa",
}

LIGHT_CALENDAR_STYLE = {
    "--fc-page-bg-color": "#ffffff",
    "--fc-neutral-bg-color": "#f8f9fa",
    "--fc-neutral-text-color": "#212529",
    "--fc-border-color": "#dee2e6",
    "--fc-button-text-color": "#495057",
    "--fc-button-bg-color": "#f8f9fa",
    "--fc-button-border-color": "#dee2e6",
    "--fc-event-text-color": "#212529",
}


def _slot(day_offset, hour, duration, title, color, context):
    day = datetime.now().date() + timedelta(days=day_offset)
    start = datetime.combine(day, datetime.min.time()) + timedelta(hours=hour)
    end = start + timedelta(hours=duration)
    return {
        "id": title.lower().replace(" ", "-"),
        "title": title,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "className": color,
        "extendedProps": {"context": context},
    }


ADVANCED_EVENTS = [
    _slot(0, 9, 1, "Stand-up", "bg-gradient-primary", "Daily scrum and blockers."),
    _slot(0, 13, 1, "Pairing Session", "bg-gradient-info", "Mob pairing on the dashboard."),
    _slot(1, 11, 1.5, "Customer Demo", "bg-gradient-success", "Demo latest release to customers."),
    _slot(2, 15, 2, "Deep Work", "bg-gradient-warning", "Heads-down time for migration tasks."),
    _slot(3, 20, 1, "Deploy", "bg-gradient-danger", "Blue/green switch-over."),
]


component = dmc.Container(
    dmc.Grid(
        gutter={"base": "md", "sm": "lg", "lg": "xl"},
        children=[
            dmc.GridCol(
                dmc.Paper(
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    dmc.Button("Prev", id="advanced-command-prev", variant="light", size="compact-sm"),
                                    dmc.Button("Today", id="advanced-command-today", size="compact-sm"),
                                    dmc.Button("Next", id="advanced-command-next", variant="light", size="compact-sm"),
                                ],
                                justify="center",
                                gap="xs",
                            ),
                            html.Div(
                                dcal.FullCalendar(
                                    id="advanced-calendar",
                                    initialView="timeGridWeek",
                                    events=ADVANCED_EVENTS,
                                    selectable=True,
                                    selectMirror=True,
                                    editable=True,
                                    eventDurationEditable=True,
                                    weekends=True,
                                    businessHours=BUSINESS_HOURS,
                                    nowIndicator=True,
                                    height="780px",
                                ),
                                id="advanced-calendar-wrapper",
                                className="dark-calendar",
                            ),
                        ],
                        gap="md",
                    ),
                    radius="md",
                    withBorder=True,
                    p={"base": "sm", "sm": "md", "lg": "xl"},
                    style=CARD_STYLE,
                ),
                span={"base": 12, "lg": 8},
            ),
            dmc.GridCol(
                dmc.Paper(
                    dmc.Stack(
                        [
                            dmc.Fieldset(
                                legend="Toggle calendar behavior",
                                children=dmc.Stack(
                                    [
                                        dmc.Switch(label="Show weekends", id="toggle-weekends", checked=True, color="indigo"),
                                        dmc.Switch(label="Enforce business hours", id="toggle-business-hours", checked=True, color="indigo"),
                                        dmc.Switch(label="Allow dragging/resizing", id="toggle-editable", checked=True, color="indigo"),
                                        dmc.Switch(label="Allow range selection", id="toggle-selectable", checked=True, color="indigo"),
                                    ],
                                    gap="xs",
                                ),
                                styles=FIELDSET_STYLES,
                            ),
                            dmc.Divider(label="Live activity", variant="dashed"),
                            dmc.Alert(
                                "Click a date to capture quick notes.",
                                id="calendar-click-output",
                                color="indigo",
                                variant="light",
                                radius="md",
                                styles=ALERT_STYLES,
                            ),
                            dmc.Alert(
                                "Select a range to schedule a block.",
                                id="calendar-select-output",
                                color="teal",
                                variant="light",
                                radius="md",
                                styles=ALERT_STYLES,
                            ),
                            dmc.Alert(
                                "Move or resize an event to see the payload.",
                                id="calendar-mutation-output",
                                color="yellow",
                                variant="light",
                                radius="md",
                                styles=ALERT_STYLES,
                            ),
                        ],
                        gap="md",
                    ),
                    radius="md",
                    withBorder=True,
                    p={"base": "sm", "sm": "md", "lg": "xl"},
                    style=CARD_STYLE,
                ),
                span={"base": 12, "lg": 4},
            ),
        ],
    ),
    fluid=True,
    px={"base": "xs", "sm": "md"},
    py={"base": "md", "sm": "xl"},
)


@callback(
    Output("advanced-calendar", "command"),
    Input("advanced-command-prev", "n_clicks"),
    Input("advanced-command-today", "n_clicks"),
    Input("advanced-command-next", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_calendar(prev_clicks, today_clicks, next_clicks):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    mapping = {
        "advanced-command-prev": "prev",
        "advanced-command-today": "today",
        "advanced-command-next": "next",
    }
    return {"type": mapping.get(trigger, "today")}


@callback(
    Output("advanced-calendar", "weekends"),
    Output("advanced-calendar", "businessHours"),
    Output("advanced-calendar", "editable"),
    Output("advanced-calendar", "selectable"),
    Input("toggle-weekends", "checked"),
    Input("toggle-business-hours", "checked"),
    Input("toggle-editable", "checked"),
    Input("toggle-selectable", "checked"),
)
def tune_calendar(weekends, business_hours, editable, selectable):
    return (
        bool(weekends),
        BUSINESS_HOURS if business_hours else False,
        bool(editable),
        bool(selectable),
    )


@callback(
    Output("calendar-click-output", "children"),
    Output("calendar-select-output", "children"),
    Output("calendar-mutation-output", "children"),
    Input("advanced-calendar", "dateClick"),
    Input("advanced-calendar", "select"),
    Input("advanced-calendar", "eventDrop"),
    Input("advanced-calendar", "eventResize"),
    Input("advanced-calendar", "eventClick"),
    prevent_initial_call=True,
)
def surface_activity(date_click, selection, event_drop, event_resize, event_click):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    prop_id = ctx.triggered[0]["prop_id"]
    click_msg = no_update
    select_msg = no_update
    mutation_msg = no_update

    if prop_id == "advanced-calendar.dateClick" and date_click:
        click_msg = f"You clicked {date_click}."
    elif prop_id == "advanced-calendar.select" and selection:
        select_msg = f"Selected {selection['start']} → {selection['end']}."
    elif prop_id == "advanced-calendar.eventDrop" and event_drop:
        delta = event_drop["delta"]
        click_delta = delta.get("days", 0) or delta.get("milliseconds", 0) / (1000 * 60 * 60 * 24)
        mutation_msg = f"Moved {event_drop['event']['title']} by {click_delta:.1f} day(s)."
    elif prop_id == "advanced-calendar.eventResize" and event_resize:
        delta = event_resize["delta"]
        hours = delta.get("milliseconds", 0) / (1000 * 60 * 60)
        mutation_msg = f"Extended {event_resize['event']['title']} by {hours:.1f} hour(s)."
    elif prop_id == "advanced-calendar.eventClick" and event_click:
        context = (event_click.get("extendedProps") or {}).get("context", "No notes attached.")
        mutation_msg = f"{event_click.get('title', 'Event')}: {context}"

    return click_msg, select_msg, mutation_msg


@callback(
    Output("advanced-calendar-wrapper", "style"),
    Input("color-scheme-storage", "data"),
)
def update_calendar_theme(theme):
    """Update calendar styling based on color scheme"""
    return DARK_CALENDAR_STYLE if theme == "dark" else LIGHT_CALENDAR_STYLE
