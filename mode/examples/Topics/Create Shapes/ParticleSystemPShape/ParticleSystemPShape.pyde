"""
ParticleSystemPShape

A particle system optimized for drawing using PShape.
"""

from particle_system import ParticleSystem

def setup():
    size(640, 360, P2D)
    # A particle system with 10,000 particles.
    global ps
    ps = ParticleSystem(10000)
    # Writing to the depth buffer is disabled to avoid rendering
    # artifacts due to the fact that the particles are semi-transparent
    # but not z-sorted.
    hint(DISABLE_DEPTH_MASK)


def draw():
    background(0)
    # Update and display system.
    ps.update()
    ps.display()

    # Set the particle system's emitter location to the mouse.
    ps.setEmitter(mouseX, mouseY)

    # Display frame rate.
    fill(255)
    textSize(16)
    text("Frame rate: " + str(int(frameRate)), 10, 20)

