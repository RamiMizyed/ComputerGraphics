import math

from camera import Camera
from cgtypes import *
from ComputerGraphics.ray import Ray


class PerspectiveCamera(Camera):
    def __init__(self, center: vec3, direction: vec3, up: vec3, angle):
        self.center = center
        self.direction = direction.normalize()
        self.up = up.normalize()
        self.right: vec3 = direction.cross(up).normalize()
        self.up = self.right.cross(self.direction).normalize()
        self.angle = angle

        angleRadians: float = self.angle * math.pi/180
        muqabil = math.tan(angleRadians/2)
        self.leftestSide = muqabil * -self.right
        self.bottomestSide = muqabil * -self.up
        self.bottomLeftCorner = self.leftestSide + self.bottomestSide + self.direction

    def generate_ray(self, x, y):
        rightInterpolated = (-self.leftestSide*2*x)
        upInterpolated = (-self.bottomestSide*2*y)
        newDirection: vec3 = self.bottomLeftCorner + rightInterpolated + upInterpolated
        return Ray(self.center, newDirection.normalize())
