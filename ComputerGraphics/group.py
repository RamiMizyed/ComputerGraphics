from cgtypes import *
from object3d import Object3D
from hit import Hit


class Group(Object3D):
    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.objects = []

    def add(self, object3d: Object3D):
        self.objects.append(object3d)

    def intersect(self, ray: vec3, hit: Hit, tmin: float):
        for item in self.objects:
            item.intersect(ray, hit, tmin)
