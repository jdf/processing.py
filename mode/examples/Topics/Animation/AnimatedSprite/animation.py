# Class for animating a sequence of GIFs
class Animation(object):

    def __init__(self, imagePrefix, count):
        self.frame = 0
        self.imageCount = count
        self.images = [PImage] * self.imageCount
        for i in range(self.imageCount):
            # Use nf() to number format 'i' into four digits
            filename = imagePrefix + nf(i, 4) + ".gif"
            self.images[i] = loadImage(filename)

    def display(self, xpos, ypos):
        self.frame = (self.frame + 1) % self.imageCount
        image(self.images[self.frame], xpos, ypos)

    def getWidth(self):
        return self.images[0].width
