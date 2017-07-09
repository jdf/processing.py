"""
Based on the ArrayList of objects Java Mode example by Daniel Shiffman,
this demonstrates, to the same effect, how to use a simple Python list
to store a variable number of objects.
Items can be added and removed from the list.

Click the mouse to add bouncing balls.
"""
from Ball import Ball

balls = []
ballWidth = 48

def setup():
    size(640, 360)
    noStroke()

    # Start by adding one element
    balls.append(Ball(width / 2, 0, ballWidth))


def draw():
    background(255)

    # With a list, we could use `for i in range(len(list)):` but
    # we will let the Python `for obj in list:` loop iterate it.
    for ball in balls:
        ball.move()
        ball.display()
        if ball.finished():
            # Items can be deleted with remove()
            balls.remove(ball)


def mousePressed():
    # A new ball object is added to the list (by default to the end)
    balls.append(Ball(mouseX, mouseY, ballWidth))
