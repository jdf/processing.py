"""
LoadFile 2

This example loads a data file about cars. Each element is separated
with a tab and corresponds to a different aspect of each car. The file stores
the miles per gallon, cylinders, displacement, etc., for more than 400 different
makes and models. Press a mouse button to advance to the next group of entries.
"""

from collections import namedtuple

Record = namedtuple('Record', ["name",
                               "mpg",
                               "cylinders",
                               "displacement",
                               "horsepower",
                               "weight",
                               "acceleration",
                               "year",
                               "origin"])
records = []
NUM = 9  # Display this many entries on each screen.
starting_entry = 0  # Display from this entry number

def setup():
    size(200, 200)
    fill(255)
    noLoop()

    body_font = loadFont("TheSans-Plain-12.vlw")
    textFont(body_font)

    lines = loadStrings("cars2.tsv")
    for l in lines:
        pieces = l.split(TAB)  # Load data into array
        if len(pieces) == 9:
            println(pieces)
            records.append(Record(*pieces))


def draw():
    background(0)
    for i in range(NUM):
        this_entry = starting_entry + i
        if this_entry < len(records):
            entry_text = "{} > {}".format(this_entry, records[this_entry].name)
            text(entry_text, 20, 20 + i * 20)


def mousePressed():
    global starting_entry
    starting_entry += NUM
    if starting_entry > len(records):
        starting_entry = 0  # go back to the beginning
    redraw()
