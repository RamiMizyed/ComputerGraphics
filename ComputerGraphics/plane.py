from object3d import Object3D
from hit import Hit
from ray import Ray
from cgtypes import *


class Plane(Object3D):
    def __init__(self, normal: vec3, d, material):
        super().__init__(material)
        self.normal = normal.normalize()
        self.d: vec3 = d * self.normal

    def intersect(self, ray: Ray, hit: Hit, tmin):
        denominator: float = ray.direction * self.normal  # ray.direction dot with normal
        if denominator >= -1e-6:
            return
        diff: vec3 = ray.origin - self.d
        t: float = -(self.normal * diff) / denominator
        if hit.t > t > tmin:
            hit.t = t
            hit.material = self.material
            hit.normal = self.normal
            hit.intersect = True
            hit.point = ray.origin + ray.direction * t
