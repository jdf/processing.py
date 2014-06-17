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


class Particle(object):
    MOMENTUM = 0.5
    FLUID_FORCE = 0.6

    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.alpha = random(0.3, 1)
        self.mass = random(0.1, 1)

    def init(self, x, y):
        self.x = x
        self.y = y

    def update(self, invWidth, invHeight, fluidSolver):
        # Only update if particle is visible.
        if self.alpha == 0:
            return

        # Read fluid info and add to velocity.
        fluidIndex = (fluidSolver.getIndexForNormalizedPosition(
                      self.x * invWidth, self.y * invHeight))
        self.vx = (fluidSolver.u[fluidIndex] * width * self.mass *
                   Particle.FLUID_FORCE + self.vx * Particle.MOMENTUM)
        self.vy = (fluidSolver.v[fluidIndex] * height * self.mass *
                   Particle.FLUID_FORCE + self.vy * Particle.MOMENTUM)

        # Update position.
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges.
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        elif self.x > width:
            self.x = width
            self.vx *= -1
        if self.y < 0:
            self.y = 0
            self.vy *= -1
        elif self.y > height:
            self.y = height
            self.vy *= -1

        # Hackish way to make particles glitter when they slow down a lot.
        if self.vx**2 + self.vy**2 < 1:
            self.vx = random(-1, 1)
            self.vy = random(-1, 1)

        # Fade out a bit (and kill if self.alpha == 0).
        self.alpha *= 0.999
        if self.alpha < 0.01:
            self.alpha = 0

    def drawOldSchool(self, gl2):
        gl2.glColor3f(self.alpha, self.alpha, self.alpha)
        gl2.glVertex2f(self.x - self.vx, self.y - self.vy)
        gl2.glVertex2f(self.x, self.y)
