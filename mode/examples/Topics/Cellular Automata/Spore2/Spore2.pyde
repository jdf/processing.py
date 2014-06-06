"""
Spore 2 
by Mike Davis. 

A short program for alife experiments. Click in the window to restart. 
Each cell is represented by a pixel on the display as well as an entry in
the array 'cells'. Each cell has a run() method, which performs actions
based on the cell's surroundings. Cells run one at a time (to avoid 
conflicts like wanting to move to the same space) and in random order. 
"""

w = None
maxcells = 8000
numcells = 0
cells = []
spore1 = color(128, 172, 255)
spore2 = color(64, 128, 255)
spore3 = color(255, 128, 172)
spore4 = color(255, 64, 128)
black = color(0, 0, 0)
# Set lower for smoother animation, higher for faster simulation.
runs_per_loop = 10000


def setup():
    size(640, 360)
    frameRate(24)
    reset()


def reset():
    clearScreen()
    w = World()
    numcells = 0
    seed()


def seed():
    # Add cells at random places.
    for i in range(maxcells):
        cX = int(random(width))
        cY = int(random(height))
        c = color(0)
        r = random(1)
        if r < 0.25:
            c = spore1
        elif r < 0.5:
            c = spore2
        elif r < 0.75:
            c = spore3
        else:
            c = spore4
        if w.getpix(cX, cY) == black:
            w.setpix(cX, cY, c)
            cells.append(Cell(cX, cY))
            numcells += 1


def draw():
    # Run cells in random order.
    for i in range(runs_per_loop):
        selected = min(int(random(numcells)), numcells - 1)
        cells[selected].run()


def clearScreen():
    background(0)


class Cell(object):

    def __init__(self, xin, yin):
        self.x = xin
        self.y = yin

    # Perform action based on surroundings.
    def run(self):
        # Fix cell coordinates
        while(self.x < 0):
            self.x += width
        while(self.x > width - 1):
            self.x -= width
        while(self.y < 0):
            self.y += height
        while(self.y > height - 1):
            self.y -= height
        # Cell instructions.
        myColor = w.getpix(self.x, self.y)
        if myColor == spore1:
            if w.getpix(self.x - 1, self.y + 1) == black and w.getpix(self.x + 1, self.y + 1) == black \
               and w.getpix(self.x, self.y + 1) == black:
                self.move(0, 1)
            elif w.getpix(self.x - 1, self.y) == spore2 and w.getpix(self.x - 1, self.y - 1) != black:
                self.move(0, -1)
            elif w.getpix(self.x - 1, self.y) == spore2 and w.getpix(self.x - 1, self.y - 1) == black:
                self.move(-1, -1)
            elif w.getpix(self.x + 1, self.y) == spore1 and w.getpix(self.x + 1, self.y - 1) != black:
                self.move(0, -1)
            elif w.getpix(self.x + 1, self.y) == spore1 and w.getpix(self.x + 1, self.y - 1) == black:
                self.move(1, -1)
            else:
                self.move(int(random(3)) - 1, 0)
        elif myColor == spore2:
            if w.getpix(self.x - 1, self.y + 1) == black and w.getpix(self.x + 1, self.y + 1) == black \
               and w.getpix(self.x, self.y + 1) == black:
                self.move(0, 1)
            elif w.getpix(self.x + 1, self.y) == spore1 and w.getpix(self.x + 1, self.y - 1) != black:
                self.move(0, -1)
            elif w.getpix(self.x + 1, self.y) == spore1 and w.getpix(self.x + 1, self.y - 1) == black:
                self.move(1, -1)
            elif w.getpix(self.x - 1, self.y) == spore2 and w.getpix(self.x - 1, self.y - 1) != black:
                self.move(0, -1)
            elif w.getpix(self.x - 1, self.y) == spore2 and w.getpix(self.x - 1, self.y - 1) == black:
                self.move(-1, -1)
            else:
                self.move(int(random(3)) - 1, 0)
        elif myColor == spore3:
            if w.getpix(self.x - 1, self.y - 1) == black and w.getpix(self.x + 1, self.y - 1) == black \
               and w.getpix(self.x, self.y - 1) == black:
                self.move(0, -1)
            elif w.getpix(self.x - 1, self.y) == spore4 and w.getpix(self.x - 1, self.y + 1) != black:
                self.move(0, 1)
            elif w.getpix(self.x - 1, self.y) == spore4 and w.getpix(self.x - 1, self.y + 1) == black:
                self.move(-1, 1)
            elif w.getpix(self.x + 1, self.y) == spore3 and w.getpix(self.x + 1, self.y + 1) != black:
                self.move(0, 1)
            elif w.getpix(self.x + 1, self.y) == spore3 and w.getpix(self.x + 1, self.y + 1) == black:
                self.move(1, 1)
            else:
                self.move(int(random(3)) - 1, 0)
        elif myColor == spore4:
            if w.getpix(self.x - 1, self.y - 1) == black and w.getpix(self.x + 1, self.y - 1) == black \
               and w.getpix(self.x, self.y - 1) == black:
                self.move(0, -1)
            elif w.getpix(self.x + 1, self.y) == spore3 and w.getpix(self.x + 1, self.y + 1) != black:
                self.move(0, 1)
            elif w.getpix(self.x + 1, self.y) == spore3 and w.getpix(self.x + 1, self.y + 1) == black:
                self.move(1, 1)
            elif w.getpix(self.x - 1, self.y) == spore4 and w.getpix(self.x - 1, self.y + 1) != black:
                self.move(0, 1)
            elif w.getpix(self.x - 1, self.y) == spore4 and w.getpix(self.x - 1, self.y + 1) == black:
                self.move(-1, 1)
            else:
                self.move(int(random(3)) - 1, 0)
                
                
    # Will move the cell (dx, dy) units if that space is empty.
    def move(self, dx, dy):
        if w.getpix(self.x + dx, self.y + dy) == black:
            w.setpix(self.x + dx, self.y + dy, w.getpix(self.x, self.y))
            w.setpix(self.x, self.y, color(0))
            self.x += dx
            self.y += dy


# The World class simply provides two functions, get and set, which access the
# display in the same way as getPixel and setPixel. The only difference is that
# the World class's get and set do screen wraparound ("toroidal coordinates").
class World(object):

    def setpix(self, x, y, c):
        while x < 0:
            x += width
        while x > width - 1:
            x -= width
        while y < 0:
            y += height
        while y > height - 1:
            y -= height
        set(x, y, c)

    def getpix(self, x, y):
        while x < 0:
            x += width
        while x > width - 1:
            x -= width
        while y < 0:
            y += height
        while y > height - 1:
            y -= height
        return get(x, y)


def mousePressed():
    reset()

