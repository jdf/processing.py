"""
mpeano.py by Martin Prout 
LSystem rules from The Euclidean Traveling Salesman Problem.... by MG Norman & P Moscato. 
Features a scaling adjustment and turtle reversing, use trignometry rather than processing affine 
transforms to calculate the line, uses a grammar module to create production string.
"""

import math
import grammar

# some globals
XPOS = 0
YPOS = 1
ANGLE = 2
DELTA = math.pi/4

RULES = {
'F' : '',
'Y': 'FFY',
'X' : '+!X!FF-BQFI-!X!FF+',
'A' : 'BQFI',
'B' : 'AFF' 
}

AXIOM = 'XFF2-AFF2-XFF2-AFF'
 
def render(production):
    """
    Render evaluates the production string and calls draw_line
    """
    global DELTA
    distance = 15
    turtle = [width/10, height/10, -DELTA]
    repeat = 1
    for val in production:
        if val == "F": 
            turtle = draw_line(turtle, distance)
        elif val == "+": 
            turtle[ANGLE] += DELTA * repeat
            repeat = 1
        elif val == "-": 
            turtle[ANGLE] -= DELTA * repeat
            repeat = 1
        elif val == "I": 
          distance *= 1/math.sqrt(2)
        elif val == "Q": 
            distance *= math.sqrt(2)
        elif val == "!":             
            DELTA = -DELTA        
        elif (val == '2'):
            repeat = 2   
        else: 
            pass


def draw_line(turtle, length):
    """
    Draw line utility uses processing 'line' function to draw lines
    """
    turtlecopy = []
    turtlecopy[:] = turtle
    turtlecopy[XPOS] = turtle[XPOS] + length * math.cos(turtle[ANGLE])
    turtlecopy[YPOS] = turtle[YPOS] - length * math.sin(turtle[ANGLE])
    line(turtle[XPOS], turtle[YPOS], turtlecopy[XPOS], turtlecopy[YPOS])
    return turtlecopy     


def setup():
    """
    The processing setup statement
    """
    size(600, 600)
    production = grammar.repeat(6, AXIOM, RULES)
    background(0, 0, 255)
    smooth()
    stroke(255, 255, 0)
    strokeWeight(3)
    render(production)    
    saveFrame("mpeano.png")

def draw():
    """
    An empty processing draw statement seems to be required to prevent premature exit()?
    """
    pass 
 
