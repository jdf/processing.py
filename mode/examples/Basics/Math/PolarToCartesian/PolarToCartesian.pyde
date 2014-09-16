"""
PolarToCartesian
by Daniel Shiffman.    

Convert a polar coordinate (r,theta) to cartesian (x,y):    
x = rcos(theta)
y = rsin(theta)
"""

r = 0

# Angle and angular velocity, accleration
theta = 0
theta_vel = 0
theta_acc = 0.0001

def setup():
    size(640, 360)
    global r
    r = height * 0.45


def draw():
    global theta, theta_vel

    background(0)

    # Translate the origin point to the center of the screen
    translate(width / 2, height / 2)

    # Convert polar to cartesian
    x = r * cos(theta)
    y = r * sin(theta)

    # Draw the ellipse at the cartesian coordinate
    ellipseMode(CENTER)
    noStroke()
    fill(200)
    ellipse(x, y, 32, 32)

    # Apply acceleration and velocity to angle (r remains static in this
    # example)
    theta_vel += theta_acc
    theta += theta_vel
