import numpy as np
from Vector3Math import *
from math import sqrt
from RayHit import *


# why isn't color a Vector 3 or an array ?
class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(self, ray: Vector3Math, hit: Vector3Math, tmin):
        pass


class Plane(Object3D):
    def __init__(self, normal: Vector3Math, d, color):
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

    def __init__(self, center: Vector3Math, radius: float, color):
        Object3D.__init__(self, color)
        self.center = center
        self.radius = radius

    # L is the Vector from the eye to the Center
    # tca is just a distance between ray origin to the point where its perpendicular to the center of the sphere
    # thc is the distance from the point of intersection to where its perpendicular ...
    # D is the distance from center of sphere to base of the triangle

    def intersect(self, ray: Vector3Math, hit, tmin):
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
        hit.t = t0
        hit.color = self.color
        p0 = ray.origin + ray.direction * t0
        hit.normal = (p0 - self.center).normal()
        # pass the normal at intersection point
        # t1 = tca + thc


class Triangle(Object3D):

    def __init__(self, v1: Vector3Math, v2: Vector3Math, v3: Vector3Math, color):
        super().__init__(color)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def intersect(self, ray, hit, tmin):
        pass


class Transformation(Object3D):

    def __init__(self, color, TransformationMatrix, object):
        super().__init__(color)
        self.TransformationMatrix = np.zeros(4, 4)
        self.object = Object3D

    def intersect(self, ray: Vector3Math, hit: Vector3Math, tmin):
        pass
