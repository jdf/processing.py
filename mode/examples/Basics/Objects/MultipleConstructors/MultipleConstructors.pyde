'''
 Multiple constructors
 
 A class can have multiple constructors that assign the fields in different ways. 
 Sometimes it's beneficial to specify every aspect of an object's data by assigning 
 parameters to the fields, but other times it might be appropriate to define only 
 one or a few.

 Example written in Python by  : Prabhjot Singh (NITH)
 original example in java mode : Example->Basic->Objects->MultipleConstructors
'''
def setup():
    size(640, 360)
    background(204)
    noLoop()

    global sp1, sp2, sp3, sp0

    # Run the constructor without parameters
    sp0 = Spot()

    # Run the constructor with one parameters
    sp1 = Spot(radius=58)

    # Run the constructor with two parameters
    sp2 = Spot(x=130, y=70)

    # Run the constructor with three parameters
    sp3 = Spot(width * 0.5, height * 0.5, 120)


def draw():
    global sp0, sp1, sp2, sp3
    sp1.display()
    sp2.display()
    sp3.display()
    sp0.display()

class Spot:
  # First version of the Spot constructor
  # the fields are assigned default values

  # Second version of the Spot constructor
  # the fields are assigned with parameters

    def __init__(self, x=None, y=None, radius=None):
        ''' Constructor for the Spot class'''
        if x is None:
            self.x = width * 0.25
        else:
            self.x = x

        if y is None:
            self.y = height * 0.5
        else:
            self.y = y

        if radius is None:
            self.radius = 40
        else:
            self.radius = radius

    def display(self):
        ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
