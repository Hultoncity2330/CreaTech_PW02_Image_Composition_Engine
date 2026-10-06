from .base import BaseBlend


class NormalBlend(BaseBlend):
    name = "normal"

    def _blend(self, backdrop, source):
        return source