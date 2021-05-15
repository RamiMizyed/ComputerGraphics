from Object3D import Object3D
from Vector3 import Vector3
from math import sqrt


class Sphere(Object3D):

    def __init__(self, center: Vector3, radius: float, color):
        Object3D.__init__(self, color)
        self.center = center
        self.radius = radius

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        L: Vector3 = ray.center - ray.origin
        tca: float = L.dot(ray.direction)
        d2: float = L.dot(L) - tca * tca
        if d2 > self.radius:
            pass
        thc: float = sqrt(self.radius - d2)
        t0 = tca - thc
        t1 = tca + thc
