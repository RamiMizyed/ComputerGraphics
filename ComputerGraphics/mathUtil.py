import math

from cgtypes import *


def transform(v3: vec3, matrix: mat4):
    return vec3(v3.x * matrix[0, 0] + v3.y * matrix[0, 1] + v3.z * matrix[0, 2] + matrix[0, 3],
                v3.x * matrix[1, 0] + v3.y * matrix[1, 1] + v3.z * matrix[1, 2] + matrix[1, 3],
                v3.x * matrix[2, 0] + v3.y * matrix[2, 1] + v3.z * matrix[2, 2] + matrix[2, 3])


def transform_normal(v3: vec3, matrix: mat4):
    return vec3(v3.x * matrix[0, 0] + v3.y * matrix[0, 1] + v3.z * matrix[0, 2],
                v3.x * matrix[1, 0] + v3.y * matrix[1, 1] + v3.z * matrix[1, 2],
                v3.x * matrix[2, 0] + v3.y * matrix[2, 1] + v3.z * matrix[2, 2])


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def mul_int(x, y):
    return int(x * y)


def refract(incoming: vec3, normal: vec3, ior: float):
    cosi = normal * incoming
    etai = 1
    etat = ior
    n = normal
    if cosi < 0:
        cosi = -cosi
    else:
        temp = etai
        etai = etat
        etat = temp
        n = -normal
    eta = etai / etat
    k = 1 - (eta * eta) * (1 - (cosi * cosi))
    if k <= 0:
        return vec3(0)
    else:
        return ((incoming + cosi * n) * eta - n * math.sqrt(k)).normalize()
