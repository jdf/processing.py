# An ArrayList is used to manage the list of Particles
class ParticleSystem(object): 
    ArrayList<Particle> particles# An arraylist for all the particles
    PVector origin# An origin point for where particles are birthed
    ParticleSystem(num, PVector v) 
        particles = ArrayList<Particle>()# Initialize the arraylist
        origin = v.get()# Store the origin point
        for i in range(num): 
            particles.add(Particle(origin))# Add "num" amount of particles to the arraylist
        
    
    def run(): 
        # Cycle through the ArrayList backwards, because we are deleting while iterating
        for (i = particles.size()-1i >= 0i -= 1) 
            Particle p = particles.get(i)
            p.run()
            if p.isDead():
                particles.remove(i)
            
        
    
    def addParticle(): 
        Particle p
        # Add either a Particle or CrazyParticle to the system
        if int(random(0, 2)) == 0:
            p = Particle(origin)
        
        else:
            p = CrazyParticle(origin)
        
        particles.add(p)
    
    def addParticle(Particle p): 
        particles.add(p)
    
    # A method to test if the particle system still has particles
    boolean dead() 
        return particles.isEmpty()
    
