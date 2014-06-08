"""
Gravitational Attraction (3D) 
by Daniel Shiffman.    

Simulating gravitational attraction 
G ---> universal gravitational constant
m1 --> mass of object #1
m2 --> mass of object #2
d ---> distance between objects
F = (G*m1*m2)/(d*d)

For the basics of working with PVector, see
http://processing.org/learning/pvector/
as well as examples in Topics/Vectors/
"""

from planet import Planet
from sun import Sun

# A bunch of planets.
planets = [None] * 10
# One sun (note sun is not attracted to planets (violation of Newton's 3rd
# Law).
s = None
# An angle to rotate around the scene.
angle = 0


def setup():
    size(640, 360, P3D)
    smooth()
    # Some random planets.
    for i in range(len(planets)):
        planets[i] = Planet(random(0.1, 2), random(-width / 2, width / 2),
                            random(-height / 2, height / 2), random(-100, 100))
    # A single sun.
    s = Sun()


def draw():
    background(0)
    # Setup the scene.
    sphereDetail(8)
    lights()
    translate(width / 2, height / 2)
    rotateY(angle)
    # Display the Sun.
    s.display()
    # All the Planets
    for planet in planets:
        # Sun attracts Planets.
        force = s.attract(planet)
        planet.applyForce(force)
        # Update and draw Planets.
        planet.update()
        planet.display()
    # Rotate around the scene.
    angle += 0.003

