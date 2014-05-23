class Ring(object):

    x = 0.0  # x-coordinate
    y = 0.0  # y-coordinate
    diameter = 1  # Diameter of the ring
    on = False  # Turns the display on and off

    def start(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.on = True

    def grow(self):
        if self.on == True:
            self.diameter += 0.5
            if self.diameter > width * 2:
                self.diameter = 0.0

    def display(self):
        if self.on == True:
            noFill()
            strokeWeight(4)
            stroke(155, 153)
            ellipse(self.x, self.y, self.diameter, self.diameter)

