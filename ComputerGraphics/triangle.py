from object3d import Object3D
from math import *
from hit import *
from ray import Ray
from cgtypes import *

class Triangle(Object3D):

    def __init__(self, v0: vec3, v1: vec3, v2: vec3, material):
        super().__init__(material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def intersect(self, ray: Ray, hit: Hit, tmin):
        v0v1: vec3 = self.v1 - self.v0
        v0v2: vec3 = self.v2 - self.v0
        pvec: vec3 = ray.direction.cross(v0v2)
        determinant: float = v0v1 * pvec
        if determinant < sys.float_info.epsilon:
            return
        if fabs(determinant) < sys.float_info.epsilon:
            return
        inverse: float = 1 / determinant
        tvec: vec3 = ray.origin - self.v0
        u: float = tvec * pvec * inverse
        if u < 0 or u > 1:
            return
        qvec: vec3 = tvec.cross(v0v1)
        v: float = ray.direction * qvec * inverse
        if v < 0 or (u + v > 1):
            return

        t: float = v0v2 * qvec * inverse

        if hit.t > t > tmin:
            hit.material = self.material
            hit.t = t
            hit.normal = v0v1.cross(v0v2).normalize()
            hit.intersect = True
            hit.point = ray.origin + ray.direction * t

