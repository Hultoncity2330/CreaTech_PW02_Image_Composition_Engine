import numpy as np
from pathlib import Path

import image_io
from blending_modes import get_blend
from filters import get_filter


IMAGES_DIR = Path(__file__).parent / "images"


class BlendEngine:
    """Run the complete image composition pipeline."""


    def run_pipeline(self, config: dict) -> np.ndarray:
        """Run the composition pipeline described by the configuration."""
        layers = config["layers"]

        if not layers:
            raise ValueError("The configuration contains no layers.")

        try:
            result = self._prepare_layer(layers[0])
        except (ValueError, FileNotFoundError, OSError) as error:
            raise type(error)(f"Layer 1: {error}") from error

        for index, layer in enumerate(layers[1:], start=2):
            try:
                image = self._prepare_layer(layer)

                if image.shape != result.shape:
                    raise ValueError(
                        f"image dimensions {image.shape} do not match {result.shape}."
                    )

                mode = layer.get("blend", "normal")
                opacity = layer.get("opacity", 1.0)

                result = get_blend(mode)(result, image, opacity)

            except (ValueError, FileNotFoundError, OSError) as error:
                raise type(error)(f"Layer {index}: {error}") from error

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

