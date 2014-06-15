'''

 Demo of the MSAFluid library (www.memo.tv/msafluid_for_processing)
 Move mouse to add dye and forces to the fluid.
 LEFT mouse turns off fluid rendering, showing only particles and paths.
 RIGHT mouse turns off particles, showing only fluid rendering.
 Demonstrates feeding input into the fluid and reading data back (to update
 the particles).
 Port to processing.py by Ben Alkov, 2014.

'''
# * Copyright (c) 2008, 2009, Memo Akten, www.memo.tv
# * *** The Mega Super Awesome Visuals Company ***
# *  All rights reserved.
# *
# *  Redistribution and use in source and binary forms, with or without
# *  modification, are permitted provided that the following conditions are
# *  met:
# *
# *      * Redistributions of source code must retain the above copyright
# *        notice, this list of conditions and the following disclaimer.
# *      * Redistributions in binary form must reproduce the above copyright
# *        notice, this list of conditions and the following disclaimer in
# *        the documentation and / or other materials provided with the
# *        distribution.
# *      * Neither the name of MSA Visuals nor the names of its contributors
# *        may be used to endorse or promote products derived from this
# *        software without specific prior written permission.
# *
# *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# *  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# *  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# *  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# *  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# *  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA, OR
# *  PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# *  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# *  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# *  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

add_library('MSAFluid')
from particle_system import ParticleSystem

FLUID_WIDTH = 120
invWidth = 0
invHeight = 0
fluidSolver = None
particleSystem = None
drawFluid = True
drawSparks = True
imgFluid = None
aspectRatio = 0


def setup():
    size(784, 484, OPENGL)
    invWidth = 1.0 / width
    invHeight = 1.0 / height
    aspectRatio = (width * invHeight) ** 2

    # Create fluid and set options.
    fluidSolver = MSAFluidSolver2D((FLUID_WIDTH),
                                   (FLUID_WIDTH * height / width))
    fluidSolver.enableRGB(True).setFadeSpeed(0.003).setDeltaT(0.5).setVisc(0.0001)

    # Create image to hold fluid picture.
    imgFluid = createImage(fluidSolver.getWidth(),
                           fluidSolver.getHeight(), RGB)
    particleSystem = ParticleSystem()


def mouseMoved():
    mouseNormX = mouseX * invWidth
    mouseNormY = mouseY * invHeight
    mouseVelX = (mouseX - pmouseX) * invWidth
    mouseVelY = (mouseY - pmouseY) * invHeight
    addForce(mouseNormX, mouseNormY, mouseVelX, mouseVelY)


def draw():
    fluidSolver.update()
    if drawFluid:
        imgFluid.loadPixels()
        for i in range(fluidSolver.getNumCells()):
            imgFluid.pixels[i] = color(fluidSolver.r[i] * 2,
                                       fluidSolver.g[i] * 2,
                                       fluidSolver.b[i] * 2)
        imgFluid.updatePixels()
        image(imgFluid, 0, 0, width, height)
    if drawSparks:
        particleSystem.updateAndDraw(invWidth, invHeight,
                                     drawFluid, fluidSolver)


def mousePressed():
    if mouseButton == LEFT:
        drawFluid = not drawFluid
    elif mouseButton == RIGHT:
        drawSparks = not drawSparks


# Add force and dye to fluid, and create particles.
def addForce(x, y, dx, dy):

    # Balance the x and y components of speed with the screen aspect ratio.
    speed = dx**2 + (dy**2 * aspectRatio)
    if speed > 0:
        x = constrain(x, 0, 1)
        y = constrain(y, 0, 1)
        colorMult = 5
        velocityMult = 30.0
        index = fluidSolver.getIndexForNormalizedPosition(x, y)
        colorMode(HSB, 360, 1, 1)
        hue = ((x + y) * 180 + frameCount) % 360
        drawColor = color(hue, 1, 1)
        colorMode(RGB, 1)

        fluidSolver.rOld[index] += red(drawColor) * colorMult
        fluidSolver.gOld[index] += green(drawColor) * colorMult
        fluidSolver.bOld[index] += blue(drawColor) * colorMult
        particleSystem.addParticles(x * width, y * height, 10)
        fluidSolver.uOld[index] += dx * velocityMult
        fluidSolver.vOld[index] += dy * velocityMult
