# Particles, by Daniel Shiffman.
from particle_system import ParticleSystem


def setup():
    size(1024, 768, P2D)
    sprite = loadImage("sprite.png")
    global ps
    ps = ParticleSystem(10000, sprite)
    # Writing to the depth buffer is disabled to avoid rendering
    # artifacts due to the fact that the particles are semi-transparent
    # but not z-sorted.
    hint(DISABLE_DEPTH_MASK)


def draw():
    background(0)
    ps.update()
    ps.display()

    ps.setEmitter(mouseX, mouseY)

    fill(255)
    textSize(16)
    text("Frame rate: " + str(int(frameRate)), 10, 20)

