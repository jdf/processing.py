"""
Variable Scope. 

Variables have a global or local "scope". 
For example, variables declared within either the
setup() or draw() functions may be only used in these
functions. Global variables, variables declared outside
of setup() and draw(), may be used anywhere within the program.
If a local variable is declared with the same name as a
global variable, the program will use the local variable to make 
its calculations within the current scope. Variables are localized
within each block. 
"""

a = 80  # Create a global variable "a"


def setup():
    size(640, 360)
    background(0)
    stroke(255)
    noLoop()


def draw():
    # Draw a line using the global variable "a".
    line(a, 0, a, height)

    # Create a variable "b" local to the draw() function.
    b = 100

    # Create a global variable "c".
    global c
    c = 320 # Since "c" is global, it is avalaible to other functions.
    # Make a call to the custom function drawGreenLine()
    drawGreenLine()

    # Draw a line using the local variable "b".
    line(b, 0, b, height)  # Note that "b" remains set to 100.


def drawGreenLine():
    # Since "b" was defined as a variable local to the draw() function,
    # this code inside this if statement will not run.
    if('b' in locals() or 'b' in globals()):
        background(255)  # This won't run
    else:
        with pushStyle():
            stroke(0, 255, 0)
            b = 320  # Create a variable "b" local to drawGreenLine().
            # Use the local variable "b" and the global variable "c" to draw a line.
            line(b, 0, c, height) 

