# A Bubble class


class Bubble(object):
    # Create  the Bubble

    def __init__(self, x_, y_, diameter_, name_):
        self.x = x_
        self.y = y_
        self.diameter = diameter_
        self.name = name_
        self.over = False

    # Checking if mouse is over the Bubble
    def rollover(self, px, py):
        d = dist(px, py, self.x, self.y)
        if d < self.diameter / 2:
            self.over = True
        else:
            self.over = False

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
