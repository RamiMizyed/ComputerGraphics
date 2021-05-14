# Name : Rami Mizyed
# Date: 14-may-2021


# imports
import json
from PIL import Image

# main render function takes a json file with needed information


def Render(filename, camera, group, background):
    resX = 500
    resY = 500
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()
