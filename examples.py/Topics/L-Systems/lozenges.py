"""
lozenges.py by Martin Prout after a 'Fractint' sketch by Philippe Hurbain
You will need to wait a bit for this to render...
Features the use of dict of functions (as a pythonic version of switch)
Uses a grammar module to create production, and uses trignometry in place
of processing affine transforms to calculate the line coordinates. 
"""

import math
import grammar

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
DIST = 3
RED = color(200, 0, 0, 80)
YELLOW = color(200, 200, 0, 80)
DELTA = math.pi/5
PHI = (math.sqrt(5) - 1)/2
IPHI = 1/PHI

AXIOM = 'bX'

RULES = {
    'X' : '@+bF[|Y]2-F[|X][|+@GIX]3-[X]bF2-[Y]bF', 
    'Y' : '@2+[X]rF|+rF[|Y]-[Y]rF|+rF[|X]',
    'F' : 'G'
}

# some module variables

repeat = 1
stack = []

##
# defining the actions as functions with a common signature
##

def __turnRight(pen):
    """
    private right turn function
    """
    global repeat
    pen[ANGLE] += DELTA * repeat
    repeat = 1
    return pen
    
def __turnLeft(pen):
    """
    private left turn function
    """
    global repeat
    pen[ANGLE] -= DELTA * repeat
    repeat = 1
    return pen 
    
def __reverse(pen):
    """
    private reverse direction
    """
    pen[ANGLE] += math.pi
    return pen
    
def __twiceRepeat(pen):
    """
    private set repeat to 2
    """
    global repeat
    repeat = 2
    return pen
    
def __thriceRepeat(pen):
    """
    private set repeat to 3
    """
    global repeat
    repeat = 3
    return pen  
    
def __drawLine(pen):
    """
    private draw line function uses processing 'line' function to draw lines
    takes pen dictionary input returns a pen with new position
    """
    pencopy = []
    pencopy[:] = pen
    pencopy[XPOS] = pen[XPOS] + pen[DIST] * math.cos(pen[ANGLE])
    pencopy[YPOS] = pen[YPOS] + pen[DIST] * math.sin(pen[ANGLE])
    line(pen[XPOS], pen[YPOS], pencopy[XPOS], pencopy[YPOS])
    return pencopy
    
def __moveForward(pen):
    """
    private move forward without drawing lines
    takes pen dictionary input returns a pen with new position
    """
    stroke(YELLOW)
    pencopy = []
    pencopy[:] = pen
    pencopy[XPOS] = pen[XPOS] + pen[DIST] * math.cos(pen[ANGLE])
    pencopy[YPOS] = pen[YPOS] + pen[DIST] * math.sin(pen[ANGLE])
    return pencopy  
    
def __reduceLength(pen): 
    """
    reduce length by dividing by the golden ratio
    """
    pen[DIST] *= IPHI
    return pen
    
def __increaseLength(pen):
    """
    increase length by multiplying by the golden ratio
    """ 
    pen[DIST] *= PHI
    return pen
    
def __setColorRed(pen):
    """
    using processing stroke function directly
    """ 
    stroke(RED)
    return pen      
    
def __setColorYellow(pen):
    """
    using processing stroke function directly
    """
    stroke(YELLOW)
    return pen
    
def __pushStack(pen):
    """
    surprisingly you can push to the module stack without calling global
    in the absence of a convenient list copy function, create a new list
    """
    pencopy = []
    pencopy[:] = pen
    stack.append(pencopy)
    return pen
    
def __popStack(pen):
    """
    you can also pop from the module stack without calling global
    NB: the pen parameter is only required for signature consistency 
    """
    return stack.pop()
    
####
# A dictionary of lsystem operations 
####

lsys_op ={
    '+' : __turnRight,
    '-' : __turnLeft,
    '|' : __reverse,
    '2' : __twiceRepeat,
    '3' : __thriceRepeat,
    'F' : __drawLine,
    'G' : __moveForward,
    '@' : __increaseLength,
    'I' : __reduceLength,
    'b' : __setColorRed,
    'r' : __setColorYellow,
    '[' : __pushStack,
    ']' : __popStack    
}

def evaluate(key, pen):
    """
    Is a wrapper controlling access to the dict of functions
    """
    if lsys_op.has_key(key):
        pen = lsys_op[key](pen)
    else:
        if not RULES.has_key(key): # for debugging you could comment out this line
            print "Unknown rule %s" % key # key is a substituted key without an action 
    return pen  


def render(production):        
    """
    Render evaluates the production string and calls evaluate which
    draws the lines etc
    """
    pen = [0, height/2, 0, 1000]
    for rule in production:
        pen = evaluate(rule, pen)       
   
    
def setup():
    """
    The processing setup statement
    """
    size(600, 600)
    production = grammar.repeat(7, AXIOM, RULES) 
    background(100, 0, 0)
    smooth()
    strokeWeight(3)
    stroke(YELLOW)
    render(production)
    
    
def draw():
    """
    Required to prevent premature death of script
    """
    pass
   

