from .base import BaseBlend
from .normal import NormalBlend
from .multiply import MultiplyBlend
from .lighten import LightenBlend

BLEND_MODES = {
    cls.name: cls for cls in (NormalBlend, MultiplyBlend, LightenBlend)
}


def get_blend(name):
    try:
        return BLEND_MODES[name]()
    except KeyError:
        raise ValueError(f"Mode inconnu '{name}'. Disponibles : {list(BLEND_MODES)}")


__all__ = ["BaseBlend", "NormalBlend", "MultiplyBlend", "LightenBlend","BLEND_MODES", "get_blend"]