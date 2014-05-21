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
    # Draw a line using the global variable "a"
    line(a, 0, a, height)

    # Create a variable "a" local to the for() statement
    for a in range(120, 200, 2):
        line(a, 0, a, height)

    # Create a variable "a" local to the draw() function
    a = 300
    # Draw a line using the local variable "a"
    line(a, 0, a, height)

    # Make a call to the custom function drawAnotherLine()
    drawAnotherLine()

    # Make a call to the custom function setYetAnotherLine()
    drawYetAnotherLine()


def drawAnotherLine():
    # Create a variable "a" local to this method
    a = 320
    # Draw a line using the local variable "a"
    line(a, 0, a, height)


def drawYetAnotherLine():
    # Because no local variable "a" is set,
    # this lines draws using the original global
    # variable "a" which is set to the value 20.
    line(a + 2, 0, a + 2, height)

