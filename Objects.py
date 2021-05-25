import numpy as np
from Vector3Math import *
from math import sqrt
from RayHit import *
import sys


# why isn't color a Vector 3 or an array ?
class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        pass


class Plane(Object3D):
    def __init__(self, normal: Vector3, d, color):
        super().__init__(color)
        self.normal = normal
        self.d = d

    def intersect(self, ray: Ray, hit, tmin):
        denominator: float = self.normal.dot(ray.direction)
        if denominator > -1e-6:
            return
        distance: Vector3 = ray.origin - self.d
        t: float = (-self.normal.dot(distance)) / denominator
        hit.t = t

    def updates(self):
        pass


class Sphere(Object3D):

    def __init__(self, center: Vector3, radius: float, color):
        Object3D.__init__(self, color)
        self.center = center
        self.radius = radius

    # L is the Vector from the eye to the Center
    # tca is just a distance between ray origin to the point where its perpendicular to the center of the sphere
    # thc is the distance from the point of intersection to where its perpendicular ...
    # D is the distance from center of sphere to base of the triangle

    def intersect(self, ray: Ray, hit: Hit, tmin):
        L: Vector3 = self.center - ray.origin
        if L.magnitude() < self.radius:
            return
        tca: float = L.dot(ray.direction)
        if tca < 0:
            return
        d2: float = L.dot(L) - tca * tca
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
            hit.normal = (p0 - self.center).normal()
            hit.intersect = True


class Triangle(Object3D):

    def __init__(self, v0: Vector3, v1: Vector3, v2: Vector3, color):
        super().__init__(color)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def intersect(self, ray: Ray, hit: Hit, tmin):
        v0v1: Vector3 = self.v1 - self.v0
        v0v2: Vector3 = self.v2 - self.v0
        pointVector: Vector3 = ray.direction.cross(v0v2)
        determinant: float = pointVector.dot(v0v1)
        if determinant < 0.1:
            return

        if math.fabs(determinant) < 0.1:
            return
        inverse: float = 1 / determinant
        tvec: Vector3 = ray.origin - self.v0
        u: float = tvec.dot(pointVector) * inverse
        if u < 0 or u > 1:
            return
        qvec: Vector3 = tvec.cross(v0v1)
        v: float = qvec.dot(ray.direction) * inverse
        if u < 0 or u + v > 1:
            return

        t: float = v0v2.dot(qvec) * inverse

        if t > 0 and t > tmin and t < hit.t:
            hit.color = self.color
            hit.t = t
            hit.normal = v0v1.cross(v0v2).normal()
            hit.intersect = True


class Transformation(Object3D):

    def __init__(self, color, TransformationMatrix, object):
        super().__init__(color)
        self.TransformationMatrix = np.zeros(4, 4)
        self.object = Object3D

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        pass
