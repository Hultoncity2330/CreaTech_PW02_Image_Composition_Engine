import numpy as np
from pathlib import Path

import image_io
from blending_modes import get_blend
from filters import get_filter


IMAGES_DIR = Path(__file__).parent / "images"


class BlendEngine:
    """Run the complete image composition pipeline."""

    def __init__(self, mode = "normal", opacity = 1.0):
        self.set_mode(mode)
        self.opacity = opacity

    def set_mode(self, mode):
        """Set the current blending mode."""
        self._blend = get_blend(mode)
        self.mode = mode

    def run(self, backdrop, source):
        """Apply the current blending mode."""
        return self._blend(backdrop, source, self.opacity)

    def run_layers(self, backdrop, layers):
        """Blend multiple layers on top of a backdrop."""
        result = backdrop

        for image, mode, opacity in layers:
            if result.shape != image.shape:
                raise ValueError(
                    f"Image dimensions do not match: "
                    f"{result.shape} != {image.shape}."
                )

            result = get_blend(mode)(result, image, opacity)

        return result

    def run_pipeline(self, config: dict) -> np.ndarray:
        """Run the composition pipeline described by the configuration."""
        layers = config["layers"]

        if not layers:
            raise ValueError("Configuration contains no layers.")

        result = self._prepare_layer(layers[0])

        for index, layer in enumerate(layers[1:], start = 1):
            image = self._prepare_layer(layer)

            if result.shape != image.shape:
                raise ValueError(
                    f"Layer {index}: image dimensions "
                    f"{image.shape} do not match {result.shape}."
                )

            mode = layer.get("blend", "normal")
            opacity = layer.get("opacity", 1.0)

            result = get_blend(mode)(result, image, opacity)

        return result

    def _prepare_layer(self, layer: dict) -> np.ndarray:
        """Load a layer, apply its filters to RGB, and preserve alpha."""
        image = image_io.load_image(
            str(IMAGES_DIR / layer["image"])
        )

        rgb = image[..., :3]
        alpha = image[..., 3:]

        for filter_config in layer.get("filters", []):
            name = filter_config["name"]
            params = filter_config.get("params", {})

            filter_instance = get_filter(name, **params)
            rgb = filter_instance.apply(rgb)

        return np.concatenate([rgb, alpha], axis = 2)

