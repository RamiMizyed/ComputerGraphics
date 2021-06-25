from object3d import Object3D
from hit import Hit
from ray import Ray
from mathUtil import *

class Transformation(Object3D):
    def __init__(self, material, transformationMatrix: mat4, object3d):
        super().__init__(material)
        self.transformationMatrix = transformationMatrix
        self.object3d = object3d

    def intersect(self, ray: Ray, hit: Hit, tmin: float):
        invMat: mat4 = self.transformationMatrix.inverse()

        tOrigin = transform(ray.origin, invMat)
        tDirection = transform_normal(ray.direction, invMat).normalize()
        transformedRay = Ray(tOrigin, tDirection)

        objHitTest = Hit()
        self.object3d.intersect(transformedRay, objHitTest, tmin)
        if objHitTest.intersect:
            hitPointWorld = transform(objHitTest.point, self.transformationMatrix)
            tWorld = (hitPointWorld - ray.origin).length()

            if hit.t > tWorld > tmin:
                hit.point = hitPointWorld
                hit.normal = transform_normal(objHitTest.normal, invMat.transpose()).normalize()
                hit.t = tWorld
                hit.material = objHitTest.material
                hit.intersect = True
