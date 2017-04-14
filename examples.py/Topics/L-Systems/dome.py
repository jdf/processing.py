"""
dome.py is a python script for use in processing.py
ASFAIK this is an original fractal.
By Martin Prout uses PeasyCam (Jonathan Feinberg)
Uses the processing Matrix to store state features
a python 'grammar'  module to generate the production
string
"""

import math
import grammar
import processing.opengl
import peasy.PeasyCam as PeasyCam

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
DELTA = math.pi/4
distance = 40

RULES = {
	'A' : 'F[&F+F+F+F+F+F+F+F+][A+]'
}

AXIOM = 'A+A+A+A+A+A+A+A'

production = None   # production needs exposure at module level

def __configureOpengl():
	"""
	private setup opengl
	"""
	hint(ENABLE_OPENGL_4X_SMOOTH)     
	hint(DISABLE_OPENGL_ERROR_REPORT) 
	
	
def render(production): 
	"""	
	Render evaluates the production string and calls box primitive
	uses processing affine transforms
	"""
	lightSpecular(204, 204, 204) 
	specular(255, 255, 255) 
	shininess(1.0) 
	
        for val in production:
    	    if val == "F": 
    	    	    translate(0, distance/-2, 0)
    	    	    box(distance/9, distance, distance/9)
    	    	    translate(0, distance/-2, 0)
    	    elif val == "+": 
    	    	    rotateX(DELTA)
    	    elif val == "-": 
    	    	    rotateX(-DELTA)
    	    elif val == ">": 
    	    	    rotateY(-DELTA)
    	    	    repeat = 1
    	    elif val == "<": 
    	    	    rotateY(DELTA)
    	    elif val == "&": 
    	    	    rotateZ(-DELTA) 
    	    elif val == "^": 
    	    	    rotateZ(DELTA) 
    	    elif val == '[':
    	    	    pushMatrix()      
    	    elif val == ']':
    	    	    popMatrix()   
    	    elif val == 'A':       # required to assert valid grammar
    	    	    pass     	    
    	    else: 
    	    	    print("Unknown grammar %s" % val)    
    	    
    	    
def setup():
	"""
	Processing setup method
	"""
	size(600, 600, OPENGL)
	__configureOpengl()
	cam = PeasyCam(this, 100) 
	cam.setMinimumDistance(200)
	cam.setMaximumDistance(500)
	global production    # Initialize production in setup, use in draw.
	production = grammar.repeat(3, AXIOM, RULES)
	
def draw():
	"""
	Processing draw method
	"""  
	background(0)
	lights()
	fill(255, 0, 0)
	render(production)
	
def mouseReleased():
	"""
	Save frame function
	"""
	saveFrame("dome.png")
