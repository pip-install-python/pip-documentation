---
name: Pannellum
description: Interactive 360° panorama viewer with tour mode, hotspots, and video support
endpoint: /pip/dash_pannellum
package: dash_pannellum
icon: solar:panorama-outline
---

.. toc::

.. llms_copy::Pannellum

`dash-pannellum` is a Dash component library that integrates the Pannellum panorama viewer into your Dash applications. It allows you to display interactive 360° panoramas, including equirectangular images, cube maps, and 360° videos. The component features tour mode with multiple scenes and hotspots, customizable camera controls, multi-resolution panorama support, and keyboard navigation for an immersive viewing experience.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash_pannellum)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-pannellum
```

---

### Quick Start

Display an interactive 360° equirectangular panorama with camera controls and adjustable viewing parameters.

.. exec::docs.dash_pannellum.simple
    :code: false

.. sourcetabs::docs/dash_pannellum/simple.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Basic Panorama

Create a simple panorama viewer with basic configuration.

.. exec::docs.dash_pannellum.basic
    :code: false

.. sourcetabs::docs/dash_pannellum/basic.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Tour Mode

Tour mode enables navigation between multiple connected panorama scenes with interactive hotspots. Users can click hotspots to jump between different viewpoints, creating an immersive multi-scene experience.

.. exec::docs.dash_pannellum.tours
    :code: false

.. sourcetabs::docs/dash_pannellum/tours.py
    :defaultExpanded: false
    :withExpandedButton: true

**Tour Configuration:**

Each tour consists of a `default` object and a `scenes` dictionary:

- **`default.firstScene`**: ID of the initial scene to display
- **`default.sceneFadeDuration`**: Transition duration in milliseconds between scenes
- **`scenes`**: Dictionary of scene configurations, each with its own panorama and hotspots

**Hotspot Configuration:**

- `pitch`: Vertical position in degrees
- `yaw`: Horizontal position in degrees
- `type`: `"scene"` for scene navigation hotspots
- `text`: Tooltip text displayed on hover
- `sceneId`: Target scene ID to navigate to
- `targetYaw` (optional): Camera yaw after transition
- `targetPitch` (optional): Camera pitch after transition

---

### Partial Panorama

Display panoramas that don't cover the full 360° horizontally or 180° vertically by specifying viewing extents using horizontal angle of view (haov), vertical angle of view (vaov), and vertical offset (vOffset).

.. exec::docs.dash_pannellum.partial_panorama
    :code: false

.. sourcetabs::docs/dash_pannellum/partial_panorama.py
    :defaultExpanded: false
    :withExpandedButton: true

**Viewing Parameters:**

- **`haov`**: Horizontal angle of view in degrees (e.g., 149.87)
- **`vaov`**: Vertical angle of view in degrees (e.g., 54.15)
- **`vOffset`**: Vertical offset in degrees, useful when panorama is not vertically centered (e.g., 1.17)

These parameters allow precise control over which portion of the panorama is visible and how it's framed within the viewer.

---

### 360° Video Panorama

Display interactive 360° video content with standard video controls.

.. exec::docs.dash_pannellum.video
    :code: false

.. sourcetabs::docs/dash_pannellum/video.py
    :defaultExpanded: false
    :withExpandedButton: true

**Video Configuration:**

- **`sources`**: Array of video source objects with `src` (URL) and `type` (MIME type)
- **`poster`**: URL to poster image displayed before video loads

The component supports standard HTML5 video formats. Users can interact with the video using typical video controls while maintaining the ability to pan around the 360° view.

---

### Using Callbacks

Track the viewer's current state (camera position, loaded status, active scene) using Dash callbacks. The component provides read-only properties that update as the user interacts with the panorama.

```python
from dash import callback, Input, Output

@callback(
    Output('output-div', 'children'),
    Input('panorama', 'loaded'),
    Input('panorama', 'pitch'),
    Input('panorama', 'yaw'),
    Input('panorama', 'currentScene')
)
def update_output(loaded, pitch, yaw, current_scene):
    """Display current panorama state"""
    if loaded and pitch is not None and yaw is not None:
        return f'Scene: {current_scene}, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°'
    return 'Loading panorama...'
```

**Available Callback Properties:**

- **`loaded`**: Boolean indicating if panorama has finished loading
- **`pitch`**: Current vertical camera angle (-90° to 90°)
- **`yaw`**: Current horizontal camera angle (-180° to 180°)
- **`currentScene`**: ID of the active scene in tour mode

---

### Keyboard Controls

The component supports keyboard navigation for improved user experience:

- **Arrow Keys**: Pan the view (←→ horizontal, ↑↓ vertical)
- **Shift**: Zoom in
- **Control/Ctrl**: Zoom out
- **F**: Toggle fullscreen mode

---

### Component Properties

| Property           | Type        | Default      | Description                                                                                                     |
| :----------------- | :---------- | :----------- | :-------------------------------------------------------------------------------------------------------------- |
| **`id`**           | `string`    | **Required** | Unique identifier for the component used in Dash callbacks.                                                     |
| `width`            | `string`    | `'100%'`     | Width of the panorama viewer (CSS value, e.g., '100%', '800px').                                                |
| `height`           | `string`    | `'400px'`    | Height of the panorama viewer (CSS value, e.g., '400px', '100vh').                                              |
| `tour`             | `dict`      | `None`       | Configuration object for tour mode with scenes and hotspots. Contains `default` and `scenes` keys.              |
| `multiRes`         | `dict`      | `None`       | Configuration object for multi-resolution panoramas. Requires `basePath`, `path`, `extension`, etc.             |
| `video`            | `dict`      | `None`       | Configuration object for 360° video playback. Requires `sources` array with video URLs and types.               |
| `showCenterDot`    | `bool`      | `False`      | If true, displays a center dot in the panorama viewer for orientation reference.                                |
| `autoLoad`         | `bool`      | `True`       | If true, the panorama loads automatically. If false, user must click to load.                                   |
| `pitch`            | `number`    | (read-only)  | Current vertical rotation angle of the camera in degrees (-90 to 90).                                           |
| `yaw`              | `number`    | (read-only)  | Current horizontal rotation angle of the camera in degrees (-180 to 180).                                       |
| `currentScene`     | `string`    | (read-only)  | ID of the currently active scene in tour mode.                                                                  |
| `loaded`           | `bool`      | (read-only)  | Indicates whether the panorama has finished loading.                                                            |
| `setProps`         | `func`      | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`    | `object`    | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

**Multi-Resolution Configuration:**

When using `multiRes` for high-quality panoramas, the configuration requires:

- `basePath`: Base URL path to tile directory
- `path`: Tile path pattern (e.g., `"/%l/%s%y_%x"`)
- `fallbackPath`: Fallback path for missing tiles
- `extension`: Image file extension (e.g., `"jpg"`)
- `tileResolution`: Resolution of each tile in pixels
- `maxLevel`: Maximum zoom level available
- `cubeResolution`: Total resolution of cube faces

---

### Contributing

Contributions to dash-pannellum are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.