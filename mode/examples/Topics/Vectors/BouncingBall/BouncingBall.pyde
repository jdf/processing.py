"""
Bouncing Ball with Vectors 
by Daniel Shiffman.    

Demonstration of using vectors to control motion of body.
This example is not object-oriented.
See AccelerationWithVectors for an example of how to simulate motion using vectors in an object.
"""

location = None  # Location of shape
velocity = None  # Velocity of shape
gravity = None  # Gravity acts at the shape's acceleration.


def setup():
    size(640, 360)
    smooth()
    location = PVector(100, 100)
    velocity = PVector(1.5, 2.1)
    gravity = PVector(0, 0.2)


def draw():
    background(0)
    # Add velocity to the location.
    location.add(velocity)
    # Add gravity to velocity.
    velocity.add(gravity)
    # Bounce off edges.
    if (location.x > width) or (location.x < 0):
        velocity.x = velocity.x * -1
    if location.y > height:
        # We're reducing velocity ever so slightly
        # when it hits the bottom of the window.
        velocity.y = velocity.y * -0.95
        location.y = height
    # Display circle at location vector.
    stroke(255)
    strokeWeight(2)
    fill(127)
    ellipse(location.x, location.y, 48, 48)

