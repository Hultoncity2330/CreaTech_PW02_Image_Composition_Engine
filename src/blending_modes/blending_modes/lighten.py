"""Lighten blend mode."""

import numpy as np

from .base import BaseBlend


class LightenBlend(BaseBlend):
    """Lighten: keeps the brighter of the two values, channel by channel."""

    name = "lighten"

    def _blend(self, backdrop: np.ndarray, source: np.ndarray) -> np.ndarray:
        return np.maximum(backdrop, source)
