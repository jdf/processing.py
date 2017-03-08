"""
LoadFile 2

This example loads a data file about cars. Each element is separated
with a tab and corresponds to a different aspect of each car. The file stores
the miles per gallon, cylinders, displacement, etc., for more than 400 different
makes and models. Press a mouse button to advance to the next group of entries.
"""

from Record import Record


def setup():
    global recordCount
    global records
    global num
    global startingEntry

    size(200, 200)
    fill(255)
    noLoop()

    body = loadFont("TheSans-Plain-12.vlw")
    textFont(body)

    num = 9  # Display this many entries on each screen.
    startingEntry = 0  # Display from this entry number
    recordCount = 0

    lines = loadStrings("cars2.tsv")
    records = []
    for line in xrange(len(lines)):
        pieces = split(lines[line], TAB)  # Load data array
        if len(pieces) == 9:
            records.insert(recordCount, Record(pieces))
            recordCount += 1


def draw():
    background(0)
    for i in xrange(num):
        thisEntry = startingEntry + i
        if thisEntry < recordCount:
            text(
                str(thisEntry) +
                " > " +
                records[thisEntry].name,
                20,
                20 +
                i *
                20)


def mousePressed():
    global startingEntry

    startingEntry += num
    if startingEntry > len(records):
        startingEntry = 0  # go back to the beginning

    redraw()
