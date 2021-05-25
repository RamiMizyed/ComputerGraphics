import math

from Vector3Math import Vector3
from RayHit import Ray


class Camera:
    def Generate_ray(self, x, y):
        pass


class OrthographicCamera(Camera):
    def __init__(self, center: Vector3, direction: Vector3, up: Vector3, size):
        self.center = center
        self.direction = direction
        self.up = up
        self.size = size
        self.right = direction.cross(up)

    def Generate_ray(self, x: float, y: float):
        pos = self.center + (x - 0.5) * self.size * self.right + (y - 0.5) * self.size * self.up
        return Ray(pos, self.direction)


class PerspectiveCamera(Camera):

    def __init__(self, center: Vector3, direction: Vector3, up: Vector3, angle):
        self.center = center
        self.direction = direction
        self.up = up
        self.angle = angle
        self.right: Vector3 = direction.cross(up)
        angleRadians: float = self.angle * math.pi/180
        muqabil = math.tan(angleRadians/2)
        self.leftestSide = muqabil * -self.right
        self.bottomestSide = muqabil * -self.up
        self.bottomLeftCorner = self.leftestSide + self.bottomestSide + self.direction

    def Generate_ray(self, x, y):
        rightInterpolated = (-self.leftestSide*2*x)
        upInterpolated = (-self.bottomestSide*2*y)
        newDirection: Vector3 = self.bottomLeftCorner + rightInterpolated + upInterpolated
        return Ray(self.center, newDirection.normal())







