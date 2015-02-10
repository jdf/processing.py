"""
Non-orthogonal Reflection
by Ira Greenberg.

Based on the equation (R = 2N(N * L) - L) where R is the reflection vector,
N is the normal, and L is the incident vector.
"""

# Variables related to moving ball.
# Calculate initial random velocity.
velocity = PVector.random2D()
radius = 6
speed = 3.5


def setup():
    size(640, 360)
    global base1, base2, position
    fill(128)

    # Position of left hand side of floor.
    base1 = PVector(0, height - 150)

    # Position of right hand side of floor.
    base2 = PVector(width, height)
    createGround()

    # Start ellipse at middle top of screen.
    position = PVector(width / 2, 0)
    velocity.mult(speed)


def draw():
    # Draw background.
    fill(0, 12)
    noStroke()
    rect(0, 0, width, height)

    # Draw base.
    fill(200)
    quad(base1.x, base1.y, base2.x, base2.y, base2.x, height, 0, height)

    # Calculate base top normal.
    baseDelta = PVector.sub(base2, base1)
    baseDelta.normalize()
    normal = PVector(-baseDelta.y, baseDelta.x)

    # Draw ellipse.
    noStroke()
    fill(255)
    ellipse(position.x, position.y, radius * 2, radius * 2)

    # Move elipse.
    position.add(velocity)

    # Normalized incidence vector.
    incidence = PVector.mult(velocity, -1)
    incidence.normalize()

    # Detect and handle collision.
    for coord in coords:
        # Check distance between ellipse and base top coordinates.
        if PVector.dist(position, coord) < radius:
            # Calculate dot product of incident vector and base top normal.
            dot = incidence.dot(normal)

            # Calculate reflection vector.
            # Assign reflection vector to direction vector.
            velocity.set(2 * normal.x * dot - incidence.x,
                         2 * normal.y * dot - incidence.y, 0)
            velocity.mult(speed)

            # Draw base top normal at collision point.
            stroke(255, 128, 0)
            line(position.x, position.y,
                 position.x - normal.x * 100, position.y - normal.y * 100)

    # Detect boundary collision.
    # Right.
    if position.x > width - radius:
        position.x = width - radius
        velocity.x *= -1

    # Left.
    if position.x < radius:
        position.x = radius
        velocity.x *= -1

    # Top.
    if position.y < radius:
        position.y = radius
        velocity.y *= -1
        # Randomize base top.
        base1.y = random(height - 100, height)
        base2.y = random(height - 100, height)
        createGround()


# Calculate variables for the ground.
def createGround():
    global coords
    # Calculate length of base top.
    baseLength = PVector.dist(base1, base2)

    # A list of subpoints along the floor path.
    # Fill base top coordinate array.
    coords = [PVector(base1.x + ((base2.x - base1.x) / baseLength) * i,
                      base1.y + ((base2.y - base1.y) / baseLength) * i)
              for i in range(ceil(baseLength))]
