import numpy as np
from Vector3 import *
from math import sqrt
from RayHit import *


class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        pass


class Plane(Object3D):
    def __init__(self, normal: Vector3, d, color):
        self.normal = normal
        self.d = d
        self.color = color

    def intersect(self, ray: Ray, hit, tmin):
        denominator: float = self.normal.dot(ray.direction)
        if denominator > -1e-6:
            return
        distance: Vector3 = ray.origin - self.d
        t: float = (-self.normal.dot(distance)) / denominator
        hit.t = t


class Sphere(Object3D):

    def __init__(self, center: Vector3, radius: float, color):
        Object3D.__init__(self, color)
        self.center = center
        self.radius = radius

    # L is the Vector from the eye to the Center
    # tca is just a distance between ray origin to the point where its perpendicular to the center of the sphere
    # thc is the distance from the point of intersection to where its perpendicular ...
    # D is the distance from center of sphere to base of the triangle

    def intersect(self, ray: Vector3, hit, tmin):
        L: Vector3 = self.center - ray.origin
        tca: float = L.dot(ray.direction)
        d2: float = L.dot(L) - tca * tca
        radius2 = self.radius * self.radius
        if d2 > radius2:
            return
        thc: float = sqrt(radius2 - d2)
        t0 = tca - thc
        hit.t = t0
        # t1 = tca + thc


class Triangle(Object3D):

    def __init__(self, v1: Vector3, v2: Vector3, v3: Vector3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def intersect(self, ray, hit, tmin):
        pass
