import numpy as np
from scipy.ndimage import map_coordinates
from .base import Filter


class LensCircle(Filter):
    """Apply a circular magnifying lens effect."""

    name = "lens_circle"

    def __init__(self, intensity: float = 0.5, radius: float = 0.3):
        """Initialize the lens circle filter."""
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("Lens circle intensity must be between 0 and 1.")

        if not 0.0 < radius <= 1.0:
            raise ValueError("Lens circle radius must be between 0 and 1.")

        self.intensity = intensity
        self.radius = radius

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the circular lens effect to an RGB image."""
        height, width, _ = image.shape

        center_y = height / 2
        center_x = width / 2

        y, x = np.indices((height, width))

        dx = x - center_x
        dy = y - center_y

        max_radius = min(width, height) / 2
        lens_radius = max_radius * self.radius

        distance = np.sqrt(dx**2 + dy**2)
        mask = distance < lens_radius

        source_x = x.astype(float)
        source_y = y.astype(float)

        zoom = 1 + self.intensity

        source_x[mask] = center_x + dx[mask] / zoom
        source_y[mask] = center_y + dy[mask] / zoom

        result = np.zeros_like(image)

        for channel in range(3):
            result[:, :, channel] = map_coordinates(
                image[:, :, channel],
                [source_y, source_x],
                order=1,
                mode="reflect",
            )

        return result
