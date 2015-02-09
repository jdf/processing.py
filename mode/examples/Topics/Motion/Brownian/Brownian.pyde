"""
Brownian motion.

Recording random movement as a continuous line.
"""

NUMBER = 2000
RANGE = 6


def setup():
    size(640, 360)
    global ax, ay
    halfWidth = width / 2.0
    halfHeight = height / 2.0
    ax = [halfWidth for _ in range(NUMBER)]
    ay = [halfHeight for _ in range(NUMBER)]
    frameRate(30)


def draw():
    background(51)

    # Shift all elements 1 place to the left
    for i in range(1, NUMBER):
        ax[i - 1] = ax[i]
        ay[i - 1] = ay[i]

    # Put a value at the end of the array
    ax[NUMBER - 1] += random(-RANGE, RANGE)
    ay[NUMBER - 1] += random(-RANGE, RANGE)

    # Constrain all points to the screen
    ax[NUMBER - 1] = constrain(ax[NUMBER - 1], 0, width)
    ay[NUMBER - 1] = constrain(ay[NUMBER - 1], 0, height)

    # Draw a line connecting the points
    for i in range(1, NUMBER):
        val = float(i) / NUMBER * 204.0 + 51
        stroke(val)
        line(ax[i - 1], ay[i - 1], ax[i], ay[i])
