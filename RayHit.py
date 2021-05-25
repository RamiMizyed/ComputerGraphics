from Vector3Math import *


class Ray:
    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self):
        self.t = float('inf')
        self.color = [0, 0, 0]
        self.normal: Vector3 = Vector3(0, 0, 0)
        self.intersect: bool = False
