"""Multiply blend mode."""

import numpy as np

from .base import BaseBlend


class MultiplyBlend(BaseBlend):
    """Multiply: ``backdrop * source``. The result is never brighter than either input."""

    name = "multiply"

    def _blend(self, backdrop: np.ndarray, source: np.ndarray) -> np.ndarray:
        return backdrop * source
