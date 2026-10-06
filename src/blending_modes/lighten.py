import numpy as np
from .base import BaseBlend


class LightenBlend(BaseBlend):
    name = "lighten"

    def _blend(self, backdrop, source):
        return np.maximum(backdrop, source)