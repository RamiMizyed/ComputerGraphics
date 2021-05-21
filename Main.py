# Name : Rami Mizyed
# Date: 14-may-2021


# imports
import json
from PIL import Image
from Object3D import Object3D
from Orthographic_Camera import OrthographicCamera
from Hit import Hit
from Sphere import Sphere
from Group import Group
from Vector3 import *


# main render function takes a json file with needed information


def Render(filename, camera, group, background):
    resX = 500
    resY = 500
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple(background)

    for y in range(resY):
        yy = y / resY
        for x in range(resX):
            xx = x / resX
            ray = camera.Generate_ray(xx, yy)
            hit = Hit()
            for object in group.objects:
                object.intersect(ray, hit, 0.0)
                if hit.t > 0:
                    pixels[x, y] = tuple(hit.color)

    img.save(filename, format="JPEG")


def RenderDepth(filename, camera, group, background, near, far):
    resX = 500
    resY = 500

    img = Image.new("RGB", (resX, resY), "black")
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple(background)

    
