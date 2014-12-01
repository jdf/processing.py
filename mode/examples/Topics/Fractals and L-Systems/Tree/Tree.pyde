"""
Recursive Tree
by Daniel Shiffman.    

Renders a simple tree-like structure via recursion. 
The branching angle is calculated as a function of 
the horizontal mouse location. Move the mouse left
and right to change the angle.
"""

def setup():
    size(640, 360)

def draw():
    background(0)
    frameRate(30)
    stroke(255)
    # Let's pick an angle 0 to 90 degrees based on the mouse position
    a = (mouseX / float(width)) * 90
    # Convert it to radians
    # Start the tree from the bottom of the screen
    translate(width / 2, height)
    # Draw a line 120 pixels
    line(0, 0, 0, -120)
    # Move to the end of that line
    translate(0, -120)
    # Start the recursive branching!
    branch(120, radians(a))

def branch(h, theta):
    # Each branch will be 2/3rds the size of the previous one
    h *= 0.66
    # All recursive functions must have an exit condition!!!!
    # Here, ours is when the length of the branch is 2 pixels or less
    if h > 2:
        # Save the current state of transformation (i.e. where are we now)
        pushMatrix()
        rotate(theta)  # Rotate by theta
        line(0, 0, 0, -h)  # Draw the branch
        translate(0, -h)  # Move to the end of the branch
        branch(h, theta)  # Ok, now call myself to draw two branches!!
        # Whenever we get back here, we "pop" in order to restore the previous
        # matrix state
        popMatrix()
        # Repeat the same thing, only branch off to the "left" this time!
        with pushMatrix():
            rotate(-theta)
            line(0, 0, 0, -h)
            translate(0, -h)
            branch(h, theta)

