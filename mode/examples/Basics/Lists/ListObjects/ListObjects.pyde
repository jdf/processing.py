"""
 * List Objects.
 *
 * Demonstrates the syntax for creating a list of custom objects.
 """

from module import MovingBall

unit = 40

balls = []


def setup():
    size(640, 360)
    noStroke()
    for y in range(height / unit):
        for x in range(width / unit):
            balls.append(MovingBall(x * unit, y * unit, unit / 2, unit / 2, random(0.05, 0.8), unit))


def draw():
    background(0)
    for b in balls:
        b.update()
        b.draw()

