"""
Non-orthogonal Reflection
by Ira Greenberg.

Based on the equation (R = 2N(N * L) - L) where R is the reflection vector, N
is the normal, and L is the incident vector.
"""

# Position of left hand side of floor.
base1 = None

# Position of right hand side of floor.
base2 = None

# A list of subpoints along the floor path.
coords = []

# Variables related to moving ball.
position = None
velocity = None
r = 6
speed = 3.5


def setup():
    size(640, 360)

    fill(128)
    base1 = PVector(0, height - 150)
    base2 = PVector(width, height)
    createGround()

    # Start ellipse at middle top of screen.
    position = PVector(width / 2, 0)

    # Calculate initial random velocity.
    velocity = PVector.random2D()
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
    ellipse(position.x, position.y, r * 2, r * 2)

    # Move elipse.
    position.add(velocity)

    # Normalized incidence vector.
    incidence = PVector.mult(velocity, -1)
    incidence.normalize()

    # Detect and handle collision.
    for i in range(len(coords)):
        # Check distance between ellipse and base top coordinates.
        if PVector.dist(position, coords[i]) < r:

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
    if position.x > width - r:
        position.x = width - r
        velocity.x *= -1

    # Left.
    if position.x < r:
        position.x = r
        velocity.x *= -1

    # Top.
    if position.y < r:
        position.y = r
        velocity.y *= -1
        # Randomize base top.
        base1.y = random(height - 100, height)
        base2.y = random(height - 100, height)
        createGround()


# Calculate variables for the ground.
def createGround():
    # Calculate length of base top.
    baseLength = PVector.dist(base1, base2)

    # Fill base top coordinate array.
    coords = [PVector() for _ in range(ceil(baseLength))]
    for i in range(len(coords)):
        coords[i].x = base1.x + ((base2.x - base1.x) / baseLength) * i
        coords[i].y = base1.y + ((base2.y - base1.y) / baseLength) * i
