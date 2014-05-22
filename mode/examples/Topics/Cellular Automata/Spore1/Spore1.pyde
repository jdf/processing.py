"""
Spore 1 
by Mike Davis. 

A short program for alife experiments. Click in the window to restart.
Each cell is represented by a pixel on the display as well as an entry in
the array 'cells'. Each cell has a run() method, which performs actions
based on the cell's surroundings.    Cells run one at a time (to avoid conflicts
like wanting to move to the same space) and in random order.
"""

from cell import Cell
from world import World

w = None
numcells = 0
maxcells = 6700
cells = []
spore_color = None
# set lower for smoother animation, higher for faster simulation
runs_per_loop = 10000
black = color(0, 0, 0)


def setup():
    size(640, 360)
    frameRate(24)
    reset()


def reset():
    clearScreen()
    w = World()
    spore_color = color(172, 255, 128)
    seed()


def seed():
    # Add cells at random places
    for i in range(maxcells):

        cX = int(random(width))
        cY = int(random(height))
        if w.getpix(cX, cY) == black:
            w.setpix(cX, cY, spore_color)
            cells.append(Cell(cX, cY))
            numcells += 1


def draw():
    # Run cells in random order
    for i in range(runs_per_loop):
        selected = min(int(random(numcells)), numcells - 1)
        cells[selected].run()


def clearScreen():
    background(0)

