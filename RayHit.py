import Vector3


class Ray:
    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self):
        self.t = 0
        self.color = [0, 0, 0]
        self.normal = Vector3
