"""
stochastic_plant.py  by Martin Prout is a based on a ideas from "Algorithmic Beauty of Plants"
by Przemyslaw Prusinkiewicz & Aristid Lindenmayer.
Features a lsystem grammar module, that can parse both stochastic and non-stochastic rules,
or a mixture thereof. The format of the stochastic rules (as a dict of dict) is described in 
the grammar module header.
"""

from math import cos, pi, sin
from grammar import grammar

# some constants
XPOS = 0
YPOS = 1
ANGLE = 2
WEIGHT = 3
DELTA = pi/8
# A simple stochastic rule as a dict, with a dict of values (only one key)
# and 3 weighted alternative substitutions.
RULES = {  
    'F' : {'F[+F]F[-F]' : 10,
        'F[+F]F' : 45,
        'F[-F]F' : 45
    }
}

AXIOM = 'F'


def render(production):       
    """
    Render evaluates the production string and calls draw_line
    """
    pen = [width/2, height*0.95, pi/2, 4]
    stack = []
    repeat = 1
    for val in production:
        if val == "F": 
            strokeWeight(pen[WEIGHT])
            pen = draw_line(pen, 12)
        elif val == "+": 
            pen[ANGLE] += DELTA * repeat
        elif val == "-": 
            pen[ANGLE] -= DELTA * repeat
        elif val == "[": 
            temp = []
            temp[:] = pen # deep copy pen to temp
            temp[WEIGHT] = pen[WEIGHT] * 0.248 # reduce stroke weight
            stack.append(temp)
        elif val == "]": 
            pen = stack.pop() 
            pen[WEIGHT] *= 4            # almost restore stroke weight
        else: 
            pass
        
        
def draw_line(pen, length):
    """
    Draw line utility uses processing 'line' function to draw lines
    """
    pencopy = []
    pencopy[:] = pen
    pencopy[XPOS] = pen[XPOS] + length * cos(pen[ANGLE])
    pencopy[YPOS] = pen[YPOS] - length * sin(pen[ANGLE])
    strokeWeight(pen[WEIGHT])
    line(pen[XPOS], pen[YPOS], pencopy[XPOS], pencopy[YPOS])
    return pencopy     
    
    
def setup():
    """
    The processing setup statement
    """
    size(500, 500)
    background(200, 200, 0)
    stroke(0, 100, 0)
    plant0 = grammar.repeat(4, AXIOM, RULES)
    plant1 = grammar.repeat(5, AXIOM, RULES)    
    plant2 = grammar.repeat(4, AXIOM, RULES)
    render(plant1)
    translate(-100, 10)
    render(plant0)
    translate(200, 0)
    render(plant2)  
    print grammar.toRuleString(AXIOM, RULES)
    
    
def draw():
    """
    An empty processing draw statement required to prevent premature exit
    """
    pass 
