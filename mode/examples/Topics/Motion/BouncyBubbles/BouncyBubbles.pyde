"""
Bouncy Bubbles
based on code from Keith Peters.

Multiple-object collision.
The "bounding-box" rendering is imprecise because we've implemented springy
bodies which don't show their deformation.
"""
from ball import Ball

balls = []
NUM_BALLS = 12


def setup():
    size(640, 360, P3D)
    for i in range(NUM_BALLS):
        balls.append(Ball(random(width), random(height),
                          random(15, 45), i, balls))
    noStroke()
    ellipseMode(RADIUS)
    fill(255, 204)


def draw():
    background(0)
    for ball in balls:
        ball.collide()
        ball.move()
        ball.display()
