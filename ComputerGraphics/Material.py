from hit import Hit
from ray import Ray
from Lights import *
from mathUtil import *


class Material:
    def __init__(self, diffuseColor=None, reflectiveColor=None,
                 transparentColor=None, ior: float = 1):

        self.diffuseColor = diffuseColor
        self.reflectiveColor = reflectiveColor
        self.transparentColor = transparentColor
        self.indexOfRefraction = ior

        if transparentColor is None:
            self.transparentColor = [0, 0, 0]
        if diffuseColor is None:
            self.diffuseColor = [0, 0, 0]
        if reflectiveColor is None:
            self.reflectiveColor = [0, 0, 0]
        if ior is None:
            self.indexOfRefraction = 1

    def shade(self, ray: Ray, hit: Hit, light: Light):
        pass


class PhongMaterial(Material):
    def __init__(self, specularColor=None, exponent=4, diffuseColor=None,
                 reflectiveColor=None, transparentColor=None, ior=1):

        super().__init__(diffuseColor, reflectiveColor, transparentColor, ior)
        self.specularColor = specularColor
        self.exponent = exponent

        if specularColor is None:
            self.specularColor = [0, 0, 0]
        if exponent is None:
            self.exponent = 1

    def shade(self, ray: Ray, hit: Hit, light: Light):
        viewDir: vec3 = -ray.direction
        lightDir: vec3 = -light.direction

        NDotL = hit.normal * lightDir
        diffuse = list(map(mul, self.diffuseColor, light.color))
        diffuseF = list(map(mul, diffuse, [max(NDotL, 0)]*3))

        R = (-lightDir).reflect(hit.normal)
        RDotV = R * viewDir
        expArg = pow(max(RDotV, 0), self.exponent)
        specular = list(map(mul, self.specularColor, light.color))
        specularF = list(map(mul, specular, [expArg]*3))

        return list(map(add, diffuseF, specularF))
