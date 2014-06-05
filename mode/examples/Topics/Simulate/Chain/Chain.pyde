"""
Chain. 

One mass is attached to the mouse position and the other 
is attached the position of the other mass. The gravity
in the environment pulls down on both. 
"""

s1 = None
s2 = None
gravity = 9.0
mass = 2.0


def setup():
    size(640, 360)
    fill(255, 126)
    # Inputs: x, y, mass, gravity
    s1 = Spring2D(0.0, width / 2, mass, gravity)
    s2 = Spring2D(0.0, width / 2, mass, gravity)


def draw():
    background(0)
    s1.update(mouseX, mouseY)
    s1.display(mouseX, mouseY)
    s2.update(s1.x, s1.y)
    s2.display(s1.x, s1.y)


class Spring2D(object):

    def __init__(self, xpos, ypos, m, g):
        # The x- and y-axis velocities
        self.vx = 0
        self.vy = 0
        # The x- and y-coordinates
        self.x = xpos
        self.y = ypos
        self.radius = 30
        self.stiffness = 0.2
        self.damping = 0.7
        self.mass = m
        self.gravity = g

    def update(self, targetX, targetY):
        forceX = (targetX - self.x) * self.stiffness
        ax = forceX / self.mass
        self.vx = self.damping * (self.vx + ax)
        self.x += self.vx
        forceY = (targetY - self.y) * self.stiffness
        forceY += self.gravity
        ay = forceY / self.mass
        self.vy = self.damping * (self.vy + ay)
        self.y += self.vy

    def display(self, nx, ny):
        noStroke()
        ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
        stroke(255)
        line(self.x, self.y, nx, ny)

