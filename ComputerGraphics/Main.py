# Name : Rami Mizyed

import json
import math

from renderer import Renderer

from Material import *

# region Cameras
from perspectiveCamera import PerspectiveCamera
from orthographicCamera import OrthographicCamera
# endregion

# region Lights
from Lights import *
# endregion

# region Object Imports
from plane import Plane
from sphere import Sphere
from triangle import Triangle
from group import Group
from transformation import Transformation

# endregion

resX = 1000
resY = 1000


# main render function takes a json file with needed information


def render_scene(scene, near, far, max_depth):
    with open("Data/" + scene + '.json') as f:
        data = json.load(f)

    ambient = data["background"]["ambient"]
    background = data['background']['color']

    # region Lights
    lights = []
    if "light" in data.keys():
        light = data["light"]
        lightDirection = vec3(light["direction"]).normalize()
        lightColor = light["color"]
        lights.append(DirectionalLight(lightDirection, lightColor))
    elif "lights" in data.keys():
        for light in data['lights']:
            if 'directionalLight' in light.keys():
                lightInfo = light['directionalLight']
                lightDirection = vec3(lightInfo["direction"]).normalize()
                lightColor = lightInfo["color"]
                lights.append(DirectionalLight(lightDirection, lightColor))
    # endregion

    # region Cameras
    camera = None
    if "orthocamera" in data.keys():
        camPos = vec3(data['orthocamera']['center'])
        camDir = vec3(data['orthocamera']['direction']).normalize()
        camUp = vec3(data['orthocamera']['up']).normalize()
        size = data['orthocamera']['size']
        camera = OrthographicCamera(camPos, camDir, camUp, size)
    elif "perspectivecamera" in data.keys():
        camPos = vec3(data['perspectivecamera']['center'])
        camDir = vec3(data['perspectivecamera']['direction']).normalize()
        camUp = vec3(data['perspectivecamera']['up']).normalize()
        angle = data['perspectivecamera']['angle']
        camera = PerspectiveCamera(camPos, camDir, camUp, angle)
    # endregion

    # region Materials
    materials = []
    for material in data['materials']:
        if "phongMaterial" in material.keys():
            matInfo = dict(material['phongMaterial'])
            diffuseColor = matInfo.get('diffuseColor')
            specularColor = matInfo.get('specularColor')
            exponent = matInfo.get('exponent')
            transparentColor = matInfo.get('transparentColor')
            reflectiveColor = matInfo.get('reflectiveColor')
            ior = matInfo.get('indexOfRefraction')
            newMat = PhongMaterial(specularColor, exponent, diffuseColor, reflectiveColor, transparentColor, ior)
            materials.append(newMat)
    # endregion

    # region object parsing
    group = Group([0, 0, 0])
    for item in data['group']:
        objToAdd = None
        objInfo = item
        if 'transform' in item.keys():
            objInfo = item["transform"]["object"]

        if "sphere" in objInfo.keys():
            sCenter = vec3(objInfo['sphere']['center'])
            radius = objInfo['sphere']['radius']
            material = materials[objInfo['sphere']['material']]
            objToAdd = Sphere(sCenter, radius, material)
        elif "plane" in objInfo.keys():
            normal = vec3(objInfo['plane']['normal']).normalize()
            offset = objInfo['plane']['offset']
            material = materials[objInfo['plane']['material']]
            objToAdd = Plane(normal, offset, material)
        elif "triangle" in objInfo.keys():
            v1 = vec3(objInfo["triangle"]["v1"])
            v2 = vec3(objInfo["triangle"]["v2"])
            v3 = vec3(objInfo["triangle"]["v3"])
            material = materials[objInfo['triangle']['material']]
            objToAdd = Triangle(v1, v2, v3, material)

        finalMatrix = mat4(1.0)
        metrices = []
        if 'transform' in item.keys():
            for transformation in item['transform']["transformations"]:
                if 'zrotate' in transformation.keys():
                    zrotate = transformation['zrotate']
                    zrotate = zrotate * math.pi / 180
                    matrix = mat4(1.0).rotation(zrotate, vec3(0, 0, 1))
                    metrices.append(matrix)
                if 'xrotate' in transformation.keys():
                    xrotate = transformation['xrotate']
                    xrotate = xrotate * math.pi / 180
                    matrix = mat4(1.0).rotation(xrotate, vec3(1, 0, 0))
                    metrices.append(matrix)
                if 'yrotate' in transformation.keys():
                    yrotate = transformation['yrotate']
                    yrotate = yrotate * math.pi / 180
                    matrix = mat4(1.0).rotation(yrotate, vec3(0, 1, 0))
                    metrices.append(matrix)
                if 'scale' in transformation.keys():
                    scaleVec = vec3(transformation['scale'])
                    matrix = mat4(1.0).scaling(scaleVec)
                    metrices.append(matrix)
                if 'translate' in transformation.keys():
                    translateVec = vec3(transformation['translate'])
                    matrix = mat4(1.0).translation(translateVec)
                    metrices.append(matrix)

            for matrix in metrices:
                finalMatrix *= matrix
            objToAdd = Transformation(None, finalMatrix, objToAdd)

        group.add(objToAdd)
    # endregion

    renderer = Renderer(group, camera, lights, resX, resY, background, ambient, max_depth)
    renderer.render("Render/" + scene + '.jpg')
    # renderer.render_depth("Render/" + scene + "_depth.jpg", near, far)


if __name__ == "__main__":
    print("Started")
    render_scene('scene1_exponent_variations', 8, 11.5, 3)
    render_scene('scene2_plane_sphere', 8, 11.5, 3)
    render_scene('scene3_colored_lights', 8, 11.5, 3)
    render_scene('scene4_reflective_sphere', 8, 11.5, 3)
    render_scene('scene5_transparent_sphere', 8, 11.5, 3)
    render_scene('scene6_transparent_sphere2', 8, 11.5, 3)
    print("Finished")
