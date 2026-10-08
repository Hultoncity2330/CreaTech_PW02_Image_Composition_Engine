import numpy as np
from scipy.ndimage import gaussian_filter
from .base import Filter


class NeonGlow(Filter):
    """Add a soft glow around bright areas of the image."""

    name = "neon_glow"

    def __init__(self, intensity: float = 0.7, radius: float = 8.0):
        """Initialize the neon glow filter."""
        if intensity < 0:
            raise ValueError("Neon glow intensity must be greater than or equal to 0.")

        if radius <= 0:
            raise ValueError("Neon glow radius must be greater than 0.")

        self.intensity = intensity
        self.radius = radius

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply a glow effect to bright parts of an RGB image."""
        brightness = np.mean(image, axis=2)

        mask = np.clip((brightness - 0.6) / 0.4, 0.0, 1.0)
        bright = image * mask[:, :, None]

        glow = np.zeros_like(image)

        for channel in range(3):
            glow[:, :, channel] = gaussian_filter(
                bright[:, :, channel],
                sigma=self.radius,
            )

        return image + glow * self.intensity
    