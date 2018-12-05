"""
#
# Spore 1
# by Mike Davis.
# Python version by Berin
#
# A short program for alife experiments. Click in the window to restart.
# Each cell is represented by a pixel on the display as well as an entry in
# the array 'cells'. Each cell has a run() method, which performs actions
# based on the cell's surroundings.  Cells run one at a time (to avoid conflicts
# like wanting to move to the same space) and in random order.
#
"""

SPORE_COLOR = color(172, 255, 128)

BLACK = color(0)
MAX_CELLS = 6700
CELLS = []
RUNS_PER_LOOP = 10000

def reset():
    background(BLACK)
    seed()

def seed():
    global CELLS

    CELLS = []
    for i in range(MAX_CELLS):
        x = int(random(width))
        y = int(random(height))

        if world.has_black_pixel(x, y):
            world.set_pixel(x, y, SPORE_COLOR)
            CELLS.append(Cell(x, y))

def setup():
    size(640, 360)
    frameRate(24)
    reset()

def draw():
    for i in range(RUNS_PER_LOOP):
        cell_index = int(random(len(CELLS)))
        CELLS[cell_index].run()


def parse_coord(x, y):
    while x < 0:
        x += width
    while x > (width - 1):
        x -= width
    while y < 0:
        y += height
    while y > (height - 1):
        y -= height

    return x, y


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self):
        """
        Perform action based on surroundings
        """

        # Fix cell coordinates
        self.x, self.y = parse_coord(self.x, self.y)
        x, y = self.x, self.y

        # Cell instructions
        if world.has_black_pixel(x + 1, y):
            self.move(0, 1)
        elif not world.has_black_pixel(x, y - 1) and not world.has_black_pixel(x, y + 1):
            self.move(int(random(9)) - 4, int(random(9)) - 4)

    def move(self, dx, dy):
        """
        Will move the cell (dx, dy) units if that space is empty
        """
        new_x, new_y = self.x + dx, self.y + dy

        if world.has_black_pixel(new_x, new_y):
            world.set_pixel(new_x, new_y, SPORE_COLOR)
            world.set_pixel(self.x, self.y, BLACK)
            self.x, self.y = new_x, new_y


class World(object):
    """
    The World class simply provides two functions, get and set, which access the
    display in the same way as getPixel and setPixel.  The only difference is that
    the World class's get and set do screen wraparound ("toroidal coordinates").
    """

    def __init__(self):
        self.pixels = {}

    def set_pixel(self, x, y, value):
        x, y = parse_coord(x, y)
        self.pixels[(x, y)] = value
        set(x, y, value)

    def get_pixel(self, x, y):
        x, y = parse_coord(x, y)
        return get(x, y)

    def has_black_pixel(self, x, y):
        return self.get_pixel(x, y) == BLACK

world = World()


def mousePressed():
    reset()