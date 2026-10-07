import numpy as np
from .blur import Blur


class MeanBlur(Blur):
    """Apply a mean blur to an image."""

    def __init__(self, size: int):
        kernel = np.ones((size, size)) / (size * size)
        super().__init__(kernel)
