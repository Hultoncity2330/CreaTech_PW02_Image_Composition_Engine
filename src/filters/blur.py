import numpy as np
from scipy.ndimage import convolve
from .base import Filter


class Blur(Filter):
    """Base class for blur filters using convolution."""

    def __init__(self, kernel: np.ndarray):
        self.kernel = kernel

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the convolution kernel to each RGB channel."""
        result = np.empty_like(image)

        for channel in range(3):
            result[:, :, channel] = convolve(
                image[:, :, channel],
                self.kernel,
                mode = "reflect",
            )

        return result
