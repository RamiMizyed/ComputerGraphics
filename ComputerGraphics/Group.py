from cgtypes import *
from Objects import Object3D


class Group(Object3D):
    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.objects = []

    def add(self, object):
        self.objects.append(object)

    def intersect(self, ray: vec3, hit: vec3, tmin):
        for item in self.objects:
            item.intersect(ray, hit, tmin)
