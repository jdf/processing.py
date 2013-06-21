"""
fern.py Based on a fern by Gareth Spor
Amended and adapted to python by Martin Prout
Features a grammar module, and bit shifting color
operations, uses a dict for 'pen'.
"""

from math import cos, radians, sin
from grammar import grammar

# some lsystems constants

DELTA = radians(5.4)

STARTCOLOR = color(0, 255, 0) # bright green

# bitwise color decrement for efficiency
DECREMENT = (6<<8)

RULES = {
'B' : '[6+#FD][7-#FD]', 
'C' : 'B',
'D' : 'C+@FD'
}

AXIOM = 'FD'
production = ""


def render(production):        # avoiding switch and globals
    """
    Render evaluates the production string and calls draw_line
    """
    global DELTA
    pen = { 'xpos' : 10, 
            'ypos' : 150, 
            'theta' : 0, 
            'distance' : 100, 
            'col' : STARTCOLOR
           }
    stack = []
    repeat = 1
    for val in production:
        if val == "F": 
            pen = __drawLine(pen)
        elif val == "+": 
            pen['theta'] += DELTA * repeat
            repeat = 1
        elif val == "-": 
            pen['theta'] -= DELTA * repeat
            repeat = 1
        elif val == "#": 
            pen['distance'] *= 0.33
            pen['col'] -= DECREMENT
        elif val == "@": 
            pen['distance'] *= 0.9 
            pen['col'] -= (DECREMENT << 1) # continue with bit shift * 2
        elif ((val == '6') or (val == '7')):
            repeat += int(val)  
        elif (val == '['):
            stack.append(dict(pen))
        elif (val == ']'):
            pen = stack.pop()
        elif (val == 'B' or val == 'C' or 'D'): # assert as valid grammar
            pass              
        else: 
            print("Unknown grammar %s" % val)


def __drawLine(pen):
    """
    Draw line utility uses processing 'line' function to draw lines
    takes pen dictionary input returns a pen with new position
    """
    new_xpos = pen['xpos'] + pen['distance'] * cos(pen['theta'])
    new_ypos = pen['ypos'] + pen['distance'] * sin(pen['theta'])
    stroke(pen['col'])
    strokeWeight(2)
    line(pen['xpos'], pen['ypos'], new_xpos, new_ypos)
    new_pen = dict(pen)
    new_pen['xpos'] = new_xpos
    new_pen['ypos'] = new_ypos
    return new_pen


def setup():
    """
    The processing setup statement
    """
    size(800, 600)
    global production
    production = grammar.repeat(17, AXIOM, RULES)
    

def draw():
    """
    Render the fern on a black background
    """
    background(0)
    smooth()
    render(production) 


def mouseReleased():
    saveFrame("pen.png")
