"""
Springs. 

Move the mouse over one of the circles and click to re-position. 
When you release the mouse, it will snap back into position. 
Each circle has a slightly different behavior.    
"""

num = 3
springs = [None] * num


def setup():
    size(640, 360)
    noStroke()
    springs[0] = Spring(240, 260, 40, 0.98, 8.0, 0.1, springs, 0)
    springs[1] = Spring(320, 210, 120, 0.95, 9.0, 0.1, springs, 1)
    springs[2] = Spring(180, 170, 200, 0.90, 9.9, 0.1, springs, 2)


def draw():
    background(51)
    for i in range(num):
        springs[i].update()
        springs[i].display()


def mousePressed():
    for i in range(num):
        springs[i].pressed()


def mouseReleased():
    for i in range(num):
        springs[i].released()


class Spring(object):

    # Constructor
    def __init__(self, x, y, s, d, m, k_in, others, id):
        self.over = False
        self.move = False
        self.velx = 0.0  # X Velocity
        self.vely = 0.0  # Y Velocity
        self.accel = 0  # Acceleration
        self.force = 0  # Force
        # Screen values
        self.xpos = x
        self.tempxpos = x
        self.ypos = y
        self.tempypos = y
        self.rest_posx = x  # Rest position X
        self.rest_posy = y  # Rest position Y
        self.size = s
        self.damp = d  # Damping
        self.mass = m  # Mass
        self.k = k_in  # Spring constant
        self.friends = others
        self.me = id

    def update(self):
        if self.move:
            self.rest_posy = mouseY
            self.rest_posx = mouseX
        self.force = -self.k * (self.tempypos - self.rest_posy)  # f=-ky
        # Set the acceleration, f=ma == a=f/m
        self.accel = self.force / self.mass
        self.vely = self.damp * (self.vely + self.accel)  # Set the velocity
        self.tempypos = self.tempypos + self.vely  # Updated position
        self.force = -self.k * (self.tempxpos - self.rest_posx)  # f=-ky
        # Set the acceleration, f=ma == a=f/m
        self.accel = self.force / self.mass
        self.velx = self.damp * (self.velx + self.accel)  # Set the velocity
        self.tempxpos = self.tempxpos + self.velx  # Updated position
        if (self.overEvent() or self.move) and not self.otherOver():
            self.over = True
        else:
            self.over = False

    # Test to see if mouse is over this spring
    def overEvent(self):
        disX = self.tempxpos - mouseX
        disY = self.tempypos - mouseY
        if sqrt(sq(disX) + sq(disY)) < self.size / 2:
            return True
        else:
            return False

    # Make sure no other springs are active
    def otherOver(self):
        for i in range(num):
            if i != self.me:
                if self.friends[i].over == True:
                    return True
        return False

    def display(self):
        if self.over:
            fill(153)
        else:
            fill(255)
        ellipse(self.tempxpos, self.tempypos, self.size, self.size)

    def pressed(self):
        if self.over:
            self.move = True
        else:
            self.move = False

    def released(self):
        self.move = False
        self.rest_posx = self.xpos
        self.rest_posy = self.ypos

