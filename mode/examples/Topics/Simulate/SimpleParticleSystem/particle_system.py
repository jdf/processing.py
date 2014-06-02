# A class to(object): describe a group of Particles
# An ArrayList is used to manage the list of Particles 
class ParticleSystem(object): 
    ArrayList<Particle> particles
    PVector origin
    ParticleSystem(PVector location) 
        origin = location.get()
        particles = ArrayList<Particle>()
    
    def addParticle(): 
        particles.add(Particle(origin))
    
    def run(): 
        for (i = particles.size()-1i >= 0i -= 1) 
            Particle p = particles.get(i)
            p.run()
            if p.isDead():
                particles.remove(i)
            
        
    
