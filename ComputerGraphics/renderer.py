from hit import Hit
from ray import Ray
from Lights import *
from builtins import map
from PIL import Image
from tqdm import tqdm
from mathUtil import *
from cgtypes import *


class Renderer:
    def __init__(self, group, camera, lights, resolutionX, resolutionY, bgColor, ambientColor, max_depth=2):
        self.group = group
        self.camera = camera
        self.lights = lights
        self.resolutionX = resolutionX
        self.resolutionY = resolutionY
        self.bgColor = bgColor
        self.ambientColor = ambientColor
        self.max_depth = max_depth

    def trace_ray(self, ray: Ray, hit: Hit, weight, depth):
        if depth >= self.max_depth:
            return [0, 0, 0]

        self.group.intersect(ray, hit, 0.0001)

        if not hit.intersect:
            return self.bgColor

        fColor = list(map(mul, self.ambientColor, hit.material.diffuseColor))

        for light in self.lights:
            shadowRayDir = -light.direction
            shadowRay = Ray(hit.point, shadowRayDir)
            shadowHit = Hit()
            self.group.intersect(shadowRay, shadowHit, 0.0001)

            if shadowHit.intersect:
                continue

            fColor = list(map(add, fColor, hit.material.shade(ray, hit, light)))

        # Reflection Calculation
        R = ray.direction.reflect(hit.normal)
        reflectionRay = Ray(hit.point, R)
        reflectionHit = Hit()
        tracedColorReflection = self.trace_ray(reflectionRay, reflectionHit, weight-0.05, depth+1)
        tmpColor = list(map(mul, hit.material.reflectiveColor, tracedColorReflection))
        fColor = list(map(add, fColor, tmpColor))

        # Refractive Calculations
        refractDir = refract(ray.direction, hit.normal, hit.material.indexOfRefraction)
        refractedRay = Ray(hit.point, refractDir)
        tracedColorRefraction = self.trace_ray(refractedRay, Hit(), weight - 0.05, depth+1)
        tmpColor = list(map(mul, hit.material.transparentColor, tracedColorRefraction))
        fColor = list(map(add, fColor, tmpColor))

        return list(map(mul, fColor, [weight]*3))

    def render(self, filename):
        img = Image.new("RGB", (self.resolutionX, self.resolutionY))
        pixels = img.load()

        for y in range(self.resolutionY):
            for x in range(self.resolutionX):
                pixels[x, y] = tuple(map(mul_int, self.bgColor, [255]*3))

        invXRes = 1 / self.resolutionX
        invYRes = 1 / self.resolutionY

        for y in tqdm(range(self.resolutionY), desc="Render Loop"):
            yy = y * invYRes
            for x in range(self.resolutionX):
                xx = x * invXRes

                ray = self.camera.generate_ray(xx, yy)
                hit = Hit()
                finalColor = self.trace_ray(ray, hit, 1, 0)
                if hit.intersect:
                    pixels[x, self.resolutionY - y - 1] = tuple(map(mul_int, finalColor, [255]*3))

        img.save(filename, format="JPEG")

    def render_depth(self, filename, near, far):
        img = Image.new("RGB", (self.resolutionX, self.resolutionY), "black")
        pixels = img.load()

        for y in range(self.resolutionY):
            for x in range(self.resolutionX):
                pixels[x, y] = tuple(map(mul_int, self.bgColor, [255]*3))

        for y in tqdm(range(self.resolutionY), desc="DepthRender", colour="White"):
            yy = y / self.resolutionY
            for x in range(self.resolutionX):
                xx = x / self.resolutionX

                ray = self.camera.generate_ray(xx, yy)
                hit = Hit()
                self.trace_ray(ray, hit, 1, 0)
                if hit.intersect is True:
                    depth_1 = (far - hit.t) / (far - near)
                    depth = int(depth_1 * 255)
                    pixels[x, self.resolutionY - y - 1] = tuple([depth]*3)

        img.save(filename, format="JPEG")
