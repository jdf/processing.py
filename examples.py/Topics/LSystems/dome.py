"""
dome.py is a python script for use in processing.py
ASFAIK this is an original fractal.
By Martin Prout uses PeasyCam (Jonathan Feinberg)
Uses the processing Matrix to store state features
a python 'grammar'  module to generate the production
string
"""

from math import pi
from arcball.arcball import ArcBall

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
DELTA = pi/4
distance = 40
grammar = None

RULES = {
	'A' : 'F[&F+F+F+F+F+F+F+F+][A+]'
}

AXIOM = 'A+A+A+A+A+A+A+A'

production = None   # production needs exposure at module level


def render(production): 
	"""	
	Render evaluates the production string and calls box primitive
	uses processing affine transforms (white space in python is crap
	you need to watch out where final else gets put!!!)
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
        	elif val == "[":
        		pushMatrix()      
        	elif val == "]":
        		popMatrix()   
        	elif val == "A":       # required to assert valid grammar
        		pass
                else: 
        	     print("Unknown grammar %s" % val)    
        	
        	
def setup():
	"""
	Processing setup method
	"""
	size(600, 600, OPENGL)
	
	global arcball, grammar
	arcball = ArcBall(width/2.0, height/2.0, min(width - 20, height - 20) * 0.5)
	if grammar == None:
		from grammar import grammar
		global production    # Initialize production in setup, use in draw.
		production = grammar.repeat(3, AXIOM, RULES)
		
def draw():
	"""
	Processing draw method
	"""  
	background(0)
	lights()
	fill(255, 0, 0)
	translate(width/2, height/2)
	update()
	render(production)
	
def update():
	"""
	wrap arcball update and rotation as a local function
	"""
	theta, x, y, z = arcball.update()
	rotate(theta, x, y, z)    
	
def mousePressed():
	arcball.mousePressed(mouseX, mouseY)
	
def mouseDragged():
	arcball.mouseDragged(mouseX, mouseY) 
