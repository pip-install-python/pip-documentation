---
name: Full Calendar
description: Interactive calendar component with multiple views, event handling, and resource scheduling powered by FullCalendar
endpoint: /pip/full_calendar_component
package: dash-fullcalendar
icon: line-md:calendar
---

.. toc::

.. llms_copy::Full Calendar

`dash-fullcalendar` is a Dash component library that wraps the powerful `@fullcalendar/react` library, bringing professional calendar and scheduling capabilities to your Dash applications. It provides interactive calendar views with drag-and-drop event management, multiple view types (month, week, day, list, timeline), resource scheduling, custom event rendering, and comprehensive callback support for building sophisticated scheduling interfaces and event management systems.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash-fullcalendar)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-fullcalendar
```

---

### Quick Start

Create an interactive calendar with basic event handling, including date clicking, event clicking, and drag-and-drop functionality.

.. exec::docs.full_calendar_component.introduction
    :code: false

.. sourcetabs::docs/full_calendar_component/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Multiple Views & Layouts

Switch between grid, list, multi-month, and Scheduler views by changing `initialView` or using navigation commands. FullCalendar supports various calendar layouts optimized for different use cases.

.. exec::docs.full_calendar_component.section_renders
    :code: false

.. sourcetabs::docs/full_calendar_component/section_renders.py
    :defaultExpanded: false
    :withExpandedButton: true

**Available Views:**

- **Month Views**: `dayGridMonth`, `multiMonthYear`
- **Week Views**: `timeGridWeek`, `dayGridWeek`
- **Day Views**: `timeGridDay`
- **List Views**: `listWeek`, `listMonth`, `listYear`
- **Resource Views**: `resourceTimeline`, `resourceTimeGrid` (requires Scheduler)

.. admonition:: Premium Scheduler plugins
    :icon: mdi:star-four-points
    :color: yellow

    Timeline and resource views require FullCalendar Scheduler. Use your commercial key or the open-source key (`GPL-My-Project-Is-Open-Source`) together with `plugins=["resourceTimeline","resourceTimeGrid","resource"]`.

---

### Header Toolbar & Navigation

Configure the calendar header with custom buttons, navigation controls, and view switchers. The header toolbar is fully customizable through the `headerToolbar` prop.

.. exec::docs.full_calendar_component.header_toolbar
    :code: false

.. sourcetabs::docs/full_calendar_component/header_toolbar.py
    :defaultExpanded: false
    :withExpandedButton: true

**Header Configuration:**

The `headerToolbar` prop accepts an object with `left`, `center`, and `right` properties. Each can contain:
- Navigation buttons: `prev`, `next`, `today`
- View switcher buttons: `dayGridMonth`, `timeGridWeek`, `timeGridDay`
- Custom buttons: defined in `customButtons` prop
- Title: `title` displays the current date range

---

### Interactive Event Management

Implement complete event management workflows with drag-and-drop, event resizing, date selection, and click handlers. This example demonstrates all interactive callback patterns.

.. exec::docs.full_calendar_component.extra_fields
    :code: false

.. sourcetabs::docs/full_calendar_component/extra_fields.py
    :defaultExpanded: false
    :withExpandedButton: true

**Interactive Callback Properties:**

- **`dateClick`**: Fires when a date/time is clicked, returns ISO datetime string
- **`select`**: Fires when date range is selected, returns `{"start": str, "end": str, "allDay": bool}`
- **`eventClick`**: Fires when event is clicked, returns complete event object
- **`eventDrop`**: Fires when event is dragged to new time/date
- **`eventResize`**: Fires when event duration is changed via resizing
- **`command`**: Input prop to programmatically control the calendar (navigate, change view, etc.)

---

### Remote Data & API Integration

Load events from REST APIs, databases, or real-time data sources. Events can be dynamically updated through Dash callbacks.

.. exec::docs.full_calendar_component.api_example
    :code: false

.. sourcetabs::docs/full_calendar_component/api_example.py
    :defaultExpanded: false
    :withExpandedButton: true

**Event Data Structure:**

Events provided to the `events` prop should follow this structure:

```python
{
    "title": "Event Title",           # Required
    "start": "2024-01-15T10:00:00",  # Required (ISO format)
    "end": "2024-01-15T12:00:00",    # Optional (ISO format)
    "allDay": False,                  # Optional (boolean)
    "color": "#3788d8",              # Optional (CSS color)
    "className": "important-event",   # Optional (CSS class)
    "extendedProps": {               # Optional (custom metadata)
        "department": "Marketing",
        "description": "Q1 Planning"
    }
}
```

---

### Working with Commands

Programmatically control the calendar using the `command` prop. Pass command dictionaries to navigate, change views, or update calendar state.

**Common Commands:**

```python
# Navigation
{"type": "next"}          # Go to next period
{"type": "prev"}          # Go to previous period
{"type": "today"}         # Go to today

# View Changes
{"type": "changeView", "view": "timeGridWeek"}
{"type": "changeView", "view": "dayGridMonth"}

# Date Navigation
{"type": "gotoDate", "date": "2024-01-15"}
```

Use these commands in callbacks to control the calendar based on user interactions or application state.

---

### Customization Options

**Business Hours:**

Define available/working hours on the calendar:

```python
businessHours={
    "daysOfWeek": [1, 2, 3, 4, 5],  # Monday - Friday
    "startTime": "09:00",
    "endTime": "17:00"
}
```

**Event Rendering:**

Customize how events appear using `eventDisplay` options:
- `"auto"`: Default display (block for all-day, list-item for timed)
- `"block"`: Display as blocks
- `"list-item"`: Display as list items
- `"background"`: Display as background events
- `"none"`: Hide the event (useful for custom rendering)

**Theming:**

The component automatically adapts to light and dark themes when integrated with Dash Mantine Components. Calendar colors and backgrounds update based on the active color scheme.

---

### Component Properties

| Property           | Type        | Default      | Description                                                                                                     |
| :----------------- | :---------- | :----------- | :-------------------------------------------------------------------------------------------------------------- |
| **`id`**           | `string`    | **Required** | Unique identifier for the component used in Dash callbacks.                                                     |
| `events`           | `list`      | `[]`         | Array of event objects to display on the calendar. Each event should have `title` and `start` properties.       |
| `initialView`      | `string`    | `"dayGridMonth"` | Initial calendar view to display. Options: `"dayGridMonth"`, `"timeGridWeek"`, `"timeGridDay"`, etc.        |
| `initialDate`      | `string`    | (today)      | Initial date to display in ISO format (e.g., `"2024-01-15"`).                                                  |
| `headerToolbar`    | `dict`      | (default)    | Configuration for header toolbar with `left`, `center`, `right` properties.                                     |
| `footerToolbar`    | `dict`      | `None`       | Configuration for footer toolbar (same structure as `headerToolbar`).                                           |
| `plugins`          | `list`      | `[]`         | Array of FullCalendar plugin names to enable (e.g., `["dayGrid", "timeGrid", "interaction"]`).                 |
| `editable`         | `bool`      | `False`      | Enable drag-and-drop and resizing for events.                                                                  |
| `selectable`       | `bool`      | `False`      | Enable date range selection by dragging across dates.                                                          |
| `selectMirror`     | `bool`      | `False`      | Show selection preview while dragging.                                                                         |
| `dayMaxEvents`     | `bool/int`  | `False`      | Maximum events per day. Use `True` for automatic calculation or number for specific limit.                      |
| `weekends`         | `bool`      | `True`       | Display weekends on the calendar.                                                                              |
| `businessHours`    | `dict`      | `None`       | Define business/working hours. Object with `daysOfWeek`, `startTime`, `endTime` properties.                     |
| `allDaySlot`       | `bool`      | `True`       | Display the all-day slot in week/day views.                                                                    |
| `slotMinTime`      | `string`    | `"00:00:00"` | Earliest time slot to display (e.g., `"08:00:00"`).                                                            |
| `slotMaxTime`      | `string`    | `"24:00:00"` | Latest time slot to display (e.g., `"18:00:00"`).                                                              |
| `slotDuration`     | `string`    | `"00:30:00"` | Duration of each time slot (e.g., `"00:15:00"` for 15-minute slots).                                           |
| `slotLabelInterval`| `string`    | (auto)       | Interval for displaying time labels (e.g., `"01:00:00"` for hourly labels).                                     |
| `snapDuration`     | `string`    | (auto)       | Granularity for event dragging/resizing (e.g., `"00:15:00"`).                                                  |
| `nowIndicator`     | `bool`      | `False`      | Display a marker for the current time in week/day views.                                                       |
| `height`           | `string/int`| `"auto"`     | Calendar height. Can be CSS value (`"600px"`, `"100%"`) or number (pixels).                                     |
| `aspectRatio`      | `number`    | `1.35`       | Width-to-height ratio when `height` is not set.                                                                |
| `eventDisplay`     | `string`    | `"auto"`     | How events are rendered. Options: `"auto"`, `"block"`, `"list-item"`, `"background"`, `"none"`.                |
| `eventColor`       | `string`    | `"#3788d8"` | Default color for events (CSS color value).                                                                     |
| `eventBackgroundColor` | `string` | (auto)       | Default background color for events.                                                                           |
| `eventBorderColor` | `string`    | (auto)       | Default border color for events.                                                                               |
| `eventTextColor`   | `string`    | (auto)       | Default text color for events.                                                                                 |
| `resources`        | `list`      | `None`       | Array of resource objects for resource scheduling (requires Scheduler plugins).                                 |
| `schedulerLicenseKey` | `string` | `None`       | License key for FullCalendar Scheduler. Use `"GPL-My-Project-Is-Open-Source"` for open-source projects.         |
| `customButtons`    | `dict`      | `None`       | Define custom toolbar buttons with click handlers.                                                            |
| `command`          | `dict`      | `None`       | Programmatic command to execute (e.g., navigation, view changes). Use in callbacks to control calendar.         |
| `dateClick`        | `string`    | (read-only)  | ISO datetime string of clicked date. Updates when user clicks a date/time.                                      |
| `select`           | `dict`      | (read-only)  | Object with `start`, `end`, `allDay` when date range is selected.                                              |
| `eventClick`       | `dict`      | (read-only)  | Complete event object when event is clicked.                                                                   |
| `eventDrop`        | `dict`      | (read-only)  | Object with `event`, `oldEvent`, `delta`, `relatedEvents` when event is dropped.                               |
| `eventResize`      | `dict`      | (read-only)  | Object with `event`, `oldEvent`, `startDelta`, `endDelta` when event is resized.                               |
| `setProps`         | `func`      | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`    | `object`    | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

**Note:** All callback properties (`dateClick`, `select`, `eventClick`, `eventDrop`, `eventResize`) are read-only and update automatically when user interactions occur. Use these as `Input` in Dash callbacks to respond to calendar events.

---

### Contributing

Contributions to dash-fullcalendar are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.
