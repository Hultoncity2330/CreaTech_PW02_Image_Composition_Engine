import numpy as np
from .blur import Blur


class GaussianBlur(Blur):
    """Apply a Gaussian blur to an image."""

    def __init__(self, size: int, sigma: float = 1.0):
        ax = np.arange(-(size // 2), size // 2 + 1)
        xx, yy = np.meshgrid(ax, ax)

        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
        kernel = kernel / kernel.sum()

        super().__init__(kernel)
