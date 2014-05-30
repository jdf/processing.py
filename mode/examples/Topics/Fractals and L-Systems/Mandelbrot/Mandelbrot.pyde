"""
The Mandelbrot Set
by Daniel Shiffman.    

Simple rendering of the Mandelbrot set.
"""

# Establish a range of values on the complex plane
# A different range will allow us to "zoom" in or out on the fractal
xmin = -3
ymin = -1.25
w = 5
h = 2.5
size(640, 360)
noLoop()
background(255)
# Make sure we can write to the pixels[] array.
# Only need to do this once since we don't do any other drawing.
loadPixels()
# Maximum number of iterations for each point on the complex plane
maxiterations = 100
# x goes from xmin to xmax
xmax = xmin + w
# y goes from ymin to ymax
ymax = ymin + h
# Calculate amount we increment x,y for each pixel
dx = float(xmax - xmin) / (width)
dy = float(ymax - ymin) / (height)
# Start y
y = ymin
for j in range(height):
    # Start x
    x = xmin
    for i in range(width):
        # Now we test, as we iterate z = z^2 + cm does z tend towards infinity?
        a = x
        b = y
        n = 0
        while n < maxiterations:
            aa = a * a
            bb = b * b
            twoab = 2.0 * a * b
            a = aa - bb + x
            b = twoab + y
            # Infinty in our finite world is simple, let's just consider it 16
            if aa + bb > 16.0:
                break  # Bail
            n += 1
        # We color each pixel based on how long it takes to get to infinity
        # If we never got there, let's pick the color black
        if n == maxiterations:
            pixels[i + j * width] = color(0)
        else:
            # Gosh, we could make fancy colors here if we wanted
            pixels[i + j * width] = color(n * 16 % 255)
        x += dx
    y += dy
updatePixels()

