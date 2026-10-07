from pathlib import Path

import numpy as np

import image_io
from blending_modes import get_blend
from filters import get_filter

IMAGES_DIR = Path(__file__).parent / "images"


class BlendEngine:
    """Orchestre le blending : choisit le mode et l'applique aux images."""

    def __init__(self, mode="normal", opacity=1.0):
        self.set_mode(mode)
        self.opacity = opacity

    def set_mode(self, mode):
        self._blend = get_blend(mode)  # lève ValueError si le mode est inconnu
        self.mode = mode

    def run(self, backdrop, source):
        """Applique le mode courant : source posée sur backdrop."""
        return self._blend(backdrop, source, self.opacity)

    def run_layers(self, backdrop, layers):
        """Empile plusieurs calques sur backdrop.

        layers : liste de tuples (image, mode, opacity), appliqués dans l'ordre.
        """
        result = backdrop
        for image, mode, opacity in layers:
            result = get_blend(mode)(result, image, opacity)
        return result

    def run_pipeline(self, config):
        """Exécute le pipeline décrit par le JSON (dict déjà chargé)."""
        layers = config["layers"]
        if not layers:
            raise ValueError("Le JSON ne contient aucun calque.")

        result = self._prepare_layer(layers[0])
        for layer in layers[1:]:
            image = self._prepare_layer(layer)
            mode = layer.get("blend", "normal")
            opacity = layer.get("opacity", 1.0)
            result = get_blend(mode)(result, image, opacity)
        return result

    def _prepare_layer(self, layer):
        """Charge l'image d'un calque puis applique ses filtres (sur le RGB, l'alpha est conservé)."""
        image = image_io.load_image(str(IMAGES_DIR / layer["image"]))
        rgb, alpha = image[..., :3], image[..., 3:]
        for f in layer.get("filters", []):
            rgb = get_filter(f["name"], **f.get("params", {})).apply(rgb)
        return np.concatenate([rgb, alpha], axis=2)
