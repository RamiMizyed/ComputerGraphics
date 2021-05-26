import numpy as np
from cgtypes import *
from math import *
from RayHit import *
import sys


class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(self, ray: vec3, hit: vec3, tmin):
        pass


class Plane(Object3D):
    def __init__(self, normal: vec3, d, color):
        super().__init__(color)
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
            hit.color = self.color
            hit.normal = self.normal
            hit.intersect = True

    def updates(self):
        pass


class Sphere(Object3D):

    def __init__(self, center: vec3, radius: float, color):
        Object3D.__init__(self, color)
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
            hit.color = self.color
            p0 = ray.origin + ray.direction * t0
            hit.normal = (p0 - self.center).normalize()
            hit.intersect = True


class Triangle(Object3D):

    def __init__(self, v0: vec3, v1: vec3, v2: vec3, color):
        super().__init__(color)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def intersect(self, ray: Ray, hit: Hit, tmin):
        v0v1: vec3 = self.v1 - self.v0
        v0v2: vec3 = self.v2 - self.v0
        pvec: vec3 = vec3.cross(ray.direction, v0v2)
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
        qvec: vec3 = vec3.cross(tvec, v0v1)
        v: float = ray.direction * qvec * inverse
        if u < 0 or (u + v > 1):
            return

        t: float = v0v2 * qvec * inverse

        if t > 0 and t > tmin and t < hit.t:
            hit.color = self.color
            hit.t = t
            hit.normal = vec3.cross(v0v1, v0v2).normalize()
            hit.intersect = True


class Transformation(Object3D):
    def __init__(self, color, transformationMatrix: mat4, object3d):
        super().__init__(color)
        self.transformationMatrix: mat4 = transformationMatrix
        self.object3d = object3d

    def intersect(self, ray: Ray, hit: Hit, tmin):

        invMat: mat4 = self.transformationMatrix.inverse()

        ray.direction = invMat * ray.direction

        ray.origin = invMat * ray.origin
        self.object3d.intersect(ray, hit, tmin)
