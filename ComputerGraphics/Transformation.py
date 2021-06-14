from Objects import Object3D


class Transformation(Object3D):

    def __init__(self, m, object, material):
        super().__init__(material)
        self.m = m
        self.object = object
