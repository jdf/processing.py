class Ring(object):

    def start(self, xpos, ypos):
        self.x = xpos  # x-coordinate
        self.y = ypos  # y-coordinate
        self.diameter = 1  # Diameter of the ring
        self.on = False  # Turns the display on and off
        self.on = True

    def grow(self):
        if self.on:
            self.diameter += 0.5
            if self.diameter > width * 2:
                self.diameter = 0.0

    def display(self):
        if self.on:
            noFill()
            strokeWeight(4)
            stroke(155, 153)
            ellipse(self.x, self.y, self.diameter, self.diameter)

