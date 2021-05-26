from cgtypes import *


class Light:
    def __init__(self):
        pass


class DirectionalLight(Light):
    def __init__(self, directionV: vec3, color: list):
        super().__init__()
        self.direction: vec3 = directionV
        self.color: list = color


