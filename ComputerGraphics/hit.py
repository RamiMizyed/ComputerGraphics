from cgtypes import *


class Hit:
    def __init__(self):
        self.t = float('inf')
        self.material = None
        self.normal: vec3 = vec3(0)
        self.intersect: bool = False
        self.point: vec3 = vec3(0)
