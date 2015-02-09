"""
Non-orthogonal Collision with Multiple Ground Segments
by Ira Greenberg.

Based on Keith Peter's Solution in
Foundation Actionscript Animation: Making Things Move!
"""
from orb import Orb
from ground import Ground

# An orb object that will fall and bounce around.
orb = Orb(50, 50, 3)
segments = 40


def setup():
    size(640, 360)
    global grounds

    # Calculate ground peak heights.
    peakHeights = [float(random(height - 40, height - 30))
                   for _ in range(segments + 1)]

    # Float value required for segment width (segs) calculations so the ground
    #  spans the entire display window, regardless of segment number.
    # The ground is an array of "Ground" objects.
    grounds = [Ground(width / float(segments) * s,
                      peakHeights[s],
                      width / float(segments) * (s + 1),
                      peakHeights[s + 1])
               for s in range(segments)]


def draw():
    # Background.
    noStroke()
    fill(0, 15)
    rect(0, 0, width, height)

    # Move and display the orb.
    orb.move()
    orb.display()

    # Check walls.
    orb.checkWallCollision()

    # Check against all the ground segments.
    for ground in grounds:
        orb.checkGroundCollision(ground)

    # Draw ground.
    fill(127)
    beginShape()
    for ground in grounds:
        vertex(ground.x1, ground.y1)
        vertex(ground.x2, ground.y2)
    vertex(grounds[segments - 1].x2, height)
    vertex(grounds[0].x1, height)
    endShape(CLOSE)
