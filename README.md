# CreaTech PW02 — Image Composition Engine

Project developed as part of **Computer Science Workshop 2 — Image Composition Engine**.

The goal of the project is to generate a final image from a JSON configuration file. The configuration describes the image layers, the filters applied to each layer, their parameters, the blending mode used between layers, and each layer's opacity.

The engine loads the images, applies filters in order, blends the layers, and saves the final composition in `src/output/`.

---

## Features

The engine supports:

- image loading and saving with Pillow;
- image processing with NumPy arrays;
- ordered filter pipelines on each layer;
- RGB filtering while preserving the alpha channel;
- multiple blending modes;
- per-layer opacity;
- automatic filter and blend-mode registration;
- JSON configuration validation;
- clear errors for invalid configurations, unknown filters or blend modes, missing images, invalid filter parameters, and incompatible layer dimensions;
- layer context in processing errors (`Layer 1: ...`, `Layer 2: ...`, etc.);
- automatic output numbering to avoid overwriting previous results;
- custom static effects such as glitch, chromatic aberration, radial blur, lens distortion, neon glow, and soap bubbles.

---

## Technologies

- **Python >= 3.14**
- **NumPy**
- **Pillow**
- **SciPy**
- **uv**
- **Git / GitHub**

---

## Project structure

```text
CreaTech_PW02_Image_Composition_Engine/
├── src/
│   ├── blending_modes/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── normal.py
│   │   ├── multiply.py
│   │   └── lighten.py
│   │
│   ├── filters/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── blur.py
│   │   ├── brightness.py
│   │   ├── contrast.py
│   │   ├── grayscale.py
│   │   ├── sepia.py
│   │   ├── gaussian_blur.py
│   │   ├── mean_blur.py
│   │   ├── pixelate.py
│   │   ├── chromatic.py
│   │   ├── hue.py
│   │   ├── glitch.py
│   │   ├── split_screen.py
│   │   ├── radial_blur.py
│   │   ├── bulge.py
│   │   ├── pinch.py
│   │   ├── lens_circle.py
│   │   ├── neon_glow.py
│   │   └── bubble_pop.py
│   │
│   ├── images/
│   │   ├── 0_photo.jpg
│   │   ├── 1_pop_bike.png
│   │   ├── 2_wall.png
│   │   └── 3_shiny_car.png
│   │
│   ├── output/
│   ├── config.json
│   ├── config.py
│   ├── engine.py
│   ├── image_io.py
│   └── main.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

### Main responsibilities

- `main.py` — parses command-line arguments, loads the configuration, runs the engine, and saves the final image.
- `config.py` — loads and validates the JSON configuration.
- `engine.py` — executes the composition pipeline, applies filters, checks layer dimensions, and blends layers.
- `image_io.py` — loads images as RGBA NumPy arrays and saves processed arrays back to image files.
- `filters/` — contains the filter base classes, filter registry, and filter implementations.
- `blending_modes/` — contains the blend-mode base class, registry, and blend implementations.
- `images/` — contains the source images used by the example configuration.
- `output/` — contains generated compositions.

---

## Installation

The project uses `uv` to manage the Python environment and dependencies.

From the project root:

```powershell
uv sync
```

This creates or updates the virtual environment and installs the dependencies defined in `pyproject.toml`.

---

## Running the project

From the project root:

```powershell
uv run python src/main.py
```

By default, the program loads:

```text
src/config.json
```

and saves the result inside:

```text
src/output/
```

If the default output name already exists, the program automatically chooses the next available filename:

```text
output.png
output1.png
output2.png
output3.png
...
```

### Use another configuration file

```powershell
uv run python src/main.py my_config.json
```

Relative configuration paths are resolved from the `src/` directory.

### Choose an explicit output filename

```powershell
uv run python src/main.py -o result.png
```

Both options can be combined:

```powershell
uv run python src/main.py my_config.json -o result.png
```

---

## JSON configuration

The configuration must be a JSON object containing a non-empty `layers` list.

Each layer contains:

- `image`: the source image filename;
- `filters`: an ordered list of filters;
- `blend`: the blending mode used when the layer is placed over the current result;
- `opacity`: the opacity of the layer, between `0.0` and `1.0`.

The first layer is used as the backdrop, so its `blend` and `opacity` values are not needed.

### Current example

```json
{
  "layers": [
    {
      "image": "0_photo.jpg",
      "filters": [
        {
          "name": "contrast",
          "params": {
            "level": 1.35
          }
        },
        {
          "name": "gaussianblur",
          "params": {
            "size": 10,
            "sigma": 25
          }
        },
        {
          "name": "glitch",
          "params": {
            "intensity": 0.1,
            "slices": 10
          }
        },
        {
          "name": "hue",
          "params": {
            "angle": 120
          }
        },
        {
          "name": "bubble_pop",
          "params": {
            "amount": 20,
            "average_size": 100,
            "opacity": 0.7
          }
        },
        {
          "name": "gaussianblur",
          "params": {
            "size": 5,
            "sigma": 3.5
          }
        }
      ]
    },
    {
      "image": "1_pop_bike.png",
      "filters": [
        {
          "name": "gaussianblur",
          "params": {
            "size": 25,
            "sigma": 4.2
          }
        }
      ],
      "blend": "normal",
      "opacity": 0.32
    },
    {
      "image": "2_wall.png",
      "filters": [],
      "blend": "multiply",
      "opacity": 1.0
    },
    {
      "image": "3_shiny_car.png",
      "filters": [],
      "blend": "lighten",
      "opacity": 0.35
    }
  ]
}
```

The order of the layers and the order of the filters are both significant.

---

## Available filters

| Filter name | Parameters | Description |
|---|---|---|
| `brightness` | `level` | Adds or removes brightness from the RGB values |
| `contrast` | `level` | Adjusts image contrast |
| `grayscale` | — | Converts the image to grayscale while keeping three RGB channels |
| `sepia` | — | Applies a sepia color transformation |
| `gaussianblur` | `size`, `sigma=1.0` | Applies Gaussian blur using a convolution kernel |
| `meanblur` | `size` | Applies mean blur using a convolution kernel |
| `pixelate` | `size` | Replaces blocks of pixels with their average color |
| `chromatic` | `intensity=1.0` | Creates chromatic aberration by shifting the red and blue channels |
| `hue` | `angle` | Rotates the image hue by an angle in degrees |
| `glitch` | `intensity=1.0`, `slices=10` | Randomly shifts horizontal slices of the image |
| `split_screen` | `splits=2` | Repeats the image in a grid |
| `radial_blur` | `intensity=0.1`, `samples=10` | Creates a blur directed toward the image center |
| `bulge` | `intensity=0.5` | Applies an outward distortion around the image center |
| `pinch` | `intensity=0.5` | Applies the opposite distortion of `bulge` |
| `lens_circle` | `intensity=0.5`, `radius=0.3` | Creates a circular magnifying-lens effect |
| `neon_glow` | `intensity=0.7`, `radius=8.0` | Adds a soft glow around bright areas |
| `bubble_pop` | `amount=20`, `average_size=100`, `opacity=0.5` | Adds randomly positioned, differently sized soap-bubble effects |

### Combining filters

Several filters can be combined instead of creating a new filter for every possible effect.

For example, a chromatic-glitch effect can be created by applying `glitch` followed by `chromatic`:

```json
[
  {
    "name": "glitch",
    "params": {
      "intensity": 0.5,
      "slices": 15
    }
  },
  {
    "name": "chromatic",
    "params": {
      "intensity": 0.8
    }
  }
]
```

---

## Blending modes

Three blending modes are currently implemented:

| Mode | Description |
|---|---|
| `normal` | Uses the source layer normally before alpha and opacity compositing |
| `multiply` | Multiplies source and backdrop RGB values, producing a darker result |
| `lighten` | Keeps the brighter value for each RGB channel |

Blend opacity must be between `0.0` and `1.0`.

The blending system supports RGB and RGBA arrays and performs alpha compositing automatically.

---

## Filter contract

Every filter inherits from the common abstract `Filter` class and exposes:

```python
def apply(self, image: np.ndarray) -> np.ndarray:
    ...
```

Filters receive an RGB NumPy array and return the processed RGB NumPy array.

The engine separates the RGB channels from the alpha channel before applying filters and restores the original alpha channel before blending.

Images are processed as floating-point values, generally in the range `[0.0, 1.0]`. Final clipping is handled when the image is converted for saving, although some effects may also clip their own result when required by their implementation.

---

## Automatic registries

### Filters

Concrete `Filter` subclasses register themselves automatically through `Filter.__init_subclass__()`.

The `filters` package automatically imports the modules in its directory, so adding a new filter does not require modifying the engine logic.

Example:

```python
import numpy as np

from .base import Filter


class MyFilter(Filter):
    """Apply an example custom effect."""

    name = "my_filter"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the custom effect."""
        return np.array(image, copy=True)
```

The filter can then be used directly from JSON:

```json
{
  "name": "my_filter",
  "params": {}
}
```

### Blending modes

Blending modes use the same principle through `BaseBlend.registry`.

A concrete blend mode defines a `name` and implements its `_blend()` formula. Validation, opacity, alpha compositing, and dtype conversion are handled by `BaseBlend`.

---

## Error handling and validation

The project validates the JSON configuration before running the image pipeline.

Handled cases include:

- invalid JSON;
- missing or empty `layers`;
- invalid layer structures;
- missing image or filter fields;
- invalid `params` objects;
- invalid opacity values;
- unknown filters;
- unknown blending modes;
- invalid filter parameters;
- missing or unreadable images;
- incompatible layer dimensions;
- output save errors.

Processing errors are enriched with the layer number when relevant.

Example:

```text
Error : Layer 2: Unknown filter 'unknown_filter'. Available: [...]
```

---

## Image I/O

Images are loaded with Pillow and converted to RGBA arrays with shape:

```text
(height, width, 4)
```

Pixel values are converted from `0–255` integers to floating-point values by dividing by `255`.

When saving, values are clipped to `[0.0, 1.0]` and converted back to `uint8`.

JPEG output is automatically converted from RGBA to RGB because JPEG does not support transparency.

---

## Architecture

The project separates the main responsibilities of the application:

```text
JSON configuration
       ↓
Configuration validation
       ↓
Image loading
       ↓
Layer preparation
       ↓
Ordered filter pipeline
       ↓
Blend mode + opacity + alpha compositing
       ↓
Final image
       ↓
Output file
```

`BlendEngine` now only contains the methods required by the current pipeline:

```text
run_pipeline()
_prepare_layer()
```

Unused legacy engine methods were removed to keep the class focused on its current responsibility.

---

## Adding a new filter

Create a new Python file in `src/filters/` and define a class that inherits from `Filter`.

Example:

```python
import numpy as np

from .base import Filter


class Invert(Filter):
    """Invert the colors of an RGB image."""

    name = "invert"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply color inversion."""
        return 1.0 - image
```

No change to the engine processing logic is required.

This design also makes it easier to exchange filters between projects that respect the same `Filter.apply()` contract.

---

## Git workflow

The project was developed using Git and GitHub with commits representing meaningful development steps.

The additional static filters were developed on the dedicated branch:

```text
feature/new-filters
```

They were then merged into `main` through a Pull Request.

Final cleanup work included:

- removing obsolete engine methods;
- adding layer-aware processing errors;
- removing the obsolete YAML configuration from version control;
- translating the remaining error message to English;
- harmonizing docstrings across the project.

---

## Educational goals

This project applies several concepts introduced during the workshop:

- image manipulation with NumPy and Pillow;
- convolution and blur filters;
- inheritance and abstract classes;
- Strategy Pattern;
- class registries;
- JSON configuration;
- separation of responsibilities;
- error handling;
- teamwork with Git and GitHub;
- shared interfaces between projects.

The goal is not only to generate a final image, but to build an engine that is **readable, extensible, and maintainable**.
