import numpy as np
from .base import Filter


class Brightness(Filter):
    """Adjust the brightness of an image."""

    def __init__(self, level: float):
        """Initialize the brightness filter with an adjustment level."""
        self.level = level

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the brightness adjustment."""
        result = np.array(image)
        return result + self.level
