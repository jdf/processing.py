"""
  Noise Wave
  by Daniel Shiffman.

  Using Perlin Noise to generate a wave-like pattern.
"""

xspacing = 8   # How far apart should each horizontal location be spaced

yoff = 0.0       # 2nd dimension of perlin noise
yvalues = None   # Using an array to store height values for the wave (not entirely necessary)

def setup():
    size(200, 200)
    frameRate(30)
    colorMode(RGB, 255, 255, 255, 100)
    smooth()
    global yvalues
    yvalues = [i for i in range((width + 16) / xspacing)]

def draw():
    background(0)
    calcWave()
    renderWave()

def calcWave():
    dx = 0.05
    dy = 0.01
    amplitude = 100.0

    # Increment y ('time')
    global yoff
    yoff += dy

    #xoff = 0.0  # Option #1
    xoff = yoff # Option #2

    for i in range(len(yvalues)):
        # Using 2D noise function
        #yvalues[i] = (2*noise(xoff,yoff)-1)*amplitude
        # Using 1D noise function
        yvalues[i] = (2 * noise(xoff) - 1) * amplitude
        xoff += dx

def renderWave():
    # A simple way to draw the wave with an ellipse at each location
    for x, v in enumerate(yvalues):
        noStroke()
        fill(255, 50)
        ellipseMode(CENTER)
        ellipse(x * xspacing, width / 2 + v, 16, 16)
