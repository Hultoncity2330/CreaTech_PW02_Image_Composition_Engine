import numpy as np
from .base import Filter


class Sepia(Filter):
    """Apply a sepia effect to an RGB image."""

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the sepia transformation."""
        sepia_matrix = np.array([
            [0.393, 0.349, 0.272],
            [0.769, 0.686, 0.534],
            [0.189, 0.168, 0.131],
        ])
        return image @ sepia_matrix
