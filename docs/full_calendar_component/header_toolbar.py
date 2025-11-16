from datetime import datetime, timedelta

import dash_fullcalendar as dcal
import dash_mantine_components as dmc
from dash import Input, Output, callback, html

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

BASE_HEADER_CHOICES = [
    {"value": "title", "label": "Title"},
    {"value": "prev", "label": "Prev"},
    {"value": "next", "label": "Next"},
    {"value": "prevYear", "label": "Prev Year"},
    {"value": "today", "label": "Today"},
    {"value": "dayGridMonth", "label": "dayGridMonth"},
    {"value": "timeGridWeek", "label": "timeGridWeek"},
    {"value": "timeGridDay", "label": "timeGridDay"},
    {"value": "listWeek", "label": "listWeek"},
    {"value": "listDay", "label": "listDay"},
    {"value": "multiMonthYear", "label": "multiMonthYear"},
]

HAS_RESOURCE_API = "resources" in getattr(dcal.FullCalendar, "available_properties", [])

PREMIUM_CHOICES = [
    {"value": "resourceTimelineWeek", "label": "resourceTimelineWeek*"},
    {"value": "resourceTimeGridDay", "label": "resourceTimeGridDay*"},
]

HEADER_CHOICES = BASE_HEADER_CHOICES + (PREMIUM_CHOICES if HAS_RESOURCE_API else [])
PREMIUM_KEYS = {choice["value"] for choice in PREMIUM_CHOICES} if HAS_RESOURCE_API else set()

RESOURCES = [
    {"id": "room-1", "title": "Room 101"},
    {"id": "room-2", "title": "Room 202"},
    {"id": "hybrid", "title": "Remote Crew"},
]


def _demo_events():
    base_day = datetime.now().date()

    def block(title, day_offset, hour, duration, resource, color, context):
        start = datetime.combine(base_day + timedelta(days=day_offset), datetime.min.time()) + timedelta(hours=hour)
        end = start + timedelta(hours=duration)
        event = {
            "title": title,
            "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
            "className": color,
            "extendedProps": {"context": context},
        }
        if resource:
            event["resourceId"] = resource
        return event

    return [
        block("Roadmap sync", 0, 10, 1.5, "room-1", "bg-gradient-success", "Company-wide goals alignment."),
        block("Design pairing", 1, 13, 1, "room-2", "bg-gradient-info", "Working session with design."),
        block("Support rotation", 1, 16, 2, "hybrid", "bg-gradient-warning", "Handling premium support tickets."),
        block("Deploy", 3, 21, 1.5, "room-1", "bg-gradient-danger", "Nightly deployment window."),
    ]


component = dmc.Container(
    dmc.Grid(
        gutter={"base": "md", "sm": "lg", "lg": "xl"},
        children=[
            dmc.GridCol(
                dmc.Paper(
                    html.Div(id="view-fcc-2"),
                    id="intro-wrapper-fcc-2",
                    withBorder=True,
                    radius="md",
                    p={"base": "sm", "sm": "md", "lg": "lg"},
                ),
                span={"base": 12, "lg": 9},
            ),
            dmc.GridCol(
                dmc.Paper(
                    dmc.Stack(
                        [
                            dmc.MultiSelect(
                                label="Left of the headerToolbar",
                                placeholder="Pick buttons",
                                id="fcc-headerToolbar-left-muti-select",
                                value=["prev", "today", "next"],
                                data=HEADER_CHOICES,
                            ),
                            dmc.MultiSelect(
                                label="Center of the headerToolbar",
                                placeholder="Pick buttons",
                                id="fcc-headerToolbar-center-muti-select",
                                value=["title"],
                                data=HEADER_CHOICES,
                            ),
                            dmc.MultiSelect(
                                label="Right of the headerToolbar",
                                placeholder="Pick buttons",
                                id="fcc-headerToolbar-right-muti-select",
                                value=["dayGridMonth", "timeGridWeek", "timeGridDay", "listWeek"],
                                data=HEADER_CHOICES,
                            ),
                            dmc.Text(
                                "Buttons marked with * require Scheduler plugins and a license key."
                                if HAS_RESOURCE_API
                                else "Install the Scheduler build of dash-fullcalendar to unlock resource buttons (*).",
                                size="sm",
                                c="dimmed",
                            ),
                        ],
                        gap="md",
                    ),
                    withBorder=True,
                    radius="md",
                    p={"base": "sm", "sm": "md", "lg": "lg"},
                ),
                span={"base": 12, "lg": 3},
            ),
        ],
    ),
    fluid=True,
    px={"base": "xs", "sm": "md"},
    py={"base": "md", "sm": "xl"},
)


@callback(
    Output("view-fcc-2", "children"),
    Input("fcc-headerToolbar-left-muti-select", "value"),
    Input("fcc-headerToolbar-center-muti-select", "value"),
    Input("fcc-headerToolbar-right-muti-select", "value"),
    Input("color-scheme-storage", "data"),
)
def update_form(left_buttons, center_buttons, right_buttons, theme):
    left = ",".join(left_buttons) if left_buttons else ""
    center = ",".join(center_buttons) if center_buttons else ""
    right = ",".join(right_buttons) if right_buttons else ""

    events = _demo_events()
    calendar_kwargs = {
        "id": "view-calendar-toolbar",
        "initialView": "dayGridMonth",
        "initialDate": events[0]["start"].split("T")[0],
        "headerToolbar": {"left": left, "center": center, "right": right},
        "events": events,
        "editable": True,
        "selectable": True,
        "navLinks": True,
        "nowIndicator": True,
        "height": "650px",
    }

    selected = set(left_buttons + center_buttons + right_buttons)
    if HAS_RESOURCE_API and (selected & PREMIUM_KEYS):
        calendar_kwargs.update(
            {
                "schedulerLicenseKey": "GPL-My-Project-Is-Open-Source",
                "plugins": ["resourceTimeline", "resourceTimeGrid", "resource"],
                "resources": RESOURCES,
            }
        )

    calendar_style = DARK_CALENDAR_STYLE if theme == "dark" else LIGHT_CALENDAR_STYLE

    return html.Div(
        dcal.FullCalendar(**calendar_kwargs),
        className="dark-calendar",
        style=calendar_style,
    )
