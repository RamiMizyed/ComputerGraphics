import Vector3


class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(self, ray: Vector3, hit: Vector3, tmin):
        pass
