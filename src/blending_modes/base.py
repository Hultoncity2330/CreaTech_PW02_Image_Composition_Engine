"""Base class shared by all blend modes."""

from abc import ABC, abstractmethod
from typing import Any, ClassVar

import numpy as np


class BaseBlend(ABC):
    """Base class for blend modes.

    A concrete mode only has to define ``name`` and implement ``_blend``.
    This class takes care of everything else: validation, conversion to float,
    layer opacity, per-pixel alpha compositing and conversion back to the
    original dtype. Subclasses that define ``name`` are registered
    automatically in ``BaseBlend.registry``.

    Images are arrays of shape ``(height, width, 3)`` (RGB) or
    ``(height, width, 4)`` (RGBA). Integer arrays are read as 0-255, float
    arrays as 0-1.
    """

    name: ClassVar[str | None] = None
    """Name used to select the mode (e.g. in the JSON config)."""

    registry: ClassVar[dict[str, type["BaseBlend"]]] = {}
    """Maps each mode name to its class. Filled automatically."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Register every subclass that defines its own ``name``."""
        super().__init_subclass__(**kwargs)
        name = cls.__dict__.get("name")
        if name is None:
            return  # intermediate class, not a usable mode
        if name in BaseBlend.registry:
            raise ValueError(
                f"Blend mode '{name}' already exists "
                f"({BaseBlend.registry[name].__name__})."
            )
        BaseBlend.registry[name] = cls

    def __call__(
        self,
        backdrop: np.ndarray,
        source: np.ndarray,
        opacity: float = 1.0,
    ) -> np.ndarray:
        """Shortcut for :meth:`apply`."""
        return self.apply(backdrop, source, opacity)

    def apply(
        self,
        backdrop: np.ndarray,
        source: np.ndarray,
        opacity: float = 1.0,
    ) -> np.ndarray:
        """Blend ``source`` on top of ``backdrop``.

        Args:
            backdrop: Bottom image, RGB or RGBA.
            source: Top image, RGB or RGBA, same height and width as the backdrop.
            opacity: Opacity of the top layer, between 0 and 1. It multiplies
                the alpha channel of ``source``.

        Returns:
            The blended image, with the dtype of ``backdrop``. It has an alpha
            channel (4 channels) if either input has one, otherwise 3 channels.

        Raises:
            ValueError: If an image is not ``(height, width, 3 or 4)``, if the
                two images differ in height or width, or if ``opacity`` is
                outside [0, 1].
        """
        self._check_image(backdrop, "backdrop")
        self._check_image(source, "source")
        if backdrop.shape[:2] != source.shape[:2]:
            raise ValueError(
                "Both images must have the same height and width, got "
                f"{backdrop.shape[:2]} and {source.shape[:2]}."
            )
        if not 0.0 <= opacity <= 1.0:
            raise ValueError(f"opacity must be between 0 and 1, got {opacity}.")

        has_alpha = backdrop.shape[2] == 4 or source.shape[2] == 4
        dtype = backdrop.dtype

        b_rgb, b_a = self._split(self._to_float(backdrop))
        s_rgb, s_a = self._split(self._to_float(source))
        s_a = s_a * opacity  # layer opacity scales the source alpha

        blended = self._blend(b_rgb, s_rgb)  # blend modes only see the RGB channels

        # Standard alpha compositing (source over, with a blend function)
        out_a = s_a + b_a * (1.0 - s_a)
        ratio = np.divide(s_a, out_a, out=np.zeros_like(out_a), where=out_a > 0)
        mixed = (1.0 - b_a) * s_rgb + b_a * blended
        out_rgb = (1.0 - ratio) * b_rgb + ratio * mixed

        out = np.concatenate([out_rgb, out_a], axis=2) if has_alpha else out_rgb
        return self._from_float(out, dtype)

    @abstractmethod
    def _blend(self, backdrop: np.ndarray, source: np.ndarray) -> np.ndarray:
        """Blend formula of the mode.

        Args:
            backdrop: Bottom RGB image, float values in [0, 1].
            source: Top RGB image, float values in [0, 1].

        Returns:
            The blended RGB image, same shape as the inputs. Alpha and opacity
            are handled by :meth:`apply`, not here.
        """

    @staticmethod
    def _check_image(image: np.ndarray, label: str) -> None:
        """Raise ``ValueError`` unless ``image`` is ``(height, width, 3 or 4)``."""
        if image.ndim != 3 or image.shape[2] not in (3, 4):
            raise ValueError(
                f"{label} must have shape (height, width, 3 or 4), "
                f"got {image.shape}."
            )

    @staticmethod
    def _split(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Split an image into RGB and alpha.

        Returns:
            ``(rgb, alpha)`` with alpha of shape ``(height, width, 1)``.
            Alpha is 1 everywhere if the image has no alpha channel.
        """
        if img.shape[2] == 4:
            return img[..., :3], img[..., 3:]
        return img, np.ones(img.shape[:2] + (1,), dtype=img.dtype)

    @staticmethod
    def _to_float(img: np.ndarray) -> np.ndarray:
        """Convert to float32 in [0, 1] (integer images are divided by 255)."""
        if np.issubdtype(img.dtype, np.integer):
            return img.astype(np.float32) / 255.0
        return img.astype(np.float32)

    @staticmethod
    def _from_float(img: np.ndarray, dtype: np.dtype) -> np.ndarray:
        """Clip to [0, 1] and convert back to ``dtype`` (rounded for integers)."""
        img = np.clip(img, 0.0, 1.0)
        if np.issubdtype(dtype, np.integer):
            return (img * 255.0 + 0.5).astype(dtype)
        return img.astype(dtype)
