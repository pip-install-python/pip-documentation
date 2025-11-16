---
name: Insta Stories
description: Instagram and Snapchat style stories component with video support, custom renderers, and interactive controls.
endpoint: /pip/dash_insta_stories
package: dash_insta_stories
icon: material-symbols:web-stories-outline
---

.. toc::

.. llms_copy::Insta Stories

`dash-insta-stories` is a Dash component library that brings Instagram and Snapchat-style stories to your Dash applications. It features automatic progression with customizable intervals, video and image support, custom headers and loaders, interactive navigation with tap/swipe controls, keyboard navigation, story preloading for smooth transitions, custom renderers for complex content, and responsive design with configurable dimensions.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash_insta_stories)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-insta-stories
```

---

### Quick Start

Display a basic Instagram-style story viewer with automatic progression. Tap the left or right side to navigate between stories.

.. exec::docs.dash_insta_stories.introduction
    :code: false

.. sourcetabs::docs/dash_insta_stories/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Simple Image Stories

Create a story viewer using an array of image URLs. The component automatically handles progression and provides tap controls for navigation.

```python
from dash import Dash
from dash_insta_stories import DashInstaStories

app = Dash(__name__)

stories = [
    'https://picsum.photos/400/600?image=1',
    'https://picsum.photos/400/600?image=2',
    'https://picsum.photos/400/600?image=3',
]

app.layout = DashInstaStories(
    id='simple-stories',
    stories=stories,
    width=360,
    height=640,
    defaultInterval=3000,  # 3 seconds per story
)
```

**Simple Stories Array:**

Pass an array of image URLs as strings for quick setup. Each story displays for the `defaultInterval` duration.

---

### Advanced Story Objects

Use story objects for fine-grained control over each story's appearance and behavior, including headers, custom durations, and video content.

```python
from dash_insta_stories import DashInstaStories

advanced_stories = [
    {
        'url': 'https://picsum.photos/400/600?image=10',
        'duration': 5000,  # 5 seconds
        'header': {
            'heading': 'Product Launch',
            'subheading': '2 hours ago',
            'profileImage': 'https://picsum.photos/100/100?image=20'
        }
    },
    {
        'url': 'https://example.com/video.mp4',
        'type': 'video',
        'duration': 10000,
        'header': {
            'heading': 'Behind the Scenes',
            'subheading': '5 hours ago',
            'profileImage': 'https://picsum.photos/100/100?image=21'
        }
    },
    {
        'url': 'https://picsum.photos/400/600?image=30',
        'duration': 4000,
        'seeMore': True,  # Adds "See More" button
        'header': {
            'heading': 'New Collection',
            'subheading': '1 day ago',
            'profileImage': 'https://picsum.photos/100/100?image=22'
        }
    }
]

app.layout = DashInstaStories(
    id='advanced-stories',
    stories=advanced_stories,
    width='100%',
    height='100vh',
    loop=True,  # Loop back to first story after last
)
```

**Story Object Properties:**

- **`url`**: Image or video URL (required)
- **`type`**: Set to `'video'` for video content (optional)
- **`duration`**: Custom duration in milliseconds (optional)
- **`header`**: Object with `heading`, `subheading`, and `profileImage` (optional)
- **`seeMore`**: Adds "See More" button at bottom (optional)
- **`seeMoreCollapsed`**: Custom component for collapsed state (optional)
- **`styles`**: Override default story styles (optional)
- **`preloadResource`**: Enable/disable preloading, defaults to true for images (optional)

---

### Interactive Callbacks

Track story progression and user interactions using Dash callbacks. The component provides callback properties for story events and navigation.

```python
from dash import Dash, html, callback, Input, Output
from dash_insta_stories import DashInstaStories

app = Dash(__name__)

app.layout = html.Div([
    DashInstaStories(
        id='interactive-stories',
        stories=[
            'https://picsum.photos/400/600?image=40',
            'https://picsum.photos/400/600?image=41',
            'https://picsum.photos/400/600?image=42',
        ],
        width=360,
        height=640,
    ),
    html.Div(id='story-info')
])

@callback(
    Output('story-info', 'children'),
    Input('interactive-stories', 'currentIndex'),
    prevent_initial_call=True
)
def display_story_info(current_index):
    if current_index is not None:
        return f'Currently viewing story {current_index + 1}'
    return 'No story selected'
```

**Available Callback Events:**

- **`onStoryStart`**: Triggered when a story begins
- **`onStoryEnd`**: Triggered when a story ends
- **`onAllStoriesEnd`**: Triggered when all stories complete
- **`onNext`**: Triggered when user navigates to next story
- **`onPrevious`**: Triggered when user navigates to previous story

---

### Playback Control

Control story playback programmatically using the `isPaused` and `currentIndex` properties.

```python
from dash import Dash, html, callback, Input, Output
import dash_mantine_components as dmc
from dash_insta_stories import DashInstaStories

app = Dash(__name__)

app.layout = html.Div([
    DashInstaStories(
        id='controlled-stories',
        stories=[
            'https://picsum.photos/400/600?image=50',
            'https://picsum.photos/400/600?image=51',
            'https://picsum.photos/400/600?image=52',
        ],
        width=360,
        height=640,
        isPaused=False,
        currentIndex=0,
    ),
    dmc.Group([
        dmc.Button('Pause', id='pause-btn', n_clicks=0),
        dmc.Button('Resume', id='resume-btn', n_clicks=0),
        dmc.Button('Jump to Story 3', id='jump-btn', n_clicks=0),
    ])
])

@callback(
    Output('controlled-stories', 'isPaused'),
    Input('pause-btn', 'n_clicks'),
    Input('resume-btn', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_playback(pause_clicks, resume_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id == 'pause-btn'

@callback(
    Output('controlled-stories', 'currentIndex'),
    Input('jump-btn', 'n_clicks'),
    prevent_initial_call=True
)
def jump_to_story(n_clicks):
    if n_clicks:
        return 2  # Jump to third story (0-indexed)
    return 0
```

---

### Styling and Customization

Customize the appearance of stories, progress bars, and containers using style properties.

```python
from dash_insta_stories import DashInstaStories

app.layout = DashInstaStories(
    id='styled-stories',
    stories=[
        'https://picsum.photos/400/600?image=60',
        'https://picsum.photos/400/600?image=61',
    ],
    width=400,
    height=700,
    storyContainerStyles={
        'borderRadius': '20px',
        'overflow': 'hidden',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.3)'
    },
    storyStyles={
        'objectFit': 'cover',
        'filter': 'brightness(0.95)'
    },
    progressContainerStyles={
        'padding': '10px'
    },
    progressStyles={
        'background': 'linear-gradient(to right, #667eea, #764ba2)',
        'height': '3px'
    }
)
```

**Available Style Properties:**

- **`storyContainerStyles`**: Outer container styles (border, shadow, etc.)
- **`storyStyles`**: Individual story content styles (filters, fit, etc.)
- **`progressContainerStyles`**: Container wrapping all progress bars
- **`progressWrapperStyles`**: Container for each progress bar
- **`progressStyles`**: Progress bar appearance

---

### Keyboard Navigation

Enable keyboard controls for desktop users to navigate stories using arrow keys.

```python
from dash_insta_stories import DashInstaStories

app.layout = DashInstaStories(
    id='keyboard-stories',
    stories=[
        'https://picsum.photos/400/600?image=70',
        'https://picsum.photos/400/600?image=71',
        'https://picsum.photos/400/600?image=72',
    ],
    width=360,
    height=640,
    keyboardNavigation=True,  # Enable keyboard controls
    preventDefault=False,     # Allow default browser behavior
)
```

**Keyboard Controls:**

- **Left Arrow**: Previous story
- **Right Arrow**: Next story
- **Up Arrow**: Open "See More" section (if available)
- **Escape / Down Arrow**: Close "See More" section

---

### Performance Optimization

Control story preloading to optimize performance and bandwidth usage.

```python
from dash_insta_stories import DashInstaStories

app.layout = DashInstaStories(
    id='optimized-stories',
    stories=[
        {
            'url': 'https://picsum.photos/400/600?image=80',
            'preloadResource': True  # Preload this story
        },
        {
            'url': 'https://example.com/large-video.mp4',
            'type': 'video',
            'preloadResource': False  # Don't preload video
        },
        {
            'url': 'https://picsum.photos/400/600?image=81',
            'preloadResource': True
        }
    ],
    width=360,
    height=640,
    preloadCount=2,  # Preload 2 stories ahead of current
)
```

**Preloading Options:**

- **`preloadCount`**: Number of stories to preload ahead (default: 1)
- **`preloadResource`**: Per-story preload setting (defaults: true for images, false for videos)

Images are preloaded by default for smooth transitions, while videos are not to conserve bandwidth.

---

### Component Properties

| Property                  | Type                | Default         | Description                                                                                                     |
| :------------------------ | :------------------ | :-------------- |:----------------------------------------------------------------------------------------------------------------|
| **`id`**                  | `string`            | **Required**    | Unique identifier for the component used in Dash callbacks.                                                     |
| **`stories`**             | `list`              | **Required**    | Array of image URLs (strings) or story objects with url, type, duration, header, etc.                          |
| `renderers`               | `list`              | `[]`            | Array of custom renderer objects for advanced content types.                                                    |
| `defaultInterval`         | `number`            | `1200`          | Default duration in milliseconds for which each story persists.                                                 |
| `loader`                  | `Component`         | Ripple loader   | Custom loader component displayed while story loads from URL.                                                   |
| `header`                  | `Component`         | Default header  | Custom header component displayed at top of each story. Receives header object from story data.                 |
| `storyContainerStyles`    | `dict`              | `{}`            | CSS styles object for the outer story container.                                                                |
| `width`                   | `number` or `string`| `360`           | Width of the component. Accepts numbers (pixels) or strings (e.g., '100%', '100vw', 'inherit').                 |
| `height`                  | `number` or `string`| `640`           | Height of the component. Accepts numbers (pixels) or strings (e.g., '100vh', '100%', 'inherit').                |
| `storyStyles`             | `dict`              | `{}`            | CSS styles object to override default story content styles.                                                     |
| `progressContainerStyles` | `dict`              | `{}`            | CSS styles object for the container wrapping all progress bars.                                                 |
| `progressWrapperStyles`   | `dict`              | `{}`            | CSS styles object for the container wrapping each individual progress bar.                                      |
| `progressStyles`          | `dict`              | `{}`            | CSS styles object for the progress bars themselves.                                                             |
| `loop`                    | `bool`              | `False`         | If true, loops back to first story after the last story ends.                                                   |
| `isPaused`                | `bool`              | `False`         | Controls story playback state. Set to true to pause, false to resume.                                           |
| `currentIndex`            | `number`            | `None`          | Current story index (0-based). Set this to jump to a specific story programmatically.                           |
| `onStoryStart`            | `func`              | `None`          | Callback function triggered when a story starts playing.                                                        |
| `onStoryEnd`              | `func`              | `None`          | Callback function triggered when a story finishes playing.                                                      |
| `onAllStoriesEnd`         | `func`              | `None`          | Callback function triggered when all stories in the array have completed.                                       |
| `onNext`                  | `func`              | `None`          | Callback function triggered when user navigates to the next story (tap/press right or arrow key).               |
| `onPrevious`              | `func`              | `None`          | Callback function triggered when user navigates to the previous story (tap/press left or arrow key).            |
| `keyboardNavigation`      | `bool`              | `False`         | If true, enables arrow key navigation. Also enables up arrow for "See More" and escape/down for closing.        |
| `preventDefault`          | `bool`              | `False`         | If true, disables default click behavior on the component.                                                      |
| `preloadCount`            | `number`            | `1`             | Number of stories to preload ahead of the current story index for smoother transitions.                         |
| `setProps`                | `func`              | (Dash Internal) | Callback function to update component properties.                                                               |
| `loading_state`           | `object`            | (Dash Internal) | Object describing the loading state of the component or its props.                                              |

---

### Contributing

Contributions to dash-insta-stories are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.