# Name : Rami Mizyed
# Date: 14-may-2021


# imports
import json
from builtins import map

from PIL import Image
from Cameras import *
from RayHit import *
from Objects import *
from Group import Group
from Vector3Math import Vector3
from tqdm import tqdm
from Lights import *

resX = 1000
resY = 1000


# main render function takes a json file with needed information
def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def mulI(x, y):
    return int(x * y)


def Render(filename, camera, group, background, light : DirectionalLight, ambient):
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple([int(background[0] * 255), int(background[1] * 255), int(background[2] * 255)])

    for y in tqdm(range(resY), desc="Render Loop"):
        yy = y / resY
        for x in range(resX):
            xx = x / resX
            ray = camera.Generate_ray(xx, yy)
            hit = Hit()
            for object in group.objects:
                object.intersect(ray, hit, 0.0)
                if hit.t > 0:
                    lightDir = Vector3(-light.direction.x, -light.direction.y, -light.direction.z).normal()
                    lightIntensity = max(hit.normal.dot(lightDir), 0)
                    ambientColor = tuple(map(mul, hit.color, ambient))
                    diffuseColor = tuple(map(mul, hit.color, light.color))
                    diffuseColor = tuple(map(mul, diffuseColor, [lightIntensity, lightIntensity, lightIntensity]))
                    finalColor = list(map(add, ambientColor, diffuseColor))
                    pixels[x, resY - y - 1] = tuple(map(mulI, finalColor, [255, 255, 255]))

    img.save(filename, format="JPEG")


def test():
    img = Image.new("RGB", (resX, resY))
    pixels = img.load()
    for y in range(resY):
        for x in range(resX):
            pixels[x, resY - y - 1] = tuple([int((x * 255 / resX)), int(y * 255 / resY), 64])

    img.show()


def RenderDepth(filename, camera, group, background, near, far):
    img = Image.new("RGB", (resX, resY), "black")
    pixels = img.load()

    for y in range(resY):
        for x in range(resX):
            pixels[x, y] = tuple([int(background[0] * 255), int(background[1] * 255), int(background[2] * 255)])

    for y in tqdm(range(resY), desc="DepthRender", colour="White"):
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
    lightDirection = data["light"]["direction"]
    lightDirectionVec = Vector3(lightDirection[0], lightDirection[1], lightDirection[2])
    lightColor = data["light"]["color"]
    light: DirectionalLight = DirectionalLight(lightDirectionVec, lightColor)
    ambient = data["background"]["ambient"]

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

    Render("Render/" + scene + '.jpg', camera, group, background, light, ambient)
    RenderDepth("Render/" + scene + "_depth.jpg", camera, group, background, near, far)


print("Started")
RenderScene('scene1_diffuse', 9, 11)
RenderScene('scene2_ambient', 8, 11.5)
RenderScene('scene3_perspective', 8, 11.5)
print("Finished")
