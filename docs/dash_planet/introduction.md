---
name: Planet
description: Interactive orbital menu component with circular satellite layout, spring animations, and premium features
endpoint: /pip/dash_planet
package: dash_planet
icon: solar:planet-4-bold
---

.. toc::

.. llms_copy::Planet

`dash-planet` is a Dash component library that provides an interactive orbital menu system for creating engaging circular navigation interfaces. It displays content elements (satellites) in a circular orbit around a central element with smooth spring-based animations. The component offers both free and premium tiers, supporting basic orbital menus with up to 3 satellites for free, and unlimited satellites with advanced features like draggable elements, semicircle layouts, and enhanced animation controls with a premium API key.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash_planet)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-planet
```

---

### Quick Start

Create a basic interactive orbital menu with a central avatar and satellite action buttons.

.. exec::docs.dash_planet.introduction
    :code: false

.. sourcetabs::docs/dash_planet/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Basic Code Example

Here's a minimal example to get started with DashPlanet:

```python
from dash import Dash
from dash_planet import DashPlanet
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__)

app.layout = DashPlanet(
    id='my-planet',
    centerContent=dmc.Avatar(
        size="lg",
        radius="xl",
        src="path/to/avatar.png"
    ),
    children=[
        dmc.ActionIcon(
            DashIconify(icon="clarity:settings-line", width=20, height=20),
            size="lg",
            variant="filled",
            id="action-icon-1",
        ),
        dmc.ActionIcon(
            DashIconify(icon="mdi:email", width=20, height=20),
            size="lg",
            variant="filled",
            id="action-icon-2",
        ),
        dmc.ActionIcon(
            DashIconify(icon="mdi:bell", width=20, height=20),
            size="lg",
            variant="filled",
            id="action-icon-3",
        ),
    ],
    orbitRadius=80,
    rotation=0,
)

if __name__ == '__main__':
    app.run_server(debug=True)
```

---

### Semicircle Menu Layout

Premium feature that displays satellites in a semicircle layout instead of full circular orbit. Perfect for creating arc-shaped menus and navigation bars.

.. exec::docs.dash_planet.semicircle_example
    :code: false

.. sourcetabs::docs/dash_planet/semicircle_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Free vs Premium Features

DashPlanet offers both free and premium tiers to suit different project needs.

| **Free Tier**                         | **Premium Features** |
|:-----------------------------------------|:----------------|
| ✓ Up to 3 satellite elements in orbit    | 🌟 Unlimited satellite elements |
| ✓ Basic orbital animation                | 🌙 Semicircle Menu layout |
| ✓ Customizable orbit radius and rotation | ⚡ Enhanced animation controls |
| ✓ Click-to-toggle functionality          | 💎 Draggable satellites and center element |
|                                          | 🎯 Bounce animations with directional control |
|                                          | 🔄 Advanced satellite orientation options |

**Get Premium Access:** [Buy DashPlanet API Key](https://plotly.pro/product/prod_SY2xOUihEmOKda)

To use premium features, provide your API key:

```python
DashPlanet(
    apiKey="your-api-key-here",
    # Premium features now available
    dragableSatellites=True,
    bounce=True,
    bounceDirection="TOP",
)
```

---

### Working with Callbacks

**Toggle Orbital Menu:**

Control the visibility of satellite elements using the `open` property and `n_clicks` callback.

```python
from dash import Input, Output, callback

@callback(
    Output("my-planet", "open"),
    Input("my-planet", "n_clicks")
)
def toggle_planet(n_clicks):
    """Toggle satellite visibility on center element click"""
    if n_clicks is None:
        return False
    return n_clicks % 2 == 1
```

**Dynamic Rotation Control:**

Update the orbital rotation angle dynamically based on user input.

```python
@callback(
    Output("my-planet", "rotation"),
    Input("rotation-slider", "value")
)
def update_rotation(value):
    """Rotate the entire orbital system"""
    return value
```

**Satellite Click Handling:**

Respond to clicks on individual satellite elements by giving each satellite a unique ID.

```python
@callback(
    Output("output-div", "children"),
    Input("satellite-1", "n_clicks"),
    Input("satellite-2", "n_clicks"),
    Input("satellite-3", "n_clicks"),
)
def handle_satellite_clicks(n1, n2, n3):
    """Handle clicks on different satellites"""
    ctx = callback_context
    if not ctx.triggered:
        return "Click a satellite"

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return f"Clicked: {button_id}"
```

---

### Customizing Satellite Elements

Satellites can be any valid Dash component, allowing for rich, interactive menu items.

**Using Icons:**

```python
from dash_iconify import DashIconify
from dash import html

satellites = [
    html.Div([
        DashIconify(
            icon="mdi:email",
            width=40,
            height=40,
            color="#3b82f6"
        )
    ], style={'width': '40px', 'height': '40px'})
    for _ in range(3)
]
```

**Using Mantine Components:**

```python
import dash_mantine_components as dmc

satellites = [
    dmc.ActionIcon(
        dmc.ThemeIcon(DashIconify(icon="mdi:home")),
        size="lg",
        variant="filled",
        color="blue",
    ),
    dmc.ActionIcon(
        dmc.ThemeIcon(DashIconify(icon="mdi:settings")),
        size="lg",
        variant="filled",
        color="green",
    ),
]
```

---

### Animation Controls

Fine-tune the spring physics animation using `mass`, `tension`, and `friction` properties.

```python
DashPlanet(
    mass=4,           # Higher mass = slower, heavier animation
    tension=500,      # Higher tension = stiffer spring, faster animation
    friction=19,      # Higher friction = more damping, less bounce
)
```

**Animation Parameter Guide:**

- **`mass`**: Controls the "weight" of the animation (default: 1)
  - Lower values (0.5-1): Light, quick animations
  - Higher values (2-5): Heavy, slower animations

- **`tension`**: Controls spring stiffness (default: 500)
  - Lower values (100-300): Looser, more elastic
  - Higher values (500-1000): Tighter, snappier

- **`friction`**: Controls damping/resistance (default: 17)
  - Lower values (5-15): More bouncy, oscillating
  - Higher values (20-30): Smoother, more damped

---

### Styling and Appearance

**Component Styling:**

Apply custom styles to the container using the `style` prop:

```python
DashPlanet(
    style={
        'backgroundColor': '#f8f9fa',
        'borderRadius': '50%',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'padding': '20px',
    }
)
```

**Hiding the Orbit Line:**

Toggle the visibility of the orbital path line:

```python
DashPlanet(
    hideOrbit=True,  # Hide the circular orbit line
)
```

**Satellite Orientation (Premium):**

Control how satellites rotate as they orbit:

- **`DEFAULT`**: No rotation, satellites maintain upright position
- **`INSIDE`**: Satellites face toward the center
- **`OUTSIDE`**: Satellites face away from the center
- **`READABLE`**: Satellites rotate to remain readable (top half upright, bottom half inverted)

```python
DashPlanet(
    apiKey="your-key",
    satelliteOrientation="READABLE",
)
```

---

### Browser Support

DashPlanet is compatible with modern browsers that support CSS transforms and React Spring animations:

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

**Minimum Requirements:**
- `dash` ≥ 2.0.0
- `react` ≥ 18.3.1

---

### Component Properties

| Property           | Type        | Default      | Description                                                                                                     |
| :----------------- | :---------- | :----------- | :-------------------------------------------------------------------------------------------------------------- |
| **`id`**           | `string`    | **Required** | Unique identifier for the component used in Dash callbacks.                                                     |
| `centerContent`    | `node`      | `None`       | Content displayed in the center of the orbit (e.g., avatar, button, icon).                                      |
| `children`         | `node`      | `None`       | Satellite elements to be displayed in orbit around the center. Can be any valid Dash components.                |
| `open`             | `bool`      | `False`      | Controls visibility of satellite elements. Set to `True` to show satellites, `False` to hide.                   |
| `orbitRadius`      | `number`    | `120`        | Radius of the orbit in pixels. Determines how far satellites are from the center.                               |
| `rotation`         | `number`    | `0`          | Initial rotation angle of the orbital system in degrees. Use to offset starting positions.                      |
| `hideOrbit`        | `bool`      | `False`      | If `True`, hides the circular orbit line. Satellites still orbit, but the path is invisible.                    |
| `mass`             | `number`    | `1`          | Mass parameter for spring physics animation. Higher values create heavier, slower animations.                   |
| `tension`          | `number`    | `500`        | Spring tension parameter. Higher values create stiffer, faster animations.                                      |
| `friction`         | `number`    | `17`         | Spring friction parameter. Higher values create more damping and reduce bounce.                                 |
| `style`            | `dict`      | `{}`         | Standard CSS styles to apply to the component container.                                                        |
| `className`        | `string`    | `None`       | CSS class name to apply to the component container.                                                            |
| `n_clicks`         | `number`    | `0`          | Number of times the center element has been clicked. Updates automatically on click.                            |
| `apiKey`           | `string`    | `None`       | API key for unlocking premium features. Purchase at [plotly.pro](https://plotly.pro/product/prod_SY2xOUihEmOKda) |
| `dragablePlanet`   | `bool`      | `False`      | **(Premium)** Enable dragging of the center element. Requires valid `apiKey`.                                   |
| `dragableSatellites` | `bool`    | `False`      | **(Premium)** Enable dragging of satellite elements. Requires valid `apiKey`.                                   |
| `bounce`           | `bool`      | `False`      | **(Premium)** Enable bounce animation effect. Requires valid `apiKey`.                                          |
| `bounceDirection`  | `string`    | `"TOP"`      | **(Premium)** Direction of bounce animation. Options: `"TOP"`, `"BOTTOM"`, `"LEFT"`, `"RIGHT"`. Requires `apiKey`. |
| `satelliteOrientation` | `string` | `"DEFAULT"` | **(Premium)** How satellites rotate in orbit. Options: `"DEFAULT"`, `"INSIDE"`, `"OUTSIDE"`, `"READABLE"`. Requires `apiKey`. |
| `setProps`         | `func`      | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`    | `object`    | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

**Note:** Premium features marked with **(Premium)** require a valid API key. Free tier is limited to 3 satellite elements maximum.

---

### Contributing

Contributions to dash-planet are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.