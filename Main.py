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
        for x in range(resX):
            pass


