"""
Spring. 

Click, drag, and release the horizontal bar to start the spring. 
"""

# Spring drawing constants for top bar
springHeight = 32  # Height
left = 0      # Left position
right = 0     # Right position
max = 200     # Maximum Y value
min = 100     # Minimum Y value
over = False  # If mouse over
move = False  # If mouse down and over
# Spring simulation constants
M = 0.8   # Mass
K = 0.2   # Spring constant
D = 0.92  # Damping
R = 150   # Rest position
# Spring simulation variables
ps = R    # Position
v = 0.0   # Velocity
a = 0     # Acceleration
f = 0     # Force


def setup():
    size(640, 360)
    rectMode(CORNERS)
    noStroke()
    left = width / 2 - 100
    right = width / 2 + 100


def draw():
    background(102)
    updateSpring()
    drawSpring()


def drawSpring():
    # Draw base
    fill(0.2)
    baseWidth = 0.5 * ps + -8
    rect(width / 2 - baseWidth, ps + springHeight,
         width / 2 + baseWidth, height)
    # Set color and draw top bar.
    if over or move:
        fill(255)
    else:
        fill(204)
    rect(left, ps, right, ps + springHeight)


def updateSpring():
    # Update the spring position.
    if not move:
        f = -K * (ps - R)  # f=-ky
        a = f / M  # Set the acceleration. f=ma == a=f/m
        v = D * (v + a)  # Set the velocity.
        ps = ps + v  # Updated position
    if abs(v) < 0.1:
        v = 0.0
    # Test if mouse is over the top bar
    over = left < mouseX < right and ps < mouseY < ps + springHeight
    # Set and constrain the position of top bar.
    if move:
        ps = mouseY - springHeight / 2
        ps = constrain(ps, min, max)
        
        
def mousePressed():
    if over:
        move = True


def mouseReleased():
    move = False

