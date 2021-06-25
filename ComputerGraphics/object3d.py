from hit import Hit
from cgtypes import *
from Material import Material

class Object3D:
    def __init__(self, material: Material):
        self.material = material

    def intersect(self, ray: vec3, hit: Hit, tmin: float):
        pass
