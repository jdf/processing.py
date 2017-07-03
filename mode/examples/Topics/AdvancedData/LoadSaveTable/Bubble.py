# A Bubble class


class Bubble(object):
    # Create  the Bubble

    def __init__(self, x, y, diameter, name):
        self.x = x
        self.y = y
        self.diameter = diameter
        self.name = name
        self.over = False

    # Checking if mouse is over the Bubble
    def rollover(self, px, py):
        d = dist(px, py, self.x, self.y)
        self.over = d < self.diameter / 2

    # Display the Bubble
    def display(self):
        stroke(0)
        strokeWeight(2)
        noFill()
        ellipse(self.x, self.y, self.diameter, self.diameter)
        if self.over:
            fill(0)
            textAlign(CENTER)
            text(self.name, self.x, self.y + self.diameter / 2 + 20)
