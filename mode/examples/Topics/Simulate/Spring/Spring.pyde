"""
Spring. 

Click, drag, and release the horizontal bar to start the spring. 
"""
 
# Spring drawing constants for top bar
springHeight = 32# Height
left# Left position
right# Right position
max = 200# Maximum Y value
min = 100# Minimum Y value
boolean over = False# If mouse over
boolean move = False# If mouse down and over
# Spring simulation constants
M = 0.8# Mass
K = 0.2# Spring constant
D = 0.92# Damping
R = 150# Rest position
# Spring simulation variables
ps = R# Position
vs = 0.0# Velocity
as = 0# Acceleration
f = 0# Force
def setup(): 
    size(640, 360)
    rectMode(CORNERS)
    noStroke()
    left = width/2 - 100
    right = width/2 + 100
def draw(): 
    background(102)
    updateSpring()
    drawSpring()
def drawSpring(): 
    
    # Draw base
    fill(0.2)
    baseWidth = 0.5 * ps + -8
    rect(width/2 - baseWidth, ps + springHeight, width/2 + baseWidth, height)
    # Set color and draw top bar
    if over or move:
        fill(255)
    else:
        fill(204)
    
    rect(left, ps, right, ps + springHeight)
def updateSpring(): 
    # Update the spring position
    if !move:
        f = -K * (ps - R)# f=-ky
        as = f / M# Set the acceleration, f=ma == a=f/m
        vs = D * (vs + as)# Set the velocity
        ps = ps + vs# Updated position
    
    if abs(vs) < 0.1:
        vs = 0.0
    
    # Test if mouse is over the top bar
    if mouseX > left and mouseX < right and mouseY > ps and mouseY < ps + springHeight:
        over = True
    else:
        over = False
    
    
    # Set and constrain the position of top bar
    if move:
        ps = mouseY - springHeight/2
        ps = constrain(ps, min, max)
    
def mousePressed(): 
    if over:
        move = True
    
def mouseReleased(): 
    move = False
