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

    def __init__(self, x=0, y=0, radius=40):
        self.x = x or width / 4
        self.y = y or height / 2
        self.radius = radius
        self.diam = radius * 2

    def display(self):
        ellipse(self.x, self.y, self.diam, self.diam)

