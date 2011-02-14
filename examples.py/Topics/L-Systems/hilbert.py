"""
hilbert.py by Martin Prout based on a Hilbert curve from "Algorithmic Beauty of Plants"
by Przemyslaw Prusinkiewicz & Aristid Lindenmayer
Uses a java peasycam library (Jonathan Feinberg), and a python grammar module.
Features processing affine transforms.
"""

import math
import processing.opengl
import peasy.PeasyCam as PeasyCam
import grammar

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
BEN = math.pi/360   # just a bit of fun set BEN to zero for a regular Hilbert
THETA = math.pi/2 + BEN
PHI = math.pi/2 - BEN

RULES = {
    'A': "B>F<CFC<F>D+F-D>F<1+CFC<F<B1^",
    'B': "A+F-CFB-F-D1->F>D-1>F-B1>FC-F-A1^",
    'C': "1>D-1>F-B>F<C-F-A1+FA+F-C<F<B-F-D1^",
    'D': "1>CFB>F<B1>FA+F-A1+FB>F<B1>FC1^"
}

AXIOM = 'A'

production = None   # need exposure at module level

def render(production):       
    """
    Render evaluates the production string and calls box primitive
    uses processing affine transforms (translate/rotate)
    """
    lightSpecular(204, 204, 204) 
    specular(255, 255, 255) 
    shininess(1.0) 
    distance = 20
    repeat = 1
    for val in production:
        if val == "F":
            translate(0, 0, -distance / 2)
            box(3, 3, distance - 1.6)
            translate(0, 0, -distance / 2)
            box(3, 3, 3);
        elif val == '+': 
            rotateX(THETA * repeat)
            repeat = 1
        elif val == '-': 
            rotateX(-THETA * repeat)
            repeat = 1
        elif val == '>': 
            rotateY(THETA * repeat)
            repeat = 1
        elif val == '<': 
            rotateY(-THETA * repeat)
        elif val == '^': 
            rotateZ(PHI * repeat)
            repeat = 1
        elif (val == '1') :
            repeat += 1           
        elif (val == 'A' or val == 'B' or val == 'C' or val == 'D'):            
            pass  # assert as valid grammar and do nothing
        else: 
            print("Unknown grammar %s" % val)
        
def configure_opengl():
    hint(ENABLE_OPENGL_4X_SMOOTH)     
    hint(DISABLE_OPENGL_ERROR_REPORT) 
    
def setup():
    """
    The processing setup statement
    """
    size(500, 500, OPENGL)
    configure_opengl()
    cam = PeasyCam(this, -70, 70, -70,250)
    cam.setMinimumDistance(height/10)
    cam.setMaximumDistance(height)    
    global production
    production = grammar.repeat(3, AXIOM, RULES)    
    noStroke()
    fill(200, 0, 180)   
   
    
def draw():
    """
    Render a 3D Hilbert/Ben Tilbert, somewhat centered
    """
    lights()
    background(255)
    render(production)

