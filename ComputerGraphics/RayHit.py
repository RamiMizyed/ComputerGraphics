from cgtypes import *
class Ray:
    def __init__(self, origin: vec3, direction: vec3):
        self.origin: vec3 = origin
        self.direction: vec3 = direction


class Hit:
    def __init__(self):
        self.t = float('inf')
        self.color = [0, 0, 0]
        self.normal: vec3 = vec3(0, 0, 0)
        self.intersect: bool = False
