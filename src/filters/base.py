import numpy as np
from abc import ABC, abstractmethod


class Filter(ABC):
    """Base class for all image filters."""

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the filter to an image and return the filtered image."""
        pass
