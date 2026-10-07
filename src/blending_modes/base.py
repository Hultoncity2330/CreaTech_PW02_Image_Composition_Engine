from abc import ABC, abstractmethod
import numpy as np


class BaseBlend(ABC):
    """Classe de base : gère la conversion, l'opacité, l'alpha et le retour au dtype d'origine."""

    name = None      # à définir dans chaque mode concret
    registry = {}    # {nom: classe}, rempli automatiquement

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__dict__.get("name")
        if name is None:
            return   # classe intermédiaire, pas un mode
        if name in BaseBlend.registry:
            raise ValueError(f"Le blend '{name}' existe déjà ({BaseBlend.registry[name].__name__}).")
        BaseBlend.registry[name] = cls

    def __call__(self, backdrop, source, opacity=1.0):
        return self.apply(backdrop, source, opacity)

    def apply(self, backdrop, source, opacity=1.0):
        if backdrop.shape[:2] != source.shape[:2]:
            raise ValueError("Les deux images doivent avoir la même largeur et hauteur.")
        if not 0.0 <= opacity <= 1.0:
            raise ValueError("opacity doit être entre 0 et 1.")

        has_alpha = backdrop.shape[2] == 4 or source.shape[2] == 4
        dtype = backdrop.dtype
        
        b_rgb, b_a = self._split(self._to_float(backdrop))
        s_rgb, s_a = self._split(self._to_float(source))
        s_a = s_a * opacity                    # l'opacité du calque multiplie son alpha


        blended = self._blend(b_rgb, s_rgb)  # les modes ne voient que le RGB

        # composition alpha standard (source over, avec mode de fusion)
        out_a = s_a + b_a * (1.0 - s_a)
        ratio = np.divide(s_a, out_a, out=np.zeros_like(out_a), where=out_a > 0)
        mixed = (1.0 - b_a) * s_rgb + b_a * blended
        out_rgb = (1.0 - ratio) * b_rgb + ratio * mixed

        out = np.concatenate([out_rgb, out_a], axis=2) if has_alpha else out_rgb
        return self._from_float(out, dtype)

    @abstractmethod
    def _blend(self, backdrop: np.ndarray, source: np.ndarray) -> np.ndarray:
        """Formule du mode, sur des float dans [0, 1] (RGB uniquement)."""

    @staticmethod
    def _split(img):
        """Sépare RGB et alpha (alpha = 1 partout si l'image est en RGB)."""
        if img.shape[2] == 4:
            return img[..., :3], img[..., 3:]
        return img, np.ones(img.shape[:2] + (1,), dtype=img.dtype)
    
    @staticmethod
    def _to_float(img):
        if np.issubdtype(img.dtype, np.integer):
            return img.astype(np.float32) / 255.0
        return img.astype(np.float32)

    @staticmethod
    def _from_float(img, dtype):
        img = np.clip(img, 0.0, 1.0)
        if np.issubdtype(dtype, np.integer):
            return (img * 255.0 + 0.5).astype(dtype)
        return img.astype(dtype)