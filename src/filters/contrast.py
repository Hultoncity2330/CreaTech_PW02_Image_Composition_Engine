import numpy as np
from .base import Filter


class Contrast(Filter):
    """Adjust the contrast of an image."""

    def __init__(self, level: float):
        self.level = level

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the contrast adjustment."""
        result = np.array(image)
        return (result - 0.5) * self.level + 0.5
