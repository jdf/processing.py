class Ring(object): 
    
    x, y# X-coordinate, y-coordinate
    diameter# Diameter of the ring
    boolean on = False# Turns the display on and off
    
    def start(xpos, ypos): 
        x = xpos
        y = ypos
        on = True
        diameter = 1
    
    
    def grow(): 
        if on == True:
            diameter += 0.5
            if diameter > width*2:
                diameter = 0.0
            
        
    
    
    def display(): 
        if on == True:
            noFill()
            strokeWeight(4)
            stroke(155, 153)
            ellipse(x, y, diameter, diameter)
        
    
