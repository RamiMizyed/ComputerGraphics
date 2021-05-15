import Object3D


class Transformation(Object3D):

    def __init__(self, m, object):
        self.m = m
        self.object = object
