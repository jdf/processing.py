
# A simple Particle class, renders the particle as an image
class Particle(object): 
    PVector loc
    PVector vel
    PVector acc
    lifespan
    PImage img
    Particle(PVector l,PImage img_) 
        acc = PVector(0,0)
        vx = randomGaussian()*0.3
        vy = randomGaussian()*0.3 - 1.0
        vel = PVector(vx,vy)
        loc = l.get()
        lifespan = 100.0
        img = img_
    
    def run(): 
        update()
        render()
    
    
    # Method to apply a force vector to the Particle object
    # Note we are ignoring "mass" here
    def applyForce(PVector f): 
        acc.add(f)
    
    # Method to update location
    def update(): 
        vel.add(acc)
        loc.add(vel)
        lifespan -= 2.5
        acc.mult(0)# clear Acceleration
    
    # Method to display
    def render(): 
        imageMode(CENTER)
        tint(255,lifespan)
        image(img,loc.x,loc.y)
        # Drawing a circle instead
        # fill(255,lifespan)
        # noStroke()
        # ellipse(loc.x,loc.y,img.width,img.height)
    
    # Is the particle still useful?
    boolean isDead() 
        if lifespan <= 0.0:
            return True
        else:
            return False
        
    
