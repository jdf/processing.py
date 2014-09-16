"""
 * No Loop. 
 * 
 * The noLoop() function causes draw() to only
 * execute once. Without calling noLoop(), the 
 * code inside draw() is run continually. 
 """

y = 180

def setup():
    """ 
    The statements in the setup() function 
    execute once when the program begins
    """
    size(640, 360)    # Size should be the first statement
    stroke(255)         # Set line drawing color to white
    noLoop()


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
    if (y < 0):
        y = height
    line(0, y, width, y)

