# The World class simply provides two functions, 'get' and 'set',
# which access the display in the same way as 'getPixel' and 'setPixel'. The
# only difference is that the World class's 'get' and 'set' do screen
# wraparound ("toroidal coordinates").


class World(object):

    def setpix(self, x, y, c):
        while(x < 0):
            x += width
        while(x > width - 1):
            x -= width
        while(y < 0):
            y += height
        while(y > height - 1):
            y -= height
        set(x, y, c)

    def getpix(self, x, y):
        while(x < 0):
            x += width
        while(x > width - 1):
            x -= width
        while(y < 0):
            y += height
        while(y > height - 1):
            y -= height
        return get(x, y)

