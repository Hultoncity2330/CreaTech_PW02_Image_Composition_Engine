from abc import ABC, abstractmethod
import numpy as np


class BaseBlend(ABC):
    """Classe de base : gère la conversion, l'opacité et le retour au dtype d'origine."""

    name = "base"

    def __call__(self, backdrop, source, opacity=1.0):
        return self.apply(backdrop, source, opacity)

    def apply(self, backdrop, source, opacity=1.0):
        if backdrop.shape != source.shape:
            raise ValueError("Les deux images doivent avoir la même forme.")
        if not 0.0 <= opacity <= 1.0:
            raise ValueError("opacity doit être entre 0 et 1.")

        dtype = backdrop.dtype
        b = self._to_float(backdrop)
        s = self._to_float(source)

        blended = self._blend(b, s)
        result = (1.0 - opacity) * b + opacity * blended

        return self._from_float(result, dtype)

    @abstractmethod
    def _blend(self, backdrop, source):
        """Formule du mode, sur des float dans [0, 1]."""

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