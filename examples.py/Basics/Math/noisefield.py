"""
  noisefield.py - demonstrate Perlin noise
  Jonathan Feinberg
"""
srcSize = 50
destSize = 400
g = createGraphics(srcSize, srcSize, JAVA2D)

def setup():
    size(destSize, destSize, OPENGL)

def draw():
    t = .0005 * millis()
    g.beginDraw()
    for y in range(srcSize):
        for x in range(srcSize):
            blue = noise(t + .1*x, t + .05*y, .2*t)
            g.set(x, y, color(0, 0, 255 * blue))
    g.endDraw()
    image(g, 0, 0, destSize, destSize)
