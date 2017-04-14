"""
hilbert.py by Martin Prout based on a Hilbert curve from "Algorithmic Beauty of Plants"
by Przemyslaw Prusinkiewicz & Aristid Lindenmayer
Uses a java peasycam library (Jonathan Feinberg), and a python grammar module.
Features processing affine transforms.
"""
from math import pi
import processing.opengl
import peasycam
import peasy.PeasyCam as PeasyCam

from grammar import grammar

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
BEN = pi/360   # just a bit of fun set BEN to zero for a regular Hilbert
THETA = pi/2 + BEN
PHI = pi/2 - BEN
ADJUST = [0, 0.5, -1.5, 3.5, -7.5, 15]
distance = 200
depth = 3

RULES = {
    'A': "B>F<CFC<F>D+F-D>F<1+CFC<F<B1^",
    'B': "A+F-CFB-F-D1->F>D-1>F-B1>FC-F-A1^",
    'C': "1>D-1>F-B>F<C-F-A1+FA+F-C<F<B-F-D1^",
    'D': "1>CFB>F<B1>FA+F-A1+FB>F<B1>FC1^"
}

AXIOM = 'A'

def render(production):       
    """
    Render evaluates the production string and calls box primitive
    uses processing affine transforms (translate/rotate)
    """
    global distance, depth
   
    translate(-distance * ADJUST[depth], -distance * ADJUST[depth], -distance * ADJUST[depth])
    lightSpecular(204, 204, 204) 
    specular(255, 255, 255) 
    shininess(1.0)    
    repeat = 3
    for val in production:
        if val == "F":
            translate(0,  0,  -distance / 2 )
            box(distance/ 6, distance/ 6, distance* 5/ 6)
            translate(0,  0,  -distance / 2 )
            box(distance / 6, distance / 6, distance / 6);
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
    
def setup():
    """
    The processing setup statement
    """
    size(500, 500, P3D)
    cam = PeasyCam(this, 200)
    cam.setMinimumDistance(100)
    cam.setMaximumDistance(500)
    smooth(16)
    global production, depth, distance
    production = grammar.repeat(depth, AXIOM, RULES)
    distance *= 1/(pow(2, depth) - 1)
    noStroke()
    fill(200, 0, 180) 
   

   
    
def draw():
    """
    Render a 3D Hilbert/Ben Tilbert, somewhat centered
    """
    lights()
    background(255)
    global production
    render(production)

