from hit import Hit
from ray import Ray
from Lights import *


class Material:
    def __init__(self):
        self.diffuseColor = None
        self.reflectiveColor = None
        self.transparentColor = None
        self.indexOfRefraction = None

    def shade(self, ray: Ray, hit: Hit, light: Light):
        pass


class PhongMaterial(Material):

    def __init__(self):
        super().__init__()
        self.specularColor = None
        self.exponent = None

    def shade(self, ray: Ray, hit: Hit, light: Light):
        pass
