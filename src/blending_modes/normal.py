"""Normal blend mode."""

import numpy as np

from .base import BaseBlend


class NormalBlend(BaseBlend):
    """Normal: the source replaces the backdrop (before alpha and opacity)."""

    name = "normal"

    def _blend(self, backdrop: np.ndarray, source: np.ndarray) -> np.ndarray:
        """Apply the normal blend formula."""
        return source
