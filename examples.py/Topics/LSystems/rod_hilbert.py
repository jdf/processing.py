"""
Copyright (c) 2011 Martin Prout
 
This demo is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
http://creativecommons.org/licenses/LGPL/2.1/

hilbert.py by Martin Prout based on a Hilbert curve from "Algorithmic Beauty
of Plants" by Przemyslaw Prusinkiewicz & Aristid Lindenmayer
and a python lsystem module to provide grammar module.
Features processing affine transforms.
"""

from math import pi,  sin,  cos
from grammar import grammar

# some lsystem constants
XPOS = 0
YPOS = 1
ANGLE = 2
BEN = pi/360   # just a bit of fun set BEN to zero for a regular Hilbert
THETA = pi/2   # + BEN
PHI = pi/2     # - BEN
distance = 320
depth = 2
# (pow(depth, 2) - 1)/2
adjustment = [0,  0.5,  1.5,  3.5,  7.5]

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
    Render evaluates the production string and calls sphere() and drawRod()
    uses processing affine transforms (translate/rotate)
    """
    lightSpecular(30, 30, 30)
    ambient(192, 192, 192)
    ambientLight(80, 80, 80)
    directionalLight(0, 0, 0, 80, 80, 80)
    specular(40, 40, 40) 
    shininess(0.3)  
    fill(192, 192, 192)
    sphereDetail(10)
    sphere(distance/7)  # first sphere end cap   
    repeat = 1
    for val in production:
        if val == "F":
            drawRod(distance)
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
            repeat = 2         
        elif (val == 'A' or val == 'B' or val == 'C' or val == 'D'):            
            pass  # assert as valid grammar and do nothing
        else: 
        	print("Unknown grammar %d"%val)


def drawRod(distance):
    """
    Draw a cylinder with length distance, and a sphere at the end
    """
    sides = 10
    radius = distance/7
    angle = 0
    angleIncrement = pi * 2 / sides    
    translate(0, 0, -distance / 2.0)            
    beginShape(QUAD_STRIP)
    for i in range(sides+1):
        normal(cos(angle), sin(angle), 0)  
        vertex(radius*cos(angle), radius*sin(angle), -distance/2)
        vertex(radius*cos(angle), radius*sin(angle), distance/2,)
        angle += angleIncrement
    endShape()
    translate(0, 0, -distance/2)
    sphere(radius)
        
def configure_opengl():
    smooth()
    

def evaluateRules():
    global production,  distance
    production = grammar.repeat(depth, AXIOM, RULES)
    if (depth > 0) :
        distance *= 1/(pow(2, depth) - 1)   
    
def setup():
    """
    The processing setup statement
    """
    size(500, 500, P3D)
    configure_opengl()
    evaluateRules()
    camera(width/2.0, height/2.0, 600, 0, 0, 0, 0, -1, 0)         
    noStroke()
    fill(200, 0, 180)
    translate(width/2 , height/2, 0)
   
    
def draw():
    """
    Render a 3D Hilbert/Rod Hilbert, somewhat centered
    """
    background(10, 10, 200)
    lights() 
    lightSpecular(204, 204, 204) 
    specular(255, 255, 255) 
    shininess(1.0) 
    pushMatrix()    
    rotateX(sin(radians(frameCount)))   
    rotateY(cos(radians(frameCount)))
    pushMatrix()
    translate( distance * adjustment[depth], -distance * adjustment[depth], distance * adjustment[depth])
    render(production)
    popMatrix()
    popMatrix()

def keyPressed():
    """
    User interaction for processing.py
    """
    global depth, distance
    if (key == '+') and (depth  < 4):
        depth += 1
        distance = 280
        evaluateRules()
    if (key == '-') and (depth > 1):
        depth -= 1
        distance = 280
        evaluateRules()    

