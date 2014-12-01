"""
Noise Sphere
by David Pena.

Uniform random distribution on the surface of a sphere.
"""
from hair import Hair

quantity = 4000
rx = 0
ry = 0

def setup():
    size(640, 360, P3D)
    global halfWidth, halfHeight, radius, hairs
    halfWidth = width / 2
    halfHeight = height / 2
    radius = height / 3
    hairs = [Hair(radius) for _ in range(quantity)]
    noiseDetail(3)

def draw():
    background(0)
    translate(halfWidth, halfHeight)
    rxp = ((mouseX - (halfWidth)) * 0.005)
    ryp = ((mouseY - (halfHeight)) * 0.005)
    global rx, ry
    rx = (rx * 0.9) + (rxp * 0.1)
    ry = (ry * 0.9) + (ryp * 0.1)
    rotateY(rx)
    rotateX(ry)
    fill(0)
    noStroke()
    sphere(radius)

    for hair in hairs:
        hair.render()
