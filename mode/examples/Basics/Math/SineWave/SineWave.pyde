"""
Sine Wave
by Daniel Shiffman.

Render a simple sine wave.
"""

xspacing = 16       # How far apart should each horizontal location be spaced

theta = 0.0         # Start angle at 0
amplitude = 75.0    # Height of wave
period = 500.0      # How many pixels before the wave repeats

# Value for incrementing X, a function of period and xspacing
dx = (TWO_PI / period) * xspacing


def setup():
    size(640, 360)
    global w  # Width of entire wave
    w = width + 16
    # Using a list to store height values for the wave.
    global yvalues
    yvalues = [0.0] * (w / xspacing)


def draw():
    background(0)
    calcWave()
    renderWave()


def calcWave():
    global theta
    # Increment theta (try different values for 'angular velocity' here
    theta += 0.02
    # For every x value, calculate a y value with sine function
    x = theta
    for i in range(len(yvalues)):
        yvalues[i] = sin(x) * amplitude
        x += dx


def renderWave():
    noStroke()
    fill(255)
    # A simple way to draw the wave with an ellipse at each location
    for x in range(len(yvalues)):
        ellipse(x * xspacing, height / 2 + yvalues[x], 16, 16)
