import importlib
import pkgutil
from .base import Filter


# Imports all files in the folder : each Filter subclass registers itself automatically.
for _info in pkgutil.iter_modules(__path__):
    if _info.name != "base":
        importlib.import_module(f".{_info.name}", __name__)

FILTERS = Filter.registry


def get_filter(name, **params):
    """Creates the filter `name` with its parameters."""
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
