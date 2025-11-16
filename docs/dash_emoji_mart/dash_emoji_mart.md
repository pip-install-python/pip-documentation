---
name: Emoji Mart
description: Modern emoji picker component with custom emojis, themes, and extensive customization options.
endpoint: /pip/dash_emoji_mart
package: dash_emoji_mart
icon: fluent:emoji-meme-16-filled
---

.. toc::

.. llms_copy::Emoji Mart

`dash-emoji-mart` is a Dash component library that provides a modern, feature-rich emoji picker for your Dash applications. Based on the popular Emoji Mart library, it features native emoji support, multiple emoji sets (Apple, Google, Twitter, Facebook), custom emojis with GIF/SVG support, theme customization, internationalization in 20+ languages, and extensive configuration options for appearance and behavior.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash_emoji_mart)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-emoji-mart
```

---

### Quick Start

Display a basic emoji picker with default settings. Click an emoji to select it.

.. exec::docs.dash_emoji_mart.introduction
    :code: false

.. sourcetabs::docs/dash_emoji_mart/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom Emojis

Add custom emojis to the picker by providing an array of emoji configurations. Custom emojis support multiple skin tones and can use GIFs or SVGs as sources.

```python
from dash import Dash, html, callback, Input, Output
import dash_mantine_components as dmc
from dash_emoji_mart import DashEmojiMart

custom_emojis = [
    {
        'id': 'custom',
        'name': 'Custom',
        'emojis': [
            {
                'id': 'party_parrot',
                'name': 'Party Parrot',
                'short_names': ['party_parrot'],
                'keywords': ['dance', 'dancing'],
                'skins': [{'src': '/assets/party_parrot.gif'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'plotly',
                'name': 'Plotly',
                'short_names': ['plotly'],
                'keywords': ['plotly', 'dash'],
                'skins': [{'src': 'https://example.com/plotly-logo.png'}],
                'native': '',
                'unified': 'custom',
            },
        ],
    },
]

app = Dash(__name__)

app.layout = dmc.Container([
    DashEmojiMart(
        id='emoji-picker',
        custom=custom_emojis,
    ),
    html.Div(id='selected-emoji')
])

@callback(
    Output('selected-emoji', 'children'),
    Input('emoji-picker', 'value')
)
def display_emoji(emoji_data):
    if emoji_data:
        return f"Selected: {emoji_data.get('native', emoji_data.get('src', ''))}"
    return "No emoji selected"
```

**Custom Emoji Structure:**

- **`id`**: Unique identifier for the emoji
- **`name`**: Display name
- **`short_names`**: Array of shortcode names
- **`keywords`**: Array of search keywords
- **`skins`**: Array of skin tone variations with `src` URL
- **`native`**: Native emoji character (empty string for custom)
- **`unified`**: Unicode representation (use 'custom' for custom emojis)

---

### Custom Category Icons

Customize category icons by providing an object with category names as keys and icon definitions as values. Icons can be SVG strings or image URLs.

```python
from dash_emoji_mart import DashEmojiMart

DashEmojiMart(
    id='emoji-picker',
    categoryIcons={
        'activity': {
            'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512">...</svg>'
        },
        'people': {
            'src': 'https://example.com/people-icon.png'
        },
        'custom': {
            'svg': '<svg xmlns="http://www.w3.org/2000/svg">...</svg>'
        }
    }
)
```

**Supported Icon Formats:**

- **SVG String**: Provide raw SVG markup via the `svg` key
- **Image URL**: Provide image URL via the `src` key

Icons are displayed in the category navigation bar and adapt to the current theme.

---

### Interactive Props Explorer

Explore all available properties with live controls. Adjust settings to see how they affect the emoji picker's appearance and behavior.

.. exec::docs.dash_emoji_mart.props
    :code: false

.. sourcetabs::docs/dash_emoji_mart/props.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Themes and Appearance

The emoji picker supports three theme modes that integrate seamlessly with your application's design.

**Theme Options:**

- **`auto`**: Automatically matches system preference (light/dark mode)
- **`light`**: Forces light theme regardless of system settings
- **`dark`**: Forces dark theme regardless of system settings

**Customizing Appearance:**

```python
DashEmojiMart(
    id='custom-styled-picker',
    theme='dark',
    emojiButtonRadius='8px',        # Border radius for emoji buttons
    emojiButtonSize=40,              # Size of emoji buttons in pixels
    emojiSize=28,                    # Size of emojis within buttons
    emojiButtonColors=[              # Custom hover colors
        '#FF6B6B',
        '#4ECDC4',
        '#45B7D1'
    ]
)
```

---

### Internationalization

The picker supports 20+ languages for the user interface. Change the locale to display category names, search placeholder, and other UI text in different languages.

**Supported Locales:**

`en`, `ar`, `be`, `cs`, `de`, `es`, `fa`, `fi`, `fr`, `hi`, `it`, `ja`, `ko`, `nl`, `pl`, `pt`, `ru`, `sa`, `tr`, `uk`, `vi`, `zh`

**Example:**

```python
DashEmojiMart(
    id='emoji-picker-spanish',
    locale='es',
)
```

---

### Emoji Sets

Choose from multiple emoji sets to match your application's style or target platform.

**Available Sets:**

- **`native`**: Uses system emojis (most performant, recommended)
- **`apple`**: Apple emoji style
- **`google`**: Google emoji style
- **`twitter`**: Twitter emoji style (Twemoji)
- **`facebook`**: Facebook emoji style

```python
DashEmojiMart(
    id='emoji-picker-twitter',
    set='twitter',
)
```

**Note:** Non-native sets rely on sprite sheets and may have slower initial load times.

---

### Categories and Filtering

Control which emoji categories are displayed and exclude specific emojis.

**Customizing Categories:**

```python
DashEmojiMart(
    id='emoji-picker-filtered',
    categories=['people', 'nature', 'foods'],  # Only show these categories
    exceptEmojis=['eggplant', 'peach'],        # Exclude specific emojis
    maxFrequentRows=2,                          # Limit frequently used emojis
)
```

**Available Categories:**

`frequent`, `people`, `nature`, `foods`, `activity`, `places`, `objects`, `symbols`, `flags`

The order of categories in the array determines their display order.

---

### Layout Configuration

Customize the picker's layout including navigation position, preview position, and search bar placement.

```python
DashEmojiMart(
    id='emoji-picker-layout',
    navPosition='bottom',         # 'top', 'bottom', 'none'
    previewPosition='top',        # 'top', 'bottom', 'none'
    searchPosition='static',      # 'sticky', 'static', 'none'
    perLine=12,                   # Emojis per row
    dynamicWidth=True,            # Calculate perLine based on container width
)
```

---

### Component Properties

| Property              | Type                                | Default                                    | Description                                                                                                     |
| :-------------------- | :---------------------------------- | :----------------------------------------- |:----------------------------------------------------------------------------------------------------------------|
| **`id`**              | `string`                            | **Required**                               | Unique identifier for the component used in Dash callbacks.                                                     |
| `data`                | `dict`                              | `{}`                                       | Custom emoji data object to use for the picker.                                                                 |
| `i18n`                | `dict`                              | `{}`                                       | Localization data object for custom translations.                                                               |
| `categories`          | `list`                              | `[]`                                       | Categories to show in the picker. Order is respected. Options: frequent, people, nature, foods, activity, places, objects, symbols, flags. |
| `custom`              | `list`                              | `[]`                                       | Array of custom emoji category objects.                                                                         |
| `onEmojiSelect`       | `func`                              | `None`                                     | Callback function when an emoji is selected.                                                                    |
| `onClickOutside`      | `func`                              | `None`                                     | Callback function when a click outside the picker occurs.                                                       |
| `onAddCustomEmoji`    | `func`                              | `None`                                     | Callback when Add custom emoji button is clicked. Button only displays if this callback is provided.           |
| `autoFocus`           | `bool`                              | `False`                                    | If true, automatically focuses the search input on mount.                                                       |
| `categoryIcons`       | `dict`                              | `{}`                                       | Custom category icons object with category names as keys and icon definitions (svg or src) as values.          |
| `dynamicWidth`        | `bool`                              | `False`                                    | If true, calculates perLine dynamically based on container width. When enabled, perLine is ignored.             |
| `emojiButtonColors`   | `list`                              | `[]`                                       | Array of CSS colors for emoji button hover backgrounds (e.g., #f00, pink, rgba(155,223,88,.7)).                 |
| `emojiButtonRadius`   | `string`                            | `'100%'`                                   | Border radius of emoji buttons. Accepts CSS values (e.g., 6px, 1em, 100%).                                      |
| `emojiButtonSize`     | `number`                            | `36`                                       | Size of emoji buttons in pixels.                                                                                |
| `emojiSize`           | `number`                            | `24`                                       | Size of emojis (inside buttons) in pixels.                                                                      |
| `emojiVersion`        | `number`                            | `14`                                       | Emoji data version to use. Options: 1, 2, 3, 4, 5, 11, 12, 12.1, 13, 13.1, 14.                                  |
| `exceptEmojis`        | `list`                              | `[]`                                       | Array of emoji IDs to exclude from the picker.                                                                  |
| `icons`               | `'auto'`, `'outline'`, `'solid'`    | `'auto'`                                   | Icon style for the picker. Auto uses outline with light theme and solid with dark theme.                        |
| `locale`              | `string`                            | `'en'`                                     | Locale for UI text. Options: en, ar, be, cs, de, es, fa, fi, fr, hi, it, ja, ko, nl, pl, pt, ru, sa, tr, uk, vi, zh. |
| `maxFrequentRows`     | `number`                            | `4`                                        | Maximum number of frequently used emoji rows to show. Set to 0 to disable frequent category.                    |
| `navPosition`         | `'top'`, `'bottom'`, `'none'`       | `'top'`                                    | Position of the category navigation bar.                                                                        |
| `noCountryFlags`      | `bool`                              | `False`                                    | If true, hides country flag emojis. Automatically handled on Windows (which doesn't support flags).             |
| `noResultsEmoji`      | `string`                            | `'cry'`                                    | Emoji ID to display when search returns no results.                                                             |
| `perLine`             | `number`                            | `9`                                        | Number of emojis to display per line.                                                                           |
| `previewEmoji`        | `string`                            | `'point_up'`                               | Emoji ID to show in preview when not hovering. Defaults to point_up (bottom) or point_down (top).               |
| `previewPosition`     | `'top'`, `'bottom'`, `'none'`       | `'bottom'`                                 | Position of the emoji preview section.                                                                          |
| `searchPosition`      | `'sticky'`, `'static'`, `'none'`    | `'sticky'`                                 | Position of the search input. Sticky keeps it visible while scrolling.                                          |
| `set`                 | `'native'`, `'apple'`, `'facebook'`, `'google'`, `'twitter'` | `'native'` | Emoji set to use. Native is most performant, others use sprite sheets.                                          |
| `skin`                | `number`                            | `1`                                        | Default skin tone for emojis. Range: 1-6.                                                                       |
| `skinTonePosition`    | `'preview'`, `'search'`, `'none'`   | `'preview'`                                | Position of the skin tone selector.                                                                             |
| `theme`               | `'auto'`, `'light'`, `'dark'`       | `'auto'`                                   | Color theme of the picker. Auto matches system preference.                                                      |
| `getSpritesheetURL`   | `func`                              | `None`                                     | Function that returns the sprite sheet URL for non-native emoji sets.                                           |
| `value`               | `dict`                              | (read-only)                                | Selected emoji data object returned via callbacks.                                                              |
| `setProps`            | `func`                              | (Dash Internal)                            | Callback function to update component properties.                                                               |
| `loading_state`       | `object`                            | (Dash Internal)                            | Object describing the loading state of the component or its props.                                              |

---

### Contributing

Contributions to dash-emoji-mart are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.