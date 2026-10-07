import importlib
import pkgutil

from .base import BaseBlend

# Importe tous les fichiers du dossier : chaque classe qui hérite de BaseBlend
# et définit `name` s'enregistre toute seule.
for _info in pkgutil.iter_modules(__path__):
    if _info.name != "base":
        importlib.import_module(f".{_info.name}", __name__)

BLEND_MODES = BaseBlend.registry


def get_blend(name):
    try:
        return BLEND_MODES[name]()
    except KeyError:
        raise ValueError(f"Mode inconnu '{name}'. Disponibles : {sorted(BLEND_MODES)}") from None


__all__ = ["BaseBlend","BLEND_MODES", "get_blend"]