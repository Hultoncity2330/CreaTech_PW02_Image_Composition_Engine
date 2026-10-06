import image_io    
from blending_modes import get_blend

def run_pipeline(self, config, apply_filter=None):
        """Exécute le pipeline décrit par le JSON (dict déjà chargé)."""
        layers = config["layers"]
        if not layers:
            raise ValueError("Le JSON ne contient aucun calque.")

        result = self._prepare_layer(layers[0], apply_filter)
        for layer in layers[1:]:
            image = self._prepare_layer(layer, apply_filter)
            blend = layer.get("blend", {})
            mode = blend.get("mode", "normal")
            opacity = blend.get("opacity", 1.0)
            result = get_blend(mode)(result, image, opacity)
        return result

def _prepare_layer(self, layer, apply_filter):
    """Charge l'image d'un calque puis applique ses filtres dans l'ordre."""
    image = image_io.load_image(layer["path"])
    for f in layer.get("filters", []):
        if apply_filter is None:
            raise ValueError("Des filtres sont demandés mais aucune fonction de filtre n'est fournie.")
        image = apply_filter(image, f["name"], **f.get("params", {}))
    return image


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