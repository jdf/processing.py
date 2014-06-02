# A subclass of(object): Particle
class CrazyParticle(object): extends Particle 
    # Just adding one variable to a CrazyParticle
    # It inherits all other fields from "Particle", and we don't have to retype them!
    theta
    # The CrazyParticle constructor can call the parent class (super class) constructor
    CrazyParticle(PVector l) 
        # "super" means do everything from the constructor in Particle
        super(l)
        # One more line of code to deal with the variable, theta
        theta = 0.0
    
    # Notice we don't have the method run() hereit is inherited from Particle
    # This update() method overrides the parent class update(object):() method
    def update(): 
        super.update()
        # Increment rotation based on horizontal velocity
        theta_vel = (velocity.x * velocity.mag()) / 10.0f
        theta += theta_vel
    
    # This display() method overrides the parent class display(object):() method
    def display(): 
        # Render the ellipse just like in a regular particle
        super.display()
        # Then add a rotating line
        pushMatrix()
        translate(location.x,location.y)
        rotate(theta)
        stroke(255,lifespan)
        line(0,0,25,0)
        popMatrix()
    
