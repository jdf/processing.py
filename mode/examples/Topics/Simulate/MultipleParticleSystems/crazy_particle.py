from particle import Particle

# A subclass of Particle


class CrazyParticle(Particle):
    
    # Just adding one variable to a CrazyParticle.
    # It inherits all other fields from "Particle", and we don't have to
    # retype them!
    # The CrazyParticle constructor can call the parent class (super class)
    # constructor.
    def __init__(self, l):
        # "super" means do everything from the constructor in Particle.
        super(CrazyParticle, self).__init__(l)
        # One more line of code to deal with the variable, theta.
        self.theta = 0.0

    # Notice we don't have the method run() here, it is inherited from Particle.
    # This update() method overrides the parent class update().
    def update(self):
        super(CrazyParticle, self).update()
        # Increment rotation based on horizontal velocity.
        theta_vel = (self.velocity.x * self.velocity.mag()) / float(10.0)
        self.theta += theta_vel

    # This display() method overrides the parent class display() method.
    def display(self):
        # Render the ellipse just like in a regular particle
        super(CrazyParticle, self).display()
        # Then add a rotating line
        with pushMatrix():
            translate(self.location.x, self.location.y)
            rotate(self.theta)
            stroke(255, self.lifespan)
            line(0, 0, 25, 0)

