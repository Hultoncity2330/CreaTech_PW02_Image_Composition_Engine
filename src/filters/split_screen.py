import numpy as np
from .base import Filter


class SplitScreen(Filter):
    """Repeat the image several times in a grid."""

    name = "split_screen"

    def __init__(self, splits: int = 2):
        """Initialize the split screen filter."""
        if splits <= 0:
            raise ValueError("Split screen splits must be greater than 0.")

        self.splits = splits

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the split screen effect to an RGB image."""
        height, width, _ = image.shape

        y = np.arange(height) * self.splits % height
        x = np.arange(width) * self.splits % width

        return image[y[:, None], x]
