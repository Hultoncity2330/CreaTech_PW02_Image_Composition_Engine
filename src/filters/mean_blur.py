import numpy as np
from .blur import Blur


class MeanBlur(Blur):
    """Apply a mean blur to an image."""

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Mean blur size must be greater than 0.")
        
        kernel = np.ones((size, size)) / (size * size)
        super().__init__(kernel)
