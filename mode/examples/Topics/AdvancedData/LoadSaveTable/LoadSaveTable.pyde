"""
Loading Tabular Data
by Daniel Shiffman.  

This example demonstrates how to use loadTable()
to retrieve data from a CSV file and make objects 
from that data.
Here is what the CSV looks like:

x,y,diameter,name
160,103,43.19838,Happy
372,137,52.42526,Sad
273,235,61.14072,Joyous
121,179,44.758068,Melancholy
"""
from Bubble import Bubble

# A list of Bubble objects
bubbles = []


def setup():
    size(640, 360)
    loadData()


def draw():
    background(255)
    # Display all bubbles
    for b in bubbles:
        b.display()
        b.rollover(mouseX, mouseY)

    textAlign(LEFT)
    fill(0)
    text("Click to add bubbles.", 10, height - 10)


def loadData():
    # Load CSV file into a Table object
    global table
    global bubbles
    # "header" option indicates the file has a header row
    table = loadTable("data.csv", "header")
    bubbles = []

    for row in table.rows():
        # You can access the fields via their column name (or index)
        x = row.getFloat("x")
        y = row.getFloat("y")
        d = row.getFloat("diameter")
        n = row.getString("name")
        # Make a Bubble object out of the data read
        bubbles.append(Bubble(x, y, d, n))


def mousePressed():
    global table
    # Create a new row
    row = table.addRow()
    # Set the values of that row
    row.setFloat("x", mouseX)
    row.setFloat("y", mouseY)
    row.setFloat("diameter", random(40, 80))
    row.setString("name", "Blah")

    # If the table has more than 10 rows
    if table.getRowCount() > 10:
        # Delete the oldest row
        table.removeRow(0)

    # Writing the CSV back to the same file
    saveTable(table, "data/data.csv")
    # And reloading it
    loadData()
