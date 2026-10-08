import numpy as np
from scipy.ndimage import map_coordinates
from .base import Filter


class Bulge(Filter):
    """Apply a bulge distortion from the center of the image."""

    name = "bulge"

    def __init__(self, intensity: float = 0.5):
        """Initialize the bulge filter."""
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("Bulge intensity must be between 0 and 1.")

        self.intensity = intensity

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply a bulge distortion to an RGB image."""
        height, width, _ = image.shape

        center_y = height / 2
        center_x = width / 2

        y, x = np.indices((height, width))

        dx = x - center_x
        dy = y - center_y

        radius = min(width, height) / 2
        distance = np.sqrt(dx**2 + dy**2)

        normalized = distance / radius
        mask = normalized < 1

        factor = np.ones_like(normalized)
        factor[mask] = 1 - self.intensity * (1 - normalized[mask]) ** 2

        source_x = center_x + dx * factor
        source_y = center_y + dy * factor

        result = np.zeros_like(image)

        for channel in range(3):
            result[:, :, channel] = map_coordinates(
                image[:, :, channel],
                [source_y, source_x],
                order=1,
                mode="reflect",
            )

        return result
