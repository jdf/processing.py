# A class to(object): describe a group of Particles
# An ArrayList is used to manage the list of Particles 
class ParticleSystem(object): 
    ArrayList<Particle> particles# An arraylist for all the particles
    PVector origin# An origin point for where particles are birthed
    PImage img
    
    ParticleSystem(num, PVector v, PImage img_) 
        particles = ArrayList<Particle>()# Initialize the arraylist
        origin = v.get()# Store the origin poimg = img_
        for i in range(num): 
            particles.add(Particle(origin, img))# Add "num" amount of particles to the arraylist
        
    
    def run(): 
        for (i = particles.size()-1i >= 0i -= 1) 
            Particle p = particles.get(i)
            p.run()
            if p.isDead():
                particles.remove(i)
            
        
    
    
    # Method to add a force vector to all particles currently in the system
    def applyForce(PVector dir): 
        # Enhanced loop!!!
        for (Particle p: particles) 
            p.applyForce(dir)
        
    
    
    def addParticle(): 
        particles.add(Particle(origin,img))
    
