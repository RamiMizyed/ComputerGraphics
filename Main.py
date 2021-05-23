# Name : Rami Mizyed
# Date: 14-may-2021


# imports
import json
from PIL import Image
from Cameras import *
from RayHit import *
from Objects import *
from Group import Group
from Vector3 import *
from tqdm import tqdm

# main render function takes a json file with needed information


def Render(filename, camera, group, background):
    resX = 500
    resY = 500
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple(background)

    for y in tqdm(range(resY)):
        yy = y / resY
        for x in range(resX):
            xx = x / resX
            ray = camera.Generate_ray(xx, yy)
            hit = Hit()
            for object in group.objects:
                object.intersect(ray, hit, 0.0)
                if hit.t > 0:
                    pixels[x, resY - y - 1] = tuple(hit.color)

    img.save(filename, format="JPEG")


def test():
    resX = 500
    resY = 500
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()
    for y in range(resY):
        for x in range(resX):
            pixels[x, resY - y - 1] = tuple([int((x * 255 / resX)), int(y * 255 / resY), 64])

    img.show()


def RenderDepth(filename, camera, group, background, near, far):
    resX = 500
    resY = 500

    img = Image.new("RGB", (resX, resY), "black")
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple(background)

    for y in tqdm(range(resY)):
        yy = y / resY
        for x in range(resX):

            xx = x / resX
            ray = camera.Generate_ray(xx, yy)
            hit = Hit()
            for object in group.objects:
                object.intersect(ray, hit, 0.0)
                if hit.t > 0:
                    depth_1 = (far - hit.t) / (far - near)
                    depth = int(depth_1 * 255)
                    pixels[x, resY - y - 1] = tuple([depth, depth, depth])

    img.save(filename, format="JPEG")


def RenderScene(scene, near, far):
    with open("Data/" + scene + '.json') as f:
        data = json.load(f)

    camPos = data['orthocamera']['center']
    camVec = Vector3(camPos[0], camPos[1], camPos[2])
    camDir = data['orthocamera']['direction']
    camDirVec = Vector3(camDir[0], camDir[1], camDir[2])
    camUp = data['orthocamera']['up']
    camUpVec = Vector3(camUp[0], camUp[1], camUp[2])
    size = data['orthocamera']['size']

    camera = OrthographicCamera(camVec, camDirVec, camUpVec, size)
    background = data['background']['color']

    group = Group([0, 0, 0])

    for item in data['group']:
        sCenter = item['sphere']['center']
        sCenterVec = Vector3(sCenter[0], sCenter[1], sCenter[2])
        radius = item['sphere']['radius']
        color = item['sphere']['color']
        group.add(Sphere(sCenterVec, radius, color))

    Render("Render/" + scene + '.jpg', camera, group, background)
    RenderDepth("Render/" + scene + "_depth.jpg", camera, group, background, near, far)


print("Started")
RenderScene('scene1', 9, 11)
RenderScene('scene2', 8, 11.5)
print("Finished")
