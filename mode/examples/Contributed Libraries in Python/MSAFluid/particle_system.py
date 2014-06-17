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

from javax.media.opengl import GL
from particle import Particle


class ParticleSystem(object):
    def __init__(self, maxParticles=5000):
        self.maxParticles = maxParticles
        self.curIndex = 0
        self.particles = [Particle() for _ in range(self.maxParticles)]

    def _fadeToColor(self, gl2, red, green, blue, speed):
        gl2.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        gl2.glColor4f(red, green, blue, speed)
        gl2.glBegin(gl2.GL_QUADS)
        gl2.glVertex2f(0, 0)
        gl2.glVertex2f(width, 0)
        gl2.glVertex2f(width, height)
        gl2.glVertex2f(0, height)
        gl2.glEnd()

    def updateAndDraw(self, invWidth, invHeight, drawFluid, fluidSolver):
        with beginPGL() as pgl:
            gl2 = pgl.gl.getGL2()
            gl2.glEnable(GL.GL_BLEND)  # Enable blending.
            if not drawFluid:
                self._fadeToColor(gl2, 0, 0, 0, 0.05)

            # Additive blending (ignore alpha).
            gl2.glBlendFunc(gl2.GL_ONE, GL.GL_ONE)

            # Make points round.
            gl2.glEnable(gl2.GL_LINE_SMOOTH)
            gl2.glLineWidth(1)

            # Start drawing points.
            gl2.glBegin(gl2.GL_LINES)
            for particle in self.particles:
                if particle.alpha > 0:
                    particle.update(invWidth, invHeight, fluidSolver)
                    # Use oldschool rendering.
                    particle.drawOldSchool(gl2)
            gl2.glEnd()
            gl2.glDisable(GL.GL_BLEND)

    def addParticle(self, x, y):
        self.particles[self.curIndex].init(x, y)
        self.curIndex += 1
        if self.curIndex >= self.maxParticles:
            self.curIndex = 0

    def addParticles(self, x, y, count):
        for _ in range(count):
            self.addParticle(x + random(-15, 15), y + random(-15, 15))
