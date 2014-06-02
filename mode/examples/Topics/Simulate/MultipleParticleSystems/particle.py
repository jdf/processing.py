# A simple Particle class
class Particle(object): 
    PVector location
    PVector velocity
    PVector acceleration
    lifespan
    Particle(PVector l) 
        acceleration = PVector(0,0.05)
        velocity = PVector(random(-1,1),random(-2,0))
        location = l.get()
        lifespan = 255.0
    
    def run(): 
        update()
        display()
    
    # Method to update location
    def update(): 
        velocity.add(acceleration)
        location.add(velocity)
        lifespan -= 2.0
    
    # Method to display
    def display(): 
        stroke(255,lifespan)
        fill(255,lifespan)
        ellipse(location.x,location.y,8,8)
    
    # Is the particle still useful?
    boolean isDead() 
        return (lifespan < 0.0)
    
