"""
Simple Particle System
by Daniel Shiffman.    

Particles are generated each cycle through draw(),
fall with gravity and fade out over time
A ParticleSystem object manages a variable size list 
of particles. 
"""

from particle_system import ParticleSystem

ps = None

def setup():
    global ps
    size(640, 360)
    ps = ParticleSystem(PVector(width / 2, 50))

def draw():
    background(0)
    ps.addParticle()
    ps.run()
