import math

from camera import Camera
from cgtypes import *
from ComputerGraphics.ray import Ray


class OrthographicCamera(Camera):
    def __init__(self, center: vec3, direction: vec3, up: vec3, size):
        self.center = center
        self.direction = direction.normalize()
        self.up = up.normalize()
        self.right = direction.cross(up).normalize()
        self.up = self.right.cross(self.direction).normalize()
        self.size = size

    def generate_ray(self, x: float, y: float):
        pos = self.center + (x - 0.5) * self.size * self.right + (y - 0.5) * self.size * self.up
        return Ray(pos, self.direction)
