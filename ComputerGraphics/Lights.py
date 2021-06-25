from cgtypes import *


class Light:
    def __init__(self):
        self.color = None
        self.direction = None


class DirectionalLight(Light):
    def __init__(self, direction: vec3, color=None):
        super().__init__()

        self.direction: vec3 = direction.normalize()
        self.color = color

        if color is None:
            self.color = [0, 0, 0]
