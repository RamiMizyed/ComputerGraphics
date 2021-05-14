import Vector3


class Hit:
    def __init__(self, normal: Vector3):
        self.t = 0
        self.color = [0,0,0]
        self.normal = normal

