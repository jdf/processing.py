class Shape3D(object):

    def __init__(self, x=0, y=0, z=0):
        self.locationX = x
        self.locationY = y
        self.locationZ = z

    def setLocation(self, x, y, z):
        self.locationX = x
        self.locationY = y
        self.locationZ = z

    # Override if you need these.
    def rotX(self, theta):
        pass

    def rotY(self, theta):
        pass

    def rotZ(self, theta):
        pass
