import numpy as np
from .base import Filter


class Chromatic(Filter):
    """Apply a chromatic aberration effect to an RGB image."""

    name = "chromatic"

    def __init__(self, intensity: float = 1.0):
        """Initialize the chromatic filter."""
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("Chromatic intensity must be between 0 and 1.")

        self.intensity = intensity

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the chromatic effect to an RGB image."""
        shifted = np.array(image, copy=True)

        shift = 30

        shifted[:, :, 0] = np.roll(
            image[:, :, 0],
            shift=shift,
            axis=1,
        )

        shifted[:, :, 2] = np.roll(
            image[:, :, 2],
            shift=-shift,
            axis=1,
        )

        result = (
            image * (1.0 - self.intensity)
            + shifted * self.intensity
        )

        return result
