'''
 Multiple Constructors

 A class can have multiple constructors that assign the fields in different ways.
 Sometimes it's beneficial to specify every aspect of an object's data by assigning
 parameters to the fields, but other times it might be appropriate to define only
 one or a few.

 Advanced example written in Python Mode by: Prabhjot Singh (NITH)
 Original example in Java Mode: Example->Basic->Objects->MultipleConstructors
'''
def setup():
    size(640, 360)
    smooth(4)
    noLoop()

    ellipseMode(CENTER)
    strokeWeight(2.5)
    stroke(0)
    fill('#FFFF00')

    global spots
    spots = Spot(), Spot(radius=58), Spot(x=120, y=70),\
        Spot(width / 2, height / 2, 120)


def draw():
    background(0300)
    for sp in spots:
        sp.display()


class Spot:

    def __init__(self, x=None, y=None, radius=40):
        if x is None:
            self.x = width / 4
        else:
            self.x = x
 
        if y is None:
            self.y = height / 2
        else:
            self.y = y
 
        self.radius = radius
        self.diam = radius * 2


    def display(self):
        ellipse(self.x, self.y, self.radius, self.diam)
