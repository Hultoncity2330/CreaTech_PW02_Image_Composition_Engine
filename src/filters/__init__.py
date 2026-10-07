import importlib
import pkgutil

from .base import Filter



# Importe tous les fichiers du dossier : chaque sous-classe de Filter s'enregistre toute seule.
for _info in pkgutil.iter_modules(__path__):
    if _info.name != "base":
        importlib.import_module(f".{_info.name}", __name__)

FILTERS = Filter.registry


def get_filter(name, **params):
    """Crée le filtre `name` avec ses paramètres (ceux du constructeur)."""
    try:
        cls = FILTERS[name]
    except KeyError:
        raise ValueError(f"Filtre inconnu '{name}'. Disponibles : {sorted(FILTERS)}") from None
    return cls(**params)


__all__ = ["Filter", "FILTERS", "get_filter"]

