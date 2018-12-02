'''
 Multiple Constructors

 A class can have multiple constructors that assign the fields in different ways.
 Sometimes it's beneficial to specify every aspect of an object's data by assigning
 parameters to the fields, but other times it might be appropriate to define only
 one or a few.

In Python, as there is no method overloading, one can provide different ways of creating
instances by setting default values for parameters in the __init__ method.
'''

def setup():
    size(640, 360)
    background(204)
    noLoop()

    global spots
    spots = (Spot(),
             Spot(x=120, y=70),
             Spot(width / 2, height / 2, 120),
             Spot(radius=10),
             )

def draw():
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
        ellipse(self.x, self.y, self.diam, self.diam)
