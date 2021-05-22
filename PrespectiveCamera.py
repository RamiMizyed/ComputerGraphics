from Camera import Camera
class PerspectiveCamera(Camera):

    def __init__(self, center, direction, up, angle):
        self.center = center
        self.direction = direction
        self.up = up
        self.angle = angle

    def generateRay(self,x ,y):
        pass



    