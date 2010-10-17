"""
  simple_noisefield.py - demonstrate Perlin noise
  Jonathan Feinberg
"""

def setup():
    size(100, 100)

def draw():
    t = .0005 * millis()
    for y in range(height):
        for x in range(width):
            blue = noise(t + .1*x, t + .05*y, .2*t)
            set(x, y, color(0, 0, 255 * blue))
