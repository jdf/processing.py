"""
Wave Gradient
by Ira Greenberg.

Generate a gradient along a sin() wave.
"""
amplitude = 30
fillGap = 2


def setup():
    size(640, 360)
    background(200)
    noLoop()


def draw():
    frequency = 0
    j_del = 255.0 / (width + 50)
    for i in range(-75, height + 75):
        # Reset angle to 0, so waves stack properly
        angle = 0
        # Increasing frequency causes more gaps
        frequency += .002
        for j in range(0, width + 75):
            sy = sin(radians(angle))
            py = i + int(sy * amplitude)
            angle += frequency
            c = color(abs(sy) * 255, 255 - abs(sy) * 255, j * j_del)
            set(j, py, c)
            # Hack to fill gaps. Raise value of fillGap if you increase
            # frequency
            for filler in range(0, fillGap):
                set(j - filler, py - filler, c)
                set(j + filler, py + filler, c)
