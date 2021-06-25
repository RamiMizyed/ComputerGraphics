from object3d import Object3D
from math import *
from hit import *
from ray import Ray
from cgtypes import *


class Sphere(Object3D):

    def __init__(self, center: vec3, radius: float, material):
        Object3D.__init__(self, material)
        self.center = center
        self.radius = radius
        self.radius2 = self.radius * self.radius

    # L is the Vector from the eye to the Center
    # tca is just a distance between ray origin to the point where its perpendicular to the center of the sphere
    # thc is the distance from the point of intersection to where its perpendicular ...
    # D is the distance from center of sphere to base of the triangle

    def intersect(self, ray: Ray, hit: Hit, tmin):
        L: vec3 = self.center - ray.origin

        tca: float = L * ray.direction
        if tca < 0:
            return

        d2: float = L * L - tca * tca
        if d2 > self.radius2:
            return
        thc: float = sqrt(self.radius2 - d2)

        t0 = tca - thc
        t1 = tca + thc

        t = t0
        if t <= tmin:
            t = t1

        if hit.t > t > tmin:
            # if object was transformed these values will be transformed from object to world space later
            hit.t = t
            hit.point = ray.origin + ray.direction * t
            hit.normal = (hit.point - self.center).normalize()
            hit.material = self.material
            hit.intersect = True
