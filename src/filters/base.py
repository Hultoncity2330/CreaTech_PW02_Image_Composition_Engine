import numpy as np
from abc import ABC, abstractmethod


class Filter(ABC):
    """Base class for all image filters."""

    registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        name = cls.__dict__.get("name", cls.__name__.lower())
        if name is None:
            return
        if name in Filter.registry:
            raise ValueError(f"The filter '{name}' already exists ({Filter.registry[name].__name__}).")
        Filter.registry[name] = cls

    
    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the filter to an image and return the filtered image."""
        pass

