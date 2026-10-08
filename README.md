# CreaTech PW02 — Image Composition Engine

Project developed as part of the **Computer Science Workshop 2 — Image Composition Engine**.

The goal is to generate a final image from a JSON configuration file describing:

- the images used as layers;
- the filters applied to each layer;
- the parameters of each filter;
- the blending mode used between layers;
- the opacity of each layer.

The engine loads the images, applies filters in the specified order, blends the layers together, and automatically saves the final result in `src/output/`.

---

## Features

The project can:

- load images with Pillow;
- manipulate images as NumPy arrays;
- apply several filters successively to the same layer;
- preserve the alpha channel while applying RGB filters;
- blend multiple layers in the order defined by the configuration;
- control the opacity of each layer;
- use several blending modes;
- automatically load available filters and blending modes through registries;
- detect invalid configurations and display clear error messages;
- automatically generate output filenames without overwriting previous images.

---

## Technologies

- **Python 3.14**
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

### Main files

`main.py` is the program entry point. It reads command-line arguments, loads the configuration, runs the engine, and saves the result.

`config.py` loads and validates the JSON configuration.

`engine.py` runs the composition pipeline: loading layers, applying filters, and blending images.

`image_io.py` handles image loading and saving.

`filters/` contains all available image filters.

`blending_modes/` contains the available blending modes.

`images/` contains the source images used as layers.

`output/` contains the generated images.

---

## Installation

The project uses `uv` to manage the Python environment and dependencies.

From the project root:

```powershell
uv sync
```

This command creates or updates the virtual environment and installs the dependencies defined in `pyproject.toml`.

---

## Running the project

From the project root:

```powershell
uv run python src/main.py
```

By default, the program uses:

```text
src/config.json
```

and saves the result in:

```text
src/output/
```

Output files are automatically numbered so that previous images are not overwritten:

```text
output.png
output1.png
output2.png
output3.png
...
```

### Using another configuration file

```powershell
uv run python src/main.py my_config.json
```

Relative configuration paths are resolved from the `src/` directory.

### Choosing the output filename

```powershell
uv run python src/main.py -o result.png
```

Both options can also be combined:

```powershell
uv run python src/main.py my_config.json -o result.png
```

---

## JSON configuration

The configuration contains an ordered list of `layers`.

Example:

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

### Layers

Each layer can contain:

```text
image
filters
blend
opacity
```

The first layer is used as the base image. Each following layer is blended with the accumulated result.

The order of both layers and filters therefore matters.

---

## Available filters

| Filter | Main parameters | Description |
|---|---|---|
| `brightness` | `level` | Adjusts image brightness |
| `contrast` | `level` | Adjusts image contrast |
| `grayscale` | — | Converts the image to grayscale |
| `sepia` | — | Applies a sepia color effect |
| `gaussianblur` | `size`, `sigma` | Applies Gaussian blur |
| `meanblur` | `size` | Applies mean blur |
| `pixelate` | `size` | Pixelates the image using blocks |
| `chromatic` | `intensity` | Shifts color channels to create chromatic aberration |
| `hue` | `angle` | Rotates the hue of the image |
| `glitch` | `intensity`, `slices` | Randomly shifts horizontal image slices |
| `split_screen` | `splits` | Repeats the image in a grid |
| `radial_blur` | `intensity`, `samples` | Creates radial blur from the center |
| `bulge` | `intensity` | Creates an outward distortion from the center |
| `pinch` | `intensity` | Creates the opposite distortion of `bulge` |
| `lens_circle` | `intensity`, `radius` | Creates a circular lens effect |
| `neon_glow` | `intensity`, `radius` | Adds glow around bright areas |
| `bubble_pop` | `amount`, `average_size`, `opacity` | Adds soap-bubble effects with varied sizes |

Several filters can be combined on the same layer. They are applied in the order in which they appear in the `filters` list.

For example, an effect similar to a **chromatic glitch** can be created by combining:

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

Three blending modes are currently available:

| Mode | Description |
|---|---|
| `normal` | Standard layer composition |
| `multiply` | Darkens the result by multiplying color values |
| `lighten` | Keeps the lighter color components |

Each layer, except the first one, can also define an opacity:

```json
{
  "blend": "normal",
  "opacity": 0.5
}
```

Opacity must be between `0.0` and `1.0`.

---

## Automatic filter registry

All filters inherit from the common `Filter` base class.

Each subclass is automatically registered when imported. The `filters` package automatically imports the modules available in its directory.

This makes it possible to add a new filter without changing the engine logic.

Example:

```python
import numpy as np

from .base import Filter


class MyFilter(Filter):
    """Example custom filter."""

    name = "my_filter"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the custom filter."""
        return np.array(image, copy=True)
```

After adding the file to `src/filters/`, the filter can be used directly in the JSON configuration:

```json
{
  "name": "my_filter",
  "params": {}
}
```

This also makes it easier to exchange filters between projects that follow the same shared contract.

---

## Filter contract

Every filter must follow this interface:

```python
def apply(self, image: np.ndarray) -> np.ndarray:
    ...
```

Filters receive an RGB image as a `numpy.ndarray` and return a new transformed image.

The engine temporarily separates the alpha channel while filters are applied, then restores it before blending.

Images are processed as floating-point values, generally between `0.0` and `1.0`.

---

## Error handling

The program handles cases such as:

- missing or invalid configuration files;
- unreadable or missing images;
- unknown filters;
- unknown blending modes;
- invalid filter parameters;
- incompatible layer dimensions.

Expected errors are caught in `main.py` so the program can display a clear message instead of an unnecessary traceback.

---

## Architecture

The project follows a simple separation of responsibilities:

```text
Configuration
     ↓
Image loading
     ↓
Filter application
     ↓
Layer blending
     ↓
Saving the final image
```

Filters and blending modes use a **Strategy-style architecture** with registries, allowing the engine to select an implementation from the name written in the JSON configuration.

This organization makes it possible to extend the project without rewriting the main processing pipeline.

---

## Git workflow

The project was developed with Git and GitHub using commits representing meaningful development steps.

The new static filters were developed on a dedicated branch:

```text
feature/new-filters
```

and then merged into `main` through a Pull Request.

This workflow keeps feature development isolated until it is ready to be integrated into the main branch.

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
