---
name: Dock
description: Dynamic dock window management and layout system with resizable, draggable, and floatable panels.
endpoint: /pip/dash_dock
package: dash_dock
icon: tabler:layout-sidebar-right-collapse
---

.. toc::

.. llms_copy::Dock

`dash-dock` is a Dash component library that provides a powerful window management and layout system for your Dash applications. Based on FlexLayout, it features dockable, resizable, and floatable windows with drag-and-drop tab management, maximize, minimize, and pop-out window controls, flexible row and column layouts with nested containers, custom headers and styling for individual tabs, persistent layout state management, and compatibility with both Dash 2 and Dash 3. Available in free (3 tabs) and premium (unlimited tabs) versions.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash-dock)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-dock
```

---

### Quick Start

Create a basic dockable layout with two tabs. Drag tabs to rearrange, resize panels, or float them as separate windows.

.. exec::docs.dash_dock.simple_usage
    :code: false

.. sourcetabs::docs/dash_dock/simple_usage.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Layout Configuration

The dock layout is defined using a FlexLayout model configuration object. This determines the initial structure of your dock layout.

**Basic Layout Structure:**

```python
dock_config = {
    "global": {
        "tabEnableClose": True,      # Allow closing tabs
        "tabEnableFloat": True,      # Allow floating tabs
        "tabEnableRename": False,    # Disable tab renaming
    },
    "layout": {
        "type": "row",               # Top-level container type
        "children": [
            {
                "type": "tabset",    # Container for tabs
                "children": [
                    {
                        "type": "tab",
                        "name": "Dashboard",
                        "component": "dashboard",
                        "id": "tab-dashboard",
                    }
                ]
            },
            {
                "type": "tabset",
                "children": [
                    {
                        "type": "tab",
                        "name": "Analytics",
                        "component": "analytics",
                        "id": "tab-analytics",
                    }
                ]
            }
        ]
    }
}
```

**Layout Types:**

- **`row`**: Arranges children horizontally
- **`tabset`**: Container for tabs with tab bar
- **`tab`**: Individual tab with content
- **`col`**: Arranges children vertically (alternative to row)

---

### Tab Components

Each tab requires a corresponding `Tab` component that defines the content to display when that tab is active.

```python
import dash_dock
from dash import html

tab_components = [
    dash_dock.Tab(
        id="tab-dashboard",
        children=[
            html.H3("Dashboard"),
            html.P("Main dashboard content here"),
        ]
    ),
    dash_dock.Tab(
        id="tab-analytics",
        children=[
            html.H3("Analytics"),
            html.P("Analytics content here"),
        ]
    )
]
```

**Important:** The `id` in the Tab component must match the `id` in the layout configuration.

---

### Complete Example

Combine the layout configuration and tab components in a full application.

```python
from dash import Dash, html
import dash_dock
import dash_mantine_components as dmc

app = Dash(__name__)

# Define layout structure
dock_config = {
    "global": {
        "tabEnableClose": False,
        "tabEnableFloat": True
    },
    "layout": {
        "type": "row",
        "children": [
            {
                "type": "tabset",
                "weight": 60,  # Takes 60% of width
                "children": [
                    {
                        "type": "tab",
                        "name": "Main View",
                        "component": "main",
                        "id": "tab-main",
                    }
                ]
            },
            {
                "type": "tabset",
                "weight": 40,  # Takes 40% of width
                "children": [
                    {
                        "type": "tab",
                        "name": "Sidebar",
                        "component": "sidebar",
                        "id": "tab-sidebar",
                    }
                ]
            }
        ]
    }
}

# Create tab content
tab_components = [
    dash_dock.Tab(
        id="tab-main",
        children=[html.H3("Main Content")]
    ),
    dash_dock.Tab(
        id="tab-sidebar",
        children=[html.H3("Sidebar Content")]
    )
]

# App layout
app.layout = dmc.Box(
    dash_dock.DashDock(
        id='dock-layout',
        model=dock_config,
        children=tab_components,
        useStateForModel=True,
        style={
            'position': 'relative',
            'height': '100%',
            'width': '100%',
            'overflow': 'hidden'
        }
    ),
    style={
        'height': '100vh',
        'width': '100%',
        'position': 'relative',
        'overflow': 'hidden'
    }
)

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Global Configuration Options

Control default behaviors for all tabs using the `global` object in your model configuration.

```python
"global": {
    "tabEnableClose": True,          # Show close button on tabs
    "tabEnableFloat": True,          # Allow tabs to float as windows
    "tabEnableRename": False,        # Disable tab renaming
    "tabEnableDrag": True,           # Allow dragging tabs to reorder
    "tabSetEnableMaximize": True,    # Show maximize button on tabsets
    "tabSetEnableDrop": True,        # Allow dropping tabs into tabsets
    "borderBarSize": 30,             # Size of splitter bars in pixels
    "tabSetMinWidth": 100,           # Minimum width of tabsets
    "tabSetMinHeight": 100,          # Minimum height of tabsets
}
```

---

### Nested Layouts

Create complex layouts by nesting rows and columns within each other.

```python
dock_config = {
    "global": {
        "tabEnableClose": False,
        "tabEnableFloat": True
    },
    "layout": {
        "type": "row",
        "children": [
            # Left column with stacked tabs
            {
                "type": "col",
                "weight": 30,
                "children": [
                    {
                        "type": "tabset",
                        "weight": 50,
                        "children": [
                            {
                                "type": "tab",
                                "name": "Files",
                                "id": "tab-files"
                            }
                        ]
                    },
                    {
                        "type": "tabset",
                        "weight": 50,
                        "children": [
                            {
                                "type": "tab",
                                "name": "Outline",
                                "id": "tab-outline"
                            }
                        ]
                    }
                ]
            },
            # Right side with main content
            {
                "type": "tabset",
                "weight": 70,
                "children": [
                    {
                        "type": "tab",
                        "name": "Editor",
                        "id": "tab-editor"
                    }
                ]
            }
        ]
    }
}
```

**Weight System:**

The `weight` property determines the relative size of containers. In the example above, the left column takes 30% (30/(30+70)) and the right takes 70% of the width.

---

### Premium Version with API Key

The premium version removes the 3-tab limitation and provides unlimited tabs for complex applications.

.. exec::docs.dash_dock.api_example
    :code: false

.. sourcetabs::docs/dash_dock/api_example.py
    :defaultExpanded: false
    :withExpandedButton: true

**Obtaining an API Key:**

Visit [Plotly Pro Shop](https://plotly.pro/product/prod_SY2s0MuBRidQ1q) to purchase an API key for the premium version. API keys are delivered to the purchase email within 24 hours.

**Using the API Key:**

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    apiKey=API_KEY,  # Enable premium features
)
```

**Premium Features:**

- **Unlimited Tabs**: No restriction on the number of tabs
- **Advanced Layouts**: Create complex multi-panel applications
- **Full Feature Access**: All dock management capabilities enabled

---

### Styling and Customization

Customize the appearance of tabs using the `font` property and individual tab styles.

```python
dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    font={
        'size': '14px',
        'family': 'Inter, sans-serif',
        'weight': '500'
    },
    style={
        'position': 'relative',
        'height': '100%',
        'width': '100%',
        'overflow': 'hidden',
        'backgroundColor': '#f5f5f5'
    }
)
```

**Tab-Specific Styling:**

Add custom classes or styles through the tab configuration for individual tab appearance customization.

---

### State Management

Control whether the dock layout manages its own state internally or uses external state.

```python
dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    useStateForModel=True,  # Internal state management
)
```

**State Options:**

- **`useStateForModel=True`**: Component manages layout state internally (recommended for most cases)
- **`useStateForModel=False`**: Layout state controlled externally via callbacks (advanced use cases)

---

### Pop-out Windows

Enable tabs to open in separate browser windows for multi-monitor setups.

```python
dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    supportsPopout=True,
    popoutURL='/popout',  # URL path for popout windows
)
```

**Note:** Pop-out windows open the content in a new browser window that can be moved to a different monitor.

---

### Realtime Resize

Enable real-time content resizing as panels are dragged (may impact performance with complex content).

```python
dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    realtimeResize=True,  # Update content size during drag
)
```

**Performance Consideration:**

Set to `False` (default) for better performance. Content will resize after drag completes.

---

### Component Properties

#### DashDock Component

| Property            | Type      | Default      | Description                                                                                                     |
| :------------------ | :-------- | :----------- |:----------------------------------------------------------------------------------------------------------------|
| **`id`**            | `string`  | **Required** | Unique identifier for the component used in Dash callbacks.                                                     |
| **`model`**         | `dict`    | **Required** | FlexLayout model configuration defining the layout structure, global settings, and tab configurations.          |
| **`children`**      | `list`    | **Required** | Array of Tab components to render in the dock layout. Each Tab's id must match a tab id in the model.          |
| `headers`           | `dict`    | `None`       | Custom header components for tabs. Keys are tab IDs, values are React components.                               |
| `useStateForModel`  | `bool`    | `False`      | If true, component manages layout state internally. If false, state is controlled externally.                   |
| `font`              | `dict`    | `None`       | Font styling object for tabs with size, family, and weight properties.                                          |
| `supportsPopout`    | `bool`    | `False`      | If true, enables pop-out window functionality for tabs.                                                         |
| `popoutURL`         | `string`  | `None`       | URL path for pop-out windows. Required if supportsPopout is true.                                               |
| `realtimeResize`    | `bool`    | `False`      | If true, updates content size in real-time during drag operations. May impact performance.                      |
| `apiKey`            | `string`  | `None`       | API key for premium features. Enables unlimited tabs (free version limited to 3).                               |
| `freeTabLimit`      | `number`  | `3`          | Maximum number of tabs allowed in free version. Only applies when apiKey is not provided.                       |
| `debugMode`         | `bool`    | `False`      | If true, enables debug logging to console for troubleshooting.                                                  |
| `style`             | `dict`    | `{}`         | CSS styles object for the dock container. Recommended to set position, height, width, and overflow.             |
| `setProps`          | `func`    | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`     | `object`  | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

#### Tab Component

| Property         | Type     | Default      | Description                                                                                                     |
| :--------------- | :------- | :----------- |:----------------------------------------------------------------------------------------------------------------|
| **`id`**         | `string` | **Required** | Unique identifier that must match the tab id in the DashDock model configuration.                               |
| `children`       | `list`   | `[]`         | React components to render inside this tab when it is active.                                                   |
| `setProps`       | `func`   | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`  | `object` | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

---

### FlexLayout Model Reference

The `model` property accepts a FlexLayout configuration object with the following structure:

**Global Configuration:**

```python
"global": {
    "tabEnableClose": bool,          # Allow closing tabs
    "tabEnableFloat": bool,          # Allow floating tabs as windows
    "tabEnableRename": bool,         # Allow renaming tabs
    "tabEnableDrag": bool,           # Allow dragging tabs to reorder
    "tabSetEnableMaximize": bool,    # Show maximize button
    "tabSetEnableDrop": bool,        # Allow dropping tabs
    "borderBarSize": number,         # Splitter bar size in pixels
    "tabSetMinWidth": number,        # Minimum tabset width
    "tabSetMinHeight": number,       # Minimum tabset height
}
```

**Layout Structure:**

```python
"layout": {
    "type": "row" | "col",           # Container orientation
    "weight": number,                 # Relative size (optional)
    "children": [                     # Child elements
        {
            "type": "tabset",         # Tab container
            "weight": number,         # Relative size
            "children": [
                {
                    "type": "tab",    # Individual tab
                    "name": string,   # Display name
                    "id": string,     # Unique identifier
                    "component": string  # Component reference
                }
            ]
        }
    ]
}
```

---

### Free vs Premium Comparison

| Feature                    | Free Version | Premium Version |
|:---------------------------|:-------------|:----------------|
| Maximum Tabs               | 3            | Unlimited       |
| Dockable Windows           | ✅           | ✅              |
| Resizable Panels           | ✅           | ✅              |
| Drag & Drop Tabs           | ✅           | ✅              |
| Float Windows              | ✅           | ✅              |
| Pop-out Windows            | ✅           | ✅              |
| Nested Layouts             | ✅           | ✅              |
| Custom Styling             | ✅           | ✅              |
| API Key Required           | ❌           | ✅              |
| Commercial Use             | ✅           | ✅              |

---

### Contributing

Contributions to dash-dock are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is created under [Pip Install Python LLC](https://pip-install-python.com) and licensed under the MIT License.