"""
sierpinski.py is adapted for python by Martin Prout 
A very simple lsystem example, which uses a grammar module
to create the production string
"""

import math
import grammar

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
DELTA = math.pi*2/3

RULES = {
	'F': 'FF',
	'X' : '-FXF+FXF+FXF-'
}
AXIOM = 'FX'

def render(production):        
    """
    Render evaluates the production string and calls __drawLine
    """
    distance = 1.7
    turtle = [width/12, height/12, -DELTA]
    for val in production:
        if val == "F": 
            turtle = __drawLine(turtle, distance)
        elif val == "+": 
            turtle[ANGLE] += DELTA
        elif val == "-": 
            turtle[ANGLE] -= DELTA
        elif val == 'X':  # used to confirm 'X' is recognized grammar
            pass    
        else:             # check on unknown grammar in RULES
            print "Unknown grammar %s" % val
        
def __drawLine(turtle, length):
    """
    private draw line function
    returns a turtle at the new position
    """
    turtlecopy = []
    turtlecopy[:] = turtle
    turtlecopy[XPOS] = turtle[XPOS] + length * math.cos(turtle[ANGLE])
    turtlecopy[YPOS] = turtle[YPOS] + length * math.sin(turtle[ANGLE])
    line(turtle[XPOS], turtle[YPOS], turtlecopy[XPOS], turtlecopy[YPOS])
    return turtlecopy    
    
def setup():
    """
    Is the processing setup function
    """
    size(500, 500)
    background(0)
    stroke(255)
    production = grammar.repeat(7, AXIOM, RULES)
    translate(width*0.9, height*0.9) 
    render(production)  
    
def draw():
    """
    Is the processing draw loop
    """
    pass 
