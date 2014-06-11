"""
Multiple Particle Systems
by Daniel Shiffman.

Click the mouse to generate a burst of particles
at mouse location.

Each burst is one instance of a particle system
with Particles and CrazyParticles (a subclass of Particle).
Note use of Inheritance and Polymorphism here.
"""

from crazy_particle import CrazyParticle
from particle import Particle
from particle_system import ParticleSystem

systems = None

def setup():
    size(640, 360)
    systems = []


def draw():
    background(0)
    for ps in systems:
        ps.run()
        ps.addParticle()

    if not systems:
        fill(255)
        textAlign(CENTER)
        text("click mouse to add particle systems", width / 2, height / 2)


def mousePressed():
    systems.append(ParticleSystem(1, PVector(mouseX, mouseY)))

