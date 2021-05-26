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
from tqdm import tqdm
from Lights import *
from cgtypes import *

resX = 300
resY = 300


# main render function takes a json file with needed information
def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def mulI(x, y):
    return int(x * y)


def Render(filename, camera, group, background, light: DirectionalLight, ambient):
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
                if hit.t > 0 and hit.intersect is True:
                    transposeM: mat4 = object.transformationMatrix.inverse().transpose()

                    normalTransposed: vec3 = (transposeM * hit.normal).normalize()

                    lightDir = vec3(-light.direction.x, -light.direction.y, -light.direction.z).normalize()
                    lightIntensity = max(normalTransposed * lightDir, 0)
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
                if hit.t > 0 and hit.intersect is True:
                    depth_1 = (far - hit.t) / (far - near)
                    depth = int(depth_1 * 255)
                    pixels[x, resY - y - 1] = tuple([depth, depth, depth])

    img.save(filename, format="JPEG")


def RenderScene(scene, near, far):
    with open("Data/" + scene + '.json') as f:
        data = json.load(f)
    lightDirection = data["light"]["direction"]
    lightDirectionVec = vec3(lightDirection[0], lightDirection[1], lightDirection[2])
    lightColor = data["light"]["color"]
    light: DirectionalLight = DirectionalLight(lightDirectionVec, lightColor)
    ambient = data["background"]["ambient"]

    if "orthocamera" in data.keys():
        camPos = data['orthocamera']['center']
        camVec = vec3(camPos[0], camPos[1], camPos[2])
        camDir = data['orthocamera']['direction']
        camDirVec = vec3(camDir[0], camDir[1], camDir[2])
        camUp = data['orthocamera']['up']
        camUpVec = vec3(camUp[0], camUp[1], camUp[2])
        size = data['orthocamera']['size']
        camera = OrthographicCamera(camVec, camDirVec, camUpVec, size)
    elif "perspectivecamera" in data.keys():
        camPos = data['perspectivecamera']['center']
        camVec = vec3(camPos[0], camPos[1], camPos[2])
        camDir = data['perspectivecamera']['direction']
        camDirVec = vec3(camDir[0], camDir[1], camDir[2])
        camUp = data['perspectivecamera']['up']
        camUpVec = vec3(camUp[0], camUp[1], camUp[2])
        angle = data['perspectivecamera']['angle']
        camera = PerspectiveCamera(camVec, camDirVec, camUpVec, angle)

    background = data['background']['color']
    group = Group([0, 0, 0])
    for item in data['group']:
        finalMatrix = mat4(1.0)
        if 'transform' in item.keys():
            for transformation in item['transform']["transformations"]:
                if 'zrotate' in transformation.keys():
                    zrotate = transformation['zrotate']
                    zrotate = zrotate * math.pi / 180
                    mate = mat4(1.0)
                    zvec = vec3(0, 0, 1)
                    newRotatedMatrixZ = mate.rotation(zrotate, zvec)
                    finalMatrix = finalMatrix * newRotatedMatrixZ
                if 'xrotate' in transformation.keys():
                    xrotate = transformation['xrotate']
                    xrotate = xrotate * math.pi / 180
                    mate = mat4(1.0)
                    xvec = vec3(1, 0, 0)
                    newRotatedMatrixX = mate.rotation(xrotate, xvec)
                    finalMatrix = finalMatrix * newRotatedMatrixX
                if 'yrotate' in transformation.keys():
                    yrotate = transformation['yrotate']
                    yrotate = yrotate * math.pi / 180
                    mate = mat4(1.0)
                    yvec = vec3(0, 1, 0)
                    newRotatedMatrixY = mate.rotation(yrotate, yvec)
                    finalMatrix = finalMatrix * newRotatedMatrixY

                if 'scale' in transformation.keys():
                    mate = mat4(1.0)
                    transformations = transformation['scale']
                    transformations = vec3(transformations[0], transformations[1], transformations[2])
                    scaleMatrix = mate.scaling(transformations)
                    finalMatrix = finalMatrix * scaleMatrix
                if 'translate' in transformation.keys():
                    mate = mat4(1.0)
                    translate = transformation['translate']
                    translate = vec3(translate[0], translate[1], translate[2])
                    transMatrix = mate.translation(translate)
                    finalMatrix = finalMatrix * transMatrix
            item = item["transform"]["object"]
        objectTransformation = None
        if "sphere" in item.keys():
            sCenter = item['sphere']['center']
            sCenterVec = vec3(sCenter[0], sCenter[1], sCenter[2])
            radius = item['sphere']['radius']
            color = item['sphere']['color']
            objectTransformation = Transformation([0, 0, 0], finalMatrix, Sphere(sCenterVec, radius, color))
        elif "plane" in item.keys():
            normal = item['plane']['normal']
            normal = vec3(normal[0], normal[1], normal[2])
            offset = item['plane']['offset']
            color = item['plane']['color']
            objectTransformation = Transformation([0, 0, 0], finalMatrix, Plane(normal, offset, color))
        elif "triangle" in item.keys():
            v1 = item["triangle"]["v1"]
            v1 = vec3(v1[0], v1[1], v1[2])
            v2 = item["triangle"]["v2"]
            v2 = vec3(v2[0], v2[1], v2[2])
            v3 = item["triangle"]["v3"]
            v3 = vec3(v3[0], v3[1], v3[2])
            color = item['triangle']['color']
            objectTransformation = Transformation([0, 0, 0], finalMatrix, Triangle(v1, v2, v3, color))
        group.add(objectTransformation)
    Render("Render/" + scene + '.jpg', camera, group, background, light, ambient)
    RenderDepth("Render/" + scene + "_depth.jpg", camera, group, background, near, far)


print("Started")
RenderScene('scene1_diffuse', 9, 11)
RenderScene('scene2_ambient', 8, 11.5)
RenderScene('scene3_perspective', 8, 11.5)
RenderScene('scene4_plane', 8, 11.5)
RenderScene('scene5_sphere_triangle', 8, 11.5)
RenderScene('scene6_squashed_sphere', 8, 11.5)
RenderScene('scene7_squashed_rotated_sphere', 8, 11.5)

print("Finished")
