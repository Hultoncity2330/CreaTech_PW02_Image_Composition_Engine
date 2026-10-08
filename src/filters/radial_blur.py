import numpy as np
from scipy.ndimage import map_coordinates
from .base import Filter


class RadialBlur(Filter):
    """Apply a radial blur effect from the center of the image."""

    name = "radial_blur"

    def __init__(self, intensity: float = 0.1, samples: int = 10):
        """Initialize the radial blur filter."""
        if intensity < 0:
            raise ValueError("Radial blur intensity must be greater than or equal to 0.")

        if samples <= 0:
            raise ValueError("Radial blur samples must be greater than 0.")

        self.intensity = intensity
        self.samples = samples

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply radial blur to an RGB image."""
        height, width, _ = image.shape

        center_y = height / 2
        center_x = width / 2

        y, x = np.indices((height, width))

        result = np.zeros_like(image)

        for sample in range(self.samples):
            factor = 1.0 - self.intensity * sample / self.samples

            sample_x = center_x + (x - center_x) * factor
            sample_y = center_y + (y - center_y) * factor

            for channel in range(3):
                result[:, :, channel] += map_coordinates(
                    image[:, :, channel],
                    [sample_y, sample_x],
                    order=1,
                    mode="reflect",
                )

        return result / self.samples
