"""
Clock. 

The current time can be read with the second(), minute(), 
and hour() functions. In this example, sin() and cos() values
are used to set the position of the hands.
"""


def setup():
    size(640, 360)
    stroke(255)

    global radius, secondsRadius, minutesRadius, hoursRadius, clockDiameter, cx, cy

    radius = min(width, height) / 2
    secondsRadius = radius * 0.72
    minutesRadius = radius * 0.60
    hoursRadius = radius * 0.50
    clockDiameter = radius * 1.8

    cx = width / 2
    cy = height / 2


def draw():
    background(0)

    # Draw the clock background
    fill(80)
    noStroke()
    ellipse(cx, cy, clockDiameter, clockDiameter)

    # Angles for sin() and cos() start at 3 o'clock;
    # subtract HALF_PI to make them start at the top
    s = map(second(), 0, 60, 0, TWO_PI) - HALF_PI
    m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - HALF_PI
    h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - HALF_PI

    # Draw the hands of the clock
    stroke(255)
    strokeWeight(1)
    line(cx, cy, cx + cos(s) * secondsRadius, cy + sin(s) * secondsRadius)
    strokeWeight(2)
    line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius)
    strokeWeight(4)
    line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius)

    # Draw the minute ticks
    strokeWeight(2)
    with beginShape(POINTS):
        for a in range(0, 360, 6):
            angle = radians(a)
            x = cx + cos(angle) * secondsRadius
            y = cy + sin(angle) * secondsRadius
            vertex(x, y)

