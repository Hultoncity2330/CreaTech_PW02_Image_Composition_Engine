import numpy as np
from .base import Filter


class GrayScale(Filter):
    """Convert an RGB image to grayscale."""

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply a grayscale filter to the image."""
        result = np.array(image)

        gray = result.mean(axis = 2)
        result[:, :, :] = gray[:, :, None]

        return result
