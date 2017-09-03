"""
Wave Gradient 
by Ira Greenberg.    

Generate a gradient along a sin() wave.
"""
amplitude = 30
fillGap = 2.5


def setup():
    size(640, 360)
    background(200)
    noLoop()


def draw():
    frequency = 0
    for i in range(-75, height + 75):
        # Reset angle to 0, so waves stack properly
        angle = 0
        # Increasing frequency causes more gaps
        frequency += .002
        for j in range(0, width + 75):
            py = i + sin(radians(angle)) * amplitude
            angle += frequency
            c = color(abs(py - i) * 255 / amplitude, 255 - abs(py - i)
                      * 255 / amplitude, j * (255.0 / (width + 50)))
            # Hack to fill gaps. Raise value of fillGap if you increase
            # frequency
            for filler in range(0, int(fillGap)):
                set(int(j - filler), int(py) - filler, c)
                set(int(j), int(py), c)
                set(int(j + filler), int(py) + filler, c)

