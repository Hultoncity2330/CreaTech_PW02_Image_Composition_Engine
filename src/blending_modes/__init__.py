"""Blend modes.

Every module in this package is imported automatically. A class that inherits
from ``BaseBlend`` and defines ``name`` registers itself, so adding a blend
mode only requires dropping a new file in this folder.
"""

import importlib
import pkgutil

from .base import BaseBlend

for _info in pkgutil.iter_modules(__path__):
    if _info.name != "base":
        importlib.import_module(f".{_info.name}", __name__)

BLEND_MODES: dict[str, type[BaseBlend]] = BaseBlend.registry


def get_blend(name: str) -> BaseBlend:
    """Create the blend mode called ``name``.

    Args:
        name: Mode name, e.g. ``"normal"``, ``"multiply"`` or ``"lighten"``.

    Returns:
        A new instance of the matching blend mode.

    Raises:
        ValueError: If no mode has this name.
    """
    try:
        return BLEND_MODES[name]()
    except KeyError:
        raise ValueError(
            f"Unknown blend mode '{name}'. Available: {sorted(BLEND_MODES)}"
        ) from None


__all__ = ["BaseBlend", "BLEND_MODES", "get_blend"]
