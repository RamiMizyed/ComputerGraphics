import Object3D
import Vector3


class Triangle(Object3D):

    def __init__(self, v1: Vector3, v2: Vector3, v3: Vector3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def intersect(self, ray, hit, tmin):
        pass
