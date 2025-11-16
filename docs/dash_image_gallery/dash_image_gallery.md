---
name: Image Gallery
description: Responsive image gallery component with lightbox, thumbnails, fullscreen, slideshow, and touch support
endpoint: /pip/dash_image_gallery
package: dash_image_gallery
icon: ph:images-light
---

.. toc::

.. llms_copy::Image Gallery

`dash-image-gallery` is a Dash component library that provides a feature-rich, responsive image gallery with lightbox functionality. It offers extensive customization options including thumbnail navigation, fullscreen viewing, automatic slideshows, touch/swipe support, lazy loading, keyboard controls, and multiple layout configurations. Perfect for portfolios, product showcases, photo galleries, and any application requiring elegant image presentation.

### Installation

[Visit GitHub Repo](https://github.com/pip-install-python/dash_image_gallery)

⭐️ Star this component on GitHub! Stay up to date on new releases and browse the codebase.

```bash
pip install dash-image-gallery
```

---

### Quick Start

Create a basic image gallery with thumbnail navigation and fullscreen support.

.. exec::docs.dash_image_gallery.introduction
    :code: false

.. sourcetabs::docs/dash_image_gallery/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Image Configuration

Each image in the gallery is defined by an object in the `items` array. Here's the structure:

```python
items = [
    {
        'original': '/path/to/full-size-image.jpg',      # Required: Full-size image URL
        'thumbnail': '/path/to/thumbnail.jpg',           # Thumbnail image URL
        'fullscreen': '/path/to/fullscreen-image.jpg',   # Optional: High-res for fullscreen
        'originalAlt': 'Image description',              # Alt text for accessibility
        'thumbnailAlt': 'Thumbnail description',         # Thumbnail alt text
        'description': 'Caption text',                   # Image caption
        'originalTitle': 'Image title',                  # Title attribute
        'thumbnailLabel': 'Label',                       # Label displayed on thumbnail
        'originalWidth': 1920,                           # Original image width
        'originalHeight': 1080,                          # Original image height
        'thumbnailWidth': 200,                           # Thumbnail width
        'thumbnailHeight': 150,                          # Thumbnail height
    }
]
```

**Required Fields:**
- `original`: URL or path to the full-size image

**Optional Fields:**
- `thumbnail`: Thumbnail image (defaults to `original` if not provided)
- `fullscreen`: High-resolution image for fullscreen mode
- `description`: Caption text displayed below the image
- `originalAlt`, `thumbnailAlt`: Accessibility text
- Dimension fields for optimization

---

### Gallery Features

**Navigation Controls:**

The gallery provides multiple navigation methods:
- **Arrow Keys**: Navigate left/right through images
- **Navigation Arrows**: Click arrows on sides of image
- **Thumbnails**: Click thumbnail to jump to specific image
- **Bullets**: Optional bullet navigation dots
- **Touch/Swipe**: Swipe on mobile devices

**Display Modes:**

- **Fullscreen Mode**: Toggle fullscreen viewing with dedicated button
- **Slideshow Mode**: Automatic image progression with configurable interval
- **Thumbnail Positions**: Place thumbnails on top, bottom, left, or right
- **Index Display**: Show current image number (e.g., "3 / 12")

---

### Customizing Thumbnails

Control thumbnail behavior and positioning:

```python
ImageGallery(
    items=images,
    thumbnailPosition='right',      # Options: 'top', 'right', 'bottom', 'left'
    showThumbnails=True,            # Show/hide thumbnail strip
    disableThumbnailScroll=False,   # Auto-scroll to active thumbnail
    slideOnThumbnailOver=True,      # Change image on thumbnail hover
)
```

**Thumbnail Position Options:**
- `'bottom'` (default): Horizontal strip below image
- `'top'`: Horizontal strip above image
- `'right'`: Vertical strip on right side
- `'left'`: Vertical strip on left side

---

### Slideshow & Autoplay

Enable automatic slideshow with customizable timing:

```python
ImageGallery(
    items=images,
    autoPlay=True,           # Enable automatic slideshow
    slideInterval=3000,      # Time between slides (milliseconds)
    showPlayButton=True,     # Show play/pause control
    infinite=True,           # Loop back to first image
    slideDuration=450,       # Transition animation duration
)
```

---

### Performance Optimization

**Lazy Loading:**

Load images only when needed to improve initial page load:

```python
ImageGallery(
    items=images,
    lazyLoad=True,           # Enable lazy loading
    startIndex=0,            # Start at first image
)
```

**Transition Optimization:**

```python
ImageGallery(
    items=images,
    useTranslate3D=True,              # Use GPU-accelerated transitions
    slideDuration=450,                 # Smooth transition (450ms)
    swipingTransitionDuration=0,       # Instant swipe feedback
)
```

---

### Touch & Swipe Controls

Configure touch interaction behavior:

```python
ImageGallery(
    items=images,
    disableSwipe=False,            # Enable/disable image swiping
    disableThumbnailSwipe=False,   # Enable/disable thumbnail swiping
    swipeThreshold=30,             # % of width to trigger slide change
    flickThreshold=0.4,            # Velocity threshold for flick
)
```

---

### Keyboard Navigation

Control keyboard shortcuts:

```python
ImageGallery(
    items=images,
    disableKeyDown=False,      # Enable keyboard controls
    useWindowKeyDown=True,     # Listen globally vs. on element only
)
```

**Default Keyboard Shortcuts:**
- **Left Arrow**: Previous image
- **Right Arrow**: Next image
- **Esc**: Exit fullscreen
- **Space**: Play/pause slideshow (when enabled)

---

### Fullscreen Mode

Configure fullscreen viewing experience:

```python
ImageGallery(
    items=images,
    showFullscreenButton=True,    # Show fullscreen toggle
    useBrowserFullscreen=True,    # Use native browser fullscreen API
)
```

**Fullscreen Options:**
- `useBrowserFullscreen=True`: Native browser fullscreen (recommended)
- `useBrowserFullscreen=False`: CSS-based fullscreen (for compatibility)

---

### Advanced Customization

**Custom Rendering:**

Provide custom render functions for complete control:

```python
def render_custom_item(item):
    """Custom renderer for main image display"""
    return html.Div([
        html.Img(src=item['original'], className='custom-image'),
        html.P(item.get('description', ''), className='caption')
    ])

def render_custom_thumbnail(item):
    """Custom renderer for thumbnails"""
    return html.Div([
        html.Img(src=item['thumbnail']),
        html.Span(item.get('thumbnailLabel', ''))
    ])

ImageGallery(
    items=images,
    renderItem=render_custom_item,
    renderThumbInner=render_custom_thumbnail,
)
```

**Error Handling:**

Specify fallback image when loading fails:

```python
ImageGallery(
    items=images,
    onErrorImageURL='/assets/image-not-found.png',
)
```

---

### RTL Support

Enable right-to-left layout for RTL languages:

```python
ImageGallery(
    items=images,
    isRTL=True,  # Reverse navigation direction
)
```

---

### Component Properties

| Property           | Type        | Default      | Description                                                                                                     |
| :----------------- | :---------- | :----------- | :-------------------------------------------------------------------------------------------------------------- |
| **`id`**           | `string`    | **Required** | Unique identifier for the component used in Dash callbacks.                                                     |
| `items`            | `array`     | **Required** | Array of image objects. Each object requires `original` URL and can include thumbnail, alt text, etc.           |
| `infinite`         | `bool`      | `True`       | Enable infinite loop - gallery wraps from last image back to first.                                             |
| `lazyLoad`         | `bool`      | `False`      | Load images only when needed to improve performance.                                                            |
| `showNav`          | `bool`      | `True`       | Display left/right navigation arrows on the sides of images.                                                    |
| `showThumbnails`   | `bool`      | `True`       | Display thumbnail strip for quick navigation.                                                                   |
| `thumbnailPosition`| `string`    | `"bottom"`   | Position of thumbnail strip. Options: `"top"`, `"right"`, `"bottom"`, `"left"`.                                 |
| `showFullscreenButton` | `bool`  | `True`       | Display button to toggle fullscreen mode.                                                                       |
| `useBrowserFullscreen` | `bool`  | `True`       | Use native browser fullscreen API. If `False`, uses CSS-based fullscreen.                                       |
| `useTranslate3D`   | `bool`      | `True`       | Use GPU-accelerated `translate3d` transitions instead of `translate`.                                           |
| `showPlayButton`   | `bool`      | `True`       | Display play/pause button for slideshow control.                                                                |
| `isRTL`            | `bool`      | `False`      | Enable right-to-left layout and reverse navigation direction.                                                   |
| `showBullets`      | `bool`      | `False`      | Display bullet navigation dots below the image.                                                                 |
| `showIndex`        | `bool`      | `False`      | Display current image index (e.g., "3 / 12").                                                                   |
| `autoPlay`         | `bool`      | `False`      | Enable automatic slideshow on component mount.                                                                  |
| `disableThumbnailScroll` | `bool` | `False`     | Disable automatic scrolling of thumbnail container to active thumbnail.                                          |
| `disableKeyDown`   | `bool`      | `False`      | Disable keyboard navigation (arrow keys, esc).                                                                  |
| `disableSwipe`     | `bool`      | `False`      | Disable touch swipe gestures on main images.                                                                    |
| `disableThumbnailSwipe` | `bool` | `False`      | Disable touch swipe gestures on thumbnail strip.                                                                |
| `onErrorImageURL`  | `string`    | `None`       | Fallback image URL to display when an image fails to load.                                                      |
| `indexSeparator`   | `string`    | `" / "`      | Separator string for index display (e.g., "3 / 12").                                                            |
| `slideDuration`    | `number`    | `450`        | Duration of slide transition animation in milliseconds.                                                         |
| `swipingTransitionDuration` | `number` | `0`     | Transition duration while actively swiping (0 = instant feedback).                                               |
| `slideInterval`    | `number`    | `3000`       | Time between automatic slides in autoplay mode (milliseconds).                                                  |
| `slideOnThumbnailOver` | `bool`  | `False`      | Change to image when hovering over its thumbnail.                                                               |
| `flickThreshold`   | `number`    | `0.4`        | Velocity threshold for detecting a "flick" gesture (0-1 scale).                                                 |
| `swipeThreshold`   | `number`    | `30`         | Percentage of slide width that must be swiped to trigger slide change.                                          |
| `stopPropagation`  | `bool`      | `False`      | Stop event propagation for swipe events (prevents parent scrolling).                                            |
| `startIndex`       | `number`    | `0`          | Index of image to display initially (0-based).                                                                  |
| `useWindowKeyDown` | `bool`      | `True`       | Listen for keyboard events globally. If `False`, only when gallery is focused.                                  |
| `additionalClass`  | `string`    | `None`       | Additional CSS class name to apply to the gallery root element.                                                 |
| `renderItem`       | `function`  | `None`       | Custom render function for main image display. Receives item object as parameter.                               |
| `renderThumbInner` | `function`  | `None`       | Custom render function for thumbnail content. Receives item object as parameter.                                |
| `onImageError`     | `function`  | `None`       | Callback fired when main image fails to load. Receives event object.                                            |
| `onThumbnailError` | `function`  | `None`       | Callback fired when thumbnail fails to load. Receives event object.                                             |
| `onThumbnailClick` | `function`  | `None`       | Callback fired when thumbnail is clicked. Receives `(event, index)`.                                            |
| `onBulletClick`    | `function`  | `None`       | Callback fired when navigation bullet is clicked. Receives `(event, index)`.                                    |
| `onImageLoad`      | `function`  | `None`       | Callback fired when image loads successfully. Receives event object.                                            |
| `onSlide`          | `function`  | `None`       | Callback fired after slide transition completes. Receives `currentIndex`.                                       |
| `onBeforeSlide`    | `function`  | `None`       | Callback fired before slide transition starts. Receives `nextIndex`.                                            |
| `onScreenChange`   | `function`  | `None`       | Callback fired when fullscreen mode changes. Receives boolean (true = fullscreen).                              |
| `onPause`          | `function`  | `None`       | Callback fired when slideshow is paused. Receives `currentIndex`.                                               |
| `onPlay`           | `function`  | `None`       | Callback fired when slideshow starts playing. Receives `currentIndex`.                                          |
| `onClick`          | `function`  | `None`       | Callback fired when gallery is clicked. Receives event object.                                                  |
| `onTouchMove`      | `function`  | `None`       | Callback fired during touch move gesture. Receives event object.                                                |
| `onTouchEnd`       | `function`  | `None`       | Callback fired when touch gesture ends. Receives event object.                                                  |
| `onTouchStart`     | `function`  | `None`       | Callback fired when touch gesture starts. Receives event object.                                                |
| `onMouseOver`      | `function`  | `None`       | Callback fired on mouse over gallery. Receives event object.                                                    |
| `onMouseLeave`     | `function`  | `None`       | Callback fired when mouse leaves gallery. Receives event object.                                                |
| `setProps`         | `func`      | (Dash Internal) | Callback function to update component properties.                                                            |
| `loading_state`    | `object`    | (Dash Internal) | Object describing the loading state of the component or its props.                                           |

---

### Contributing

Contributions to dash-image-gallery are welcome! Please refer to the project's issues on GitHub for any feature requests or bug reports.

### License

This project is licensed under the MIT License.
