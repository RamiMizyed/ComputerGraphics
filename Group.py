import Vector3
from Objects import Object3D


class Group(Object3D):
    def __init__(self):
        self.objects = []

    def add(self, object):
        self.objects.append(object)

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        for item in self.objects:
            item.intersect(ray, hit, tmin)
