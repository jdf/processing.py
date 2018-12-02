"""
Pie Chart    

Uses the arc() function to generate a pie chart from the data
stored in a tuple. 
"""
angles = (30, 10, 45, 35, 60, 38, 75, 67)


def setup():
    size(640, 360)
    noStroke()
    noLoop()    # Run once and stop


def draw():
    background(100)
    pieChart(300, angles)


def pieChart(diameter, data):
    lastAngle = 0
    for i, angle in enumerate(data):
        gray = map(i, 0, len(data), 0, 255)
        fill(gray)
        arc(width / 2, height / 2, diameter, diameter,
            lastAngle, lastAngle + radians(angle))
        lastAngle += radians(angle)

