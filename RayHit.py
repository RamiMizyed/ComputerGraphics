import Vector3Math


class Ray:
    def __init__(self, origin: Vector3Math, direction: Vector3Math):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self):
        self.t = 0
        self.color = [0, 0, 0]
        self.normal: Vector3Math = Vector3Math
