"""
Integers Floats. 

Integers and floats are two different kinds of numerical data. 
An integer (more commonly called an int) is a number without 
a decimal point. A float is a floating-point number, which means 
it is a number that has a decimal place. Floats are used when you 
need to approximate real numbers.
"""

a = 0  # Create a variable "a" of the datatype "int"
b = 0.0  # Create a variable "b" of the datatype "float"


def setup():
    size(640, 360)
    stroke(255)
    frameRate(30)


def draw():
    global a, b
    
    background(0)

    a = a + 1
    b = b + 0.2
    line(a, 0, a, height / 2)
    line(b, height / 2, b, height)

    if a > width:
        a = 0

    if b > width:
        b = 0

