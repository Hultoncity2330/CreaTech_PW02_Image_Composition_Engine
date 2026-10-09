import importlib
import pkgutil
from .base import Filter
from .invert import Invert


# Imports all files in the folder : each Filter subclass registers itself automatically.
for _info in pkgutil.iter_modules(__path__):
    if _info.name != "base":
        importlib.import_module(f".{_info.name}", __name__)

FILTERS = Filter.registry

# External filter received from another group.
FILTERS["invert"] = Invert


def get_filter(name, **params):
    """Create a filter from its name and parameters."""
    
    try:
        cls = FILTERS[name]
    except KeyError:
        raise ValueError(f"Unknown filter '{name}'. Available : {sorted(FILTERS)}") from None

    try:
        return cls(**params)
    except TypeError as error:
        raise ValueError(
            f"Invalid parameters for filter '{name}': {params}"
        ) from error


__all__ = ["Filter", "FILTERS", "get_filter"]
