"""
There are a number of functions that must eventually be followed by a
partner function that "pops" or "closes" some context created by the
first function. For example, every pushMatrix() must eventually be
followed by a popMatrix().

Python mode provides all of the same functions, but also takes advantage
of the Python language's "with" statement to provide automatic context
management.

So, for example, instead of

    pushMatrix()
    translate(10, 10)
    rotate(PI/3)
    rect(0, 0, 10, 10)
    popMatrix()
    rect(0, 0, 10, 10)

you can write

    with pushMatrix():
        translate(10, 10)
        rotate(PI/3)
        rect(0, 0, 10, 10)
    rect(0, 0, 10, 10)

This has two advantages: indentation clearly reveals which lines of
code are executed while the matrix is pushed, and you can't forget
to popMatrix(). Also, there's less code, which means fewer bugs!

You can also use "with" statements in these contexts:

Use this:                        Instead of this:

with pushStyle():                pushStyle()
    doSomething()                doSomething()
                                 popStyle()
  
  
with beginContour():             beginContour()
    doSomething()                doSomething()
                                 endContour()


with beginCamera():              beginCamera()
    doSomething()                doSomething()
                                 endCamera()

with beginPGL():                 beginPGL()
    doSomething()                doSomething()
                                 endPGL()

with beginShape():               beginShape()
    vertex(x, y)                 vertex(x, y)
    vertex(j, k)                 vertex(j,k)
                                 endShape()
    
    
with beginShape(TRIANGLES):      beginShape(TRIANGLES)
    vertex(x, y)                 vertex(x, y)
    vertex(j, k)                 vertex(x, y)
                                 endShape()

with beginClosedShape():         beginShape()
    vertex(x, y)                 vertex(x, y)
    vertex(j, k)                 vertex(j, k)
                                 endShape(CLOSED)
"""
size(250, 180)
background(0)

fill('#FF0000')
# This should be red and at absolute 10, 10
ellipse(10, 10, 10, 10)
fill('#0000FF')
with pushStyle():
    fill('#00FF00')
    with pushMatrix():
        translate(10, 10)
        # This should be green and at absolute 20, 20:
        ellipse(10, 10, 10, 10)
# This should be blue and at absolute 30, 30:
ellipse(30, 30, 10, 10)

fill(255)
stroke(180)

with pushMatrix():
    translate(50, 0)
    with beginClosedShape():
        vertex(0, 20)
        vertex(20, 20)
        vertex(20, 40)
        vertex(40, 40)
        vertex(40, 60)
        vertex(0, 60)

    translate(50, 0)
    with beginShape(QUAD_STRIP):
        vertex(0, 20)
        vertex(0, 75)
        vertex(20, 20)
        vertex(20, 75)
        vertex(35, 20)
        vertex(35, 75)
        vertex(55, 20)
        vertex(55, 75)

    translate(70, 0)
    with beginShape(LINES):
        vertex(0, 20)
        vertex(55, 20)
        vertex(55, 75)
        vertex(0, 75)

with pushMatrix():
    translate(10, 80)
    with beginShape(TRIANGLE_STRIP):
        vertex(0, 75)
        vertex(10, 20)
        vertex(20, 75)
        vertex(30, 20)
        vertex(40, 75)
        vertex(50, 20)
        vertex(60, 75)

    translate(70, 0)
    with beginShape(TRIANGLE_FAN):
        vertex(35.5, 50)
        vertex(35.5, 15)
        vertex(70, 50)
        vertex(35.5, 85)
        vertex(0, 50)
        vertex(35.5, 15)

    translate(90, 0)
    with beginShape(QUADS):
        vertex(0, 20)
        vertex(0, 75)
        vertex(20, 75)
        vertex(20, 20)
        vertex(35, 20)
        vertex(35, 75)
        vertex(55, 75)
        vertex(55, 20)

