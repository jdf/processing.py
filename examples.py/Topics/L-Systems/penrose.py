"""
penrose.py processing sketch by Martin Prout, but uses LSystem rules from a Fractint sketch 
by Herb Savage which in turn is based on Martin Gardner's "Penrose Tiles to Trapdoor Ciphers", 
Roger Penrose's rhombuses.
This sketch uses a grammar module as before, here the output is a pdf file. Wait until
the penrose appears before closing the applet (NB the text does not appear in the applet, 
but should be in the pdf file). You will probably need to edit the path to ttf fonts to 
match your system (apparently pdf export doesn't work well for non ttf fonts).
"""

import math
import grammar

# some globals
XPOS = 0
YPOS = 1
ANGLE = 2
DELTA = math.pi/5

RULES = {
    'F' : '',
    'W' : 'YBF2+ZRF4-XBF[-YBF4-WRF]2+',
    'X' : '+YBF2-ZRF[3-WRF2-XBF]+',
    'Y' : '-WRF2+XBF[3+YBF2+ZRF]-',
    'Z' : '2-YBF4+WRF[+ZRF4+XBF]2-XBF'
}

AXIOM = '[X]2+[X]2+[X]2+[X]2+[X]'


def render(production):       
    """
    Render evaluates the production string and calls draw_line
    """
    turtle = [0, 0, -DELTA]
    stack = []
    repeat = 1
    for val in production:
        if val == "F": 
            turtle = __drawLine(turtle, 20)
        elif val == "+": 
            turtle[ANGLE] += DELTA * repeat
            repeat = 1
        elif val == "-": 
            turtle[ANGLE] -= DELTA * repeat
            repeat = 1
        elif val == "[":      # an unfortunate aggregation of square brackets
            temp = []
            temp[:] = turtle
            stack.append(temp)
        elif val == "]": 
            turtle = stack.pop() 
        elif ((val == '2') or (val == '3') or (val == '4')):
            repeat = int(val)     
        else: 
            pass
        
        
def __drawLine(turtle, length):
    """
    private line draw uses processing 'line' function to draw a line
    to a heading from the turtle with distance = length returns a new
    turtle corresponding to end of the new line
    """
    turtlecopy = []
    turtlecopy[:] = turtle
    turtlecopy[XPOS] = turtle[XPOS] + length * math.cos(turtle[ANGLE])
    turtlecopy[YPOS] = turtle[YPOS] - length * math.sin(turtle[ANGLE])
    line(turtle[XPOS], turtle[YPOS], turtlecopy[XPOS], turtlecopy[YPOS])
    return turtlecopy     
    
def renderToPDF(production):
    """
    Create a pdf file with penrose drawing and rules, use a ttf font for pdf export.
    NB: The standard linux font path below, will probably need modification.
    """
    myFont = createFont("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
    beginRecord(PDF, "penrose.pdf")
    translate(width/2, height*0.4)
    render(production)
    textMode(SHAPE)
    fill(0)
    textFont(myFont, 18)
    text("Penrose Tiling", 300, 50)
    text(grammar.toRuleString(AXIOM, RULES), 100, 650)
    endRecord()
    
    
def setup():
    """
    The processing setup statement
    """
    size(700, 900, P2D)
    background(255)
    hint(ENABLE_NATIVE_FONTS)
    smooth()
    production = grammar.repeat(5, AXIOM, RULES)
    strokeWeight(2)
    #render(production) # now redundant could be used if pdf render not working?
    renderToPDF(production)
    
def draw():
    """
    An empty processing draw statement prevents premature 
    """
    pass 

