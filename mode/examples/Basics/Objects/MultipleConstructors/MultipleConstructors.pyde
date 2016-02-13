'''
/**
 * Multiple constructors
 * 
 * A class can have multiple constructors that assign the fields in different ways. 
 * Sometimes it's beneficial to specify every aspect of an object's data by assigning 
 * parameters to the fields, but other times it might be appropriate to define only 
 * one or a few.
 */
 
 Example written in Python by  : Prabhjot Singh (NITH)
 original example in java mode : Example->Basic->Objects->MultipleConstructors
'''

def setup():
    size(640, 360)
    background(204)
    noLoop()
  # Run the constructor without parameters
    global sp1,sp2
    sp1 = Spot()
    
  # Run the constructor with three parameters
    sp2 = Spot(width*0.5, height*0.5, 120)

def draw():
    global sp1,sp2
    sp1.display()
    sp2.display()

class Spot :
  # First version of the Spot constructor
  # the fields are assigned default values
  
  # Second version of the Spot constructor
  # the fields are assigned with parameters
    def __init__(self,*arg):
        if len(arg)==0:
            self.radius = 40
            self.x = width*0.25
            self.y = height*0.5

        elif len(arg)==3:
            self.x = arg[0]
            self.y = arg[1]
            self.radius = arg[2]
    
    def display(self):
        ellipse(self.x, self.y, self.radius*2, self.radius*2)
  
