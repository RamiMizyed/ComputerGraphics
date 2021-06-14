import sys
from math import *
from hit import *
from ray import Ray

from cgtypes import *


def transform(v3:vec3, matrix: mat4):
    return vec3(v3.x * matrix[0, 0] + v3.y * matrix[0, 1] + v3.z * matrix[0, 2] + matrix[0, 3],
                v3.x * matrix[1, 0] + v3.y * matrix[1, 1] + v3.z * matrix[1, 2] + matrix[1, 3],
                v3.x * matrix[2, 0] + v3.y * matrix[2, 1] + v3.z * matrix[2, 2] + matrix[2, 3])


def transfromNormal(v3:vec3, matrix: mat4):
    return vec3(v3.x * matrix[0, 0] + v3.y * matrix[0, 1] + v3.z * matrix[0, 2],
                v3.x * matrix[1, 0] + v3.y * matrix[1, 1] + v3.z * matrix[1, 2],
                v3.x * matrix[2, 0] + v3.y * matrix[2, 1] + v3.z * matrix[2, 2])


class Object3D:
    def __init__(self, material):
        self.material = None

    def intersect(self, ray: vec3, hit: vec3, tmin):
        pass


class Plane(Object3D):
    def __init__(self, normal: vec3, d, material):
        super().__init__(material)
        self.normal = normal
        self.d: vec3 = d * normal

    def intersect(self, ray: Ray, hit, tmin):
        denominator: float = self.normal * ray.direction  # ray.direction dot with normal
        if denominator > -1e-6:
            return
        distance: vec3 = ray.origin - self.d
        t: float = (-self.normal * distance) / denominator
        if hit.t > t > 0:
            hit.t = t
            hit.material = self.material
            hit.normal = self.normal
            hit.intersect = True

    def updates(self):
        pass


class Sphere(Object3D):

    def __init__(self, center: vec3, radius: float, material):
        Object3D.__init__(self, material)
        self.center = center
        self.radius = radius

    # L is the Vector from the eye to the Center
    # tca is just a distance between ray origin to the point where its perpendicular to the center of the sphere
    # thc is the distance from the point of intersection to where its perpendicular ...
    # D is the distance from center of sphere to base of the triangle

    def intersect(self, ray: Ray, hit: Hit, tmin):
        L: vec3 = self.center - ray.origin
        if L.length() < self.radius:
            return
        tca: float = L * ray.direction
        if tca < 0:
            return
        d2: float = L * L - tca * tca
        radius2 = self.radius * self.radius
        if d2 > radius2 or d2 < 0:
            return
        thc: float = sqrt(radius2 - d2)

        t0 = tca - thc
        # t1 = tca + thc

        if hit.t > t0 > 0:
            hit.t = t0
            hit.material = self.material
            p0 = ray.origin + ray.direction * t0
            hit.normal = (p0 - self.center).normalize()
            hit.intersect = True


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

        if t > 0 and t > tmin and t < hit.t:
            hit.material = self.material
            hit.t = t
            hit.normal = v0v1.cross(v0v2).normalize()
            hit.intersect = True


class Transformation(Object3D):
    def __init__(self, material, transformationMatrix: mat4, object3d):
        super().__init__(material)
        self.transformationMatrix: mat4 = transformationMatrix
        self.object3d = object3d

    def intersect(self, ray: Ray, hit: Hit, tmin):

        invMat: mat4 = self.transformationMatrix.inverse()

        ray.direction = transfromNormal(ray.direction, invMat).normalize()

        ray.origin = transform(ray.origin, invMat)
        self.object3d.intersect(ray, hit, tmin)
