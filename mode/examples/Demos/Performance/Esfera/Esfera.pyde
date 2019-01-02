"""
Esfera by David Pena.

ES - Distribucion aleatoria uniforme sobre la superficie de una esfera.
EN - Uniform random distribution on the surface of a sphere.
"""

CUANTOS = 16000  # how many
LISTA = []  # list
RADIO = 200  # radius
rx = 0
ry = 0


def setup():
    global RADIO, LISTA
    size(1024, 768, P3D)
    RADIO = height / 3.5

    for _ in range(CUANTOS):
        LISTA.append(Pelo())

    noiseDetail(3)


def draw():
    global rx, ry

    background(0)

    rxp = (mouseX - (width / 2)) * 0.005
    ryp = (mouseY - (height / 2)) * 0.005
    rx = rx * 0.9 + rxp * 0.1
    ry = ry * 0.9 + ryp * 0.1

    translate(width / 2, height / 2)
    rotateY(rx)
    rotateX(ry)
    fill(0)
    noStroke()
    sphere(RADIO)

    for pelo in LISTA:
        pelo.dibujar()


class Pelo():

    """A hair"""

    def __init__(self):
        self.z = random(-RADIO, RADIO)
        self.phi = random(TWO_PI)
        self.largo = random(1.15, 1.2)
        self.theta = asin(self.z / RADIO)

    def dibujar(self):
        """Draw"""
        off = (noise(millis() * 0.0005, sin(self.phi)) - 0.5) * 0.3
        offb = (noise(millis() * 0.0007, sin(self.z) * 0.01) - 0.5) * 0.3

        thetaff = self.theta + off
        phff = self.phi + offb
        x = RADIO * cos(self.theta) * cos(self.phi)
        y = RADIO * cos(self.theta) * sin(self.phi)
        z = RADIO * sin(self.theta)

        xo = RADIO * cos(thetaff) * cos(phff)
        yo = RADIO * cos(thetaff) * sin(phff)
        zo = RADIO * sin(thetaff)

        xb = xo * self.largo
        yb = yo * self.largo
        zb = zo * self.largo

        strokeWeight(1)
        beginShape(LINES)
        stroke(0)
        vertex(x, y, z)
        stroke(200, 150)
        vertex(xb, yb, zb)
        endShape()
