"""
 Additive Wave
 by Daniel Shiffman.
 (Rewritten in Python by Jonathan Feinberg.)

 Create a more complex wave by adding two waves together.
 """

xspacing = 8    # How far apart should each horizontal location be spaced
maxwaves = 4    # total # of waves to add together
amplitude = []  # Height of wave
dx = []         # Value for incrementing X, to be calculated as a function of period and xspacing
yvalues = []    # Using an array to store height values for the wave (not entirely necessary)

def setup():
    size(200, 200)
    frameRate(30)
    colorMode(RGB, 255, 255, 255, 100)
    smooth()
    for i in range(maxwaves):
        amplitude.append(random(10, 30))
        period = random(100, 300) # How many pixels before the wave repeats
        dx.append((TWO_PI / period) * xspacing)
    for i in range((width + 16) / xspacing):
      yvalues.append(0.0)

def theta():
  # Try different multipliers for 'angular velocity' here
  return frameCount * 0.02

def draw():
    background(0)
    calcWave()
    renderWave()

def calcWave():
    # Set all height values to zero
    for i in range(len(yvalues)):
        yvalues[i] = 0

    # Accumulate wave height values
    for j in range(maxwaves):
        x = theta()
        for i in range(len(yvalues)):
            # Every other wave is cosine instead of sine
            if (j % 2 == 0):
              yvalues[i] += sin(x) * amplitude[j]
            else:
              yvalues[i] += cos(x) * amplitude[j]
            x += dx[j]


def renderWave():
    # A simple way to draw the wave with an ellipse at each location
    noStroke()
    fill(255, 50)
    ellipseMode(CENTER)
    for x in range(len(yvalues)):
        ellipse(x * xspacing, width / 2 + yvalues[x], 16, 16)
