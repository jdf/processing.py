"""
Random Gaussian. 

This sketch draws ellipses with x and y locations tied to a gaussian distribution of random numbers.
"""


def setup():
    size(640, 360)
    background(0)


def draw():
    # Get a gaussian random number w/ mean of 0 and standard deviation of 1.0
    val = randomGaussian()
    sd = 60  # Define a standard deviation
    # Define a mean value (middle of the screen along the x-axis)
    mean = width / 2
    # Scale the gaussian random number by standard deviation and mean
    x = (val * sd) + mean
    noStroke()
    fill(255, 10)
    noStroke()
    # Draw an ellipse at our "normal" random location
    ellipse(x, height / 2, 32, 32)

