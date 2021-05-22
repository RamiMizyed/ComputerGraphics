from Vector3 import Vector3
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
        self.right = Vector3.cross(direction, up)

    def Generate_ray(self, x: float, y: float):
        pos = self.center + (x - 0.5) * self.size * self.right + (y - 0.5) * self.size * self.up
        return Ray(pos, self.direction)


class PerspectiveCamera(Camera):

    def __init__(self, center, direction, up, angle):
        self.center = center
        self.direction = direction
        self.up = up
        self.angle = angle

    def generateRay(self, x, y):
        pass
