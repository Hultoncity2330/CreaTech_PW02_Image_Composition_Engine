from .base import Filter
from .brightness import Brightness
from .contrast import Contrast
from .grayscale import GrayScale
from .sepia import Sepia
from .mean_blur import MeanBlur
from .gaussian_blur import GaussianBlur


FILTERS: dict[str, type[Filter]] = {
    "brightness": Brightness,
    "contrast": Contrast,
    "grayscale": GrayScale,
    "sepia": Sepia,
    "meanblur": MeanBlur,
    "gaussianblur": GaussianBlur,
}


def get_filter(name: str, params: dict) -> Filter:
    """Create a filter from its registered name and parameters."""
    try:
        filter_class = FILTERS[name]
    except KeyError:
        raise ValueError(f"Unknown filter: '{name}'")

    try:
        return filter_class(**params)
    except TypeError as error:
        raise ValueError(
            f"Invalid parameters for filter '{name}': {params}"
        ) from error

