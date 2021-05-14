import Camera as Camera
from Vector3 import Vector3
from Ray import Ray


class OrthographicCamera(Camera):
    def __init__(self, center: Vector3, direction: Vector3, up: Vector3, size):
        self.center = center
        self.direction = direction
        self.up = up
        self.size = size

    def Generate_ray(self, x: float, y: float):
        pos = self.center + (x - 0.5) * self.size * self.right + (y - 0.5) * self.siz * self.up
        return Ray(pos, self.direction)
