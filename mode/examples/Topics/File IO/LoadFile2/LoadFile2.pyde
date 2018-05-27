"""
LoadFile 2

This example loads a data file about cars. Each element is separated
with a tab and corresponds to a different aspect of each car. The file stores 
the miles per gallon, cylinders, displacement, etc., for more than 400 different
makes and models. Press a mouse button to advance to the next group of entries.
"""

from Record import *

RECORDS = []
RECORD_COUNT = 0
NUM = 9  # Display this many entries on each screen.
STARTING_ENTRY = 0  # Display from this entry number

def setup():
    global RECORDS, RECORD_COUNT
    size(200, 200)
    fill(255)
    noLoop()

    body_font = loadFont("TheSans-Plain-12.vlw")
    textFont(body_font)

    lines = loadStrings("cars2.tsv")
    for l in lines:
        pieces = l.split(TAB)  # Load data into array
        if len(pieces) == 9:
            RECORDS.append(Record(pieces))
            RECORD_COUNT += 1

    if RECORD_COUNT != len(RECORDS):
        RECORDS = RECORDS[:RECORD_COUNT]


def draw():
    background(0)
    for i in range(NUM):
        this_entry = STARTING_ENTRY + i
        if this_entry < RECORD_COUNT:
            entry_text = "{} > {}".format(this_entry, RECORDS[this_entry].name)
            text(entry_text, 20, 20 + i * 20)


def mousePressed():
    global STARTING_ENTRY
    STARTING_ENTRY += NUM
    if STARTING_ENTRY > len(RECORDS):
        STARTING_ENTRY = 0  # go back to the beginning
    redraw()
