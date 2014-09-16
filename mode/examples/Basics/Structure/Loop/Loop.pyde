"""
Loop. 

The loop() function causes draw() to execute
repeatedly. If noLoop is called in setup()
the draw() is only executed once. In this example
click the mouse to execute loop(), which will
cause the draw() to execute repeatedly. 
"""
y = 100


def setup():
    """
    The statements in the setup() function
    run once when the program begins.
    """
    size(640, 360)    # Size should be the first statement
    stroke(255)       # Set stroke color to white
    noLoop()
    y = height * 0.5


def draw():
    """
    The statements in draw() are run until the
    program is stopped. Each statement is run in
    sequence and after the last line is read, the first
    line is run again.
    """
    global y
    background(0)     # Set the background to black
    line(0, y, width, y)
    y = y - 1
    if y < 0:
        y = height


def mousePressed():
    loop()

