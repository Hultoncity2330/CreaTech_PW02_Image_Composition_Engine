import json


def load_config(path: str) -> dict:
    """Load and validate the image composition configuration."""
    try:
        with open(path, encoding="utf-8") as file:
            config = json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON configuration: {error}"
        ) from error

    _validate_config(config)

    return config


def _validate_config(config: dict) -> None:
    """Validate the general structure of the configuration."""
    if not isinstance(config, dict):
        raise ValueError(
            "Configuration must be a JSON object."
        )

    if "layers" not in config:
        raise ValueError(
            "Configuration must contain 'layers'."
        )

    layers: list[dict] = config["layers"]

    if not isinstance(layers, list):
        raise ValueError(
            "'layers' must be a list."
        )

    if len(layers) == 0:
        raise ValueError(
            "Configuration must contain at least one layer."
        )

    for index, layer in enumerate(layers):
        _validate_layer(layer, index)


def _validate_layer(layer: dict, index: int) -> None:
    """Validate the structure of a layer."""
    if not isinstance(layer, dict):
        raise ValueError(
            f"Layer {index}: layer must be a JSON object."
        )

    if "image" not in layer:
        raise ValueError(
            f"Layer {index}: missing 'image'."
        )

    if "filters" not in layer:
        raise ValueError(
            f"Layer {index}: missing 'filters'."
        )

    if not isinstance(layer["image"], str):
        raise ValueError(
            f"Layer {index}: 'image' must be a string."
        )

    if not isinstance(layer["filters"], list):
        raise ValueError(
            f"Layer {index}: 'filters' must be a list."
        )

    for filter_config in layer["filters"]:
        _validate_filter(filter_config, index)

    _validate_blending(layer, index)


def _validate_filter(filter_config: dict, layer_index: int) -> None:
    """Validate the structure of a filter configuration."""
    if not isinstance(filter_config, dict):
        raise ValueError(
            f"Layer {layer_index}: filter must be a JSON object."
        )

    if "name" not in filter_config:
        raise ValueError(
            f"Layer {layer_index}: filter is missing 'name'."
        )

    if not isinstance(filter_config["name"], str):
        raise ValueError(
            f"Layer {layer_index}: filter 'name' must be a string."
        )

    if "params" in filter_config:
        if not isinstance(filter_config["params"], dict):
            raise ValueError(
                f"Layer {layer_index}: filter 'params' "
                "must be a JSON object."
            )


def _validate_blending(layer: dict, layer_index: int) -> None:
    """Validate blending mode and opacity of a layer."""
    if "blend" in layer:
        if not isinstance(layer["blend"], str):
            raise ValueError(
                f"Layer {layer_index}: 'blend' must be a string."
            )

    if "opacity" in layer:
        opacity = layer["opacity"]

        if not isinstance(opacity, (int, float)):
            raise ValueError(
                f"Layer {layer_index}: 'opacity' must be a number."
            )

        if not 0 <= opacity <= 1:
            raise ValueError(
                f"Layer {layer_index}: 'opacity' "
                "must be between 0 and 1."
            )

