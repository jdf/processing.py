"""
 * Setup and Draw.
 *
 * The code inside the draw() function runs continuously
 * from top to bottom until the program is stopped.
 """
y = 100


def setup():
    """
    The statements in the setup() function
    execute once when the program begins
    """
    size(640, 360)    # Size must be the first statement
    stroke(255)         # Set line drawing color to white
    frameRate(30)


def draw():
    """
    The statements in draw() are executed until the
    program is stopped. Each statement is executed in
    sequence and after the last line is read, the first
    line is executed again.
    """
    global y
    background(0)     # Set the background to black
    y = y - 1
    if y < 0:
        y = height

    line(0, y, width, y)

