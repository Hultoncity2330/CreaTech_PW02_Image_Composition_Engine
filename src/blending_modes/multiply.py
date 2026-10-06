from .base import BaseBlend


class MultiplyBlend(BaseBlend):
    name = "multiply"

    def _blend(self, backdrop, source):
        return backdrop * source