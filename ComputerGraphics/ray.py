from cgtypes import *


class Ray:
    def __init__(self, origin: vec3, direction: vec3):
        self.origin: vec3 = origin
        self.direction: vec3 = direction
