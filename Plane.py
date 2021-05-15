import Object3D
import numpy as np
import Vector3


class Plane(Object3D):
    def __init__(self, normal, d, color):
        self.normal = normal
        self.d = d
        self.color = color

    def intersect(self, ray, hit, tmin):
        denominator: float = np.dot(self.normal, 1)
        if denominator > 1e-6:
            polo: Vector3 = 0 - 0
            t = np.dot(polo, ray)

    def updates(self, t, color, normal):
        pass
