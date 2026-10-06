from abc import ABC, abstractmethod
import numpy as np


class Filter(ABC):
    """Base class for all image filters."""

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the filter to an image and return the filtered image."""
        pass
