from Vector3Math import *


class Light:
    def __init__(self):
        pass


class DirectionalLight(Light):
    def __init__(self, directionV: Vector3, color: list):
        super().__init__()
        self.direction: Vector3 = directionV
        self.color: list = color


