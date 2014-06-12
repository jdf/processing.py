# Custom Cube Class
class Cube(object):
    QuadBG = []
    # Colors are hardcoded
    QuadBG.append(color(255, 0, 0))
    QuadBG.append(color(255, 128, 0))
    QuadBG.append(color(255, 255, 0))
    QuadBG.append(color(0, 255, 0))
    QuadBG.append(color(0, 0, 255))
    QuadBG.append(color(127, 0, 255))

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        # Position, velocity vectors
        # Start in center
        self.position = PVector()
        # Random velocity vector
        self.velocity = PVector.random3D()
        # Also using PVector to hold rotation values for 3 axes
        # Random rotation
        self.rotation = PVector(random(40, 100), random(40, 100), random(40, 100))

        # cube composed of 6 quads
        # Vertices of the cube
        self.vertices = []
        # front
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, self.depth / 2))
        self.vertices.append(PVector(self.width / 2, -self.height / 2, self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, self.height / 2, self.depth / 2))
        # left
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, self.height / 2, self.depth / 2))
        # right
        self.vertices.append(PVector(self.width / 2, -self.height / 2, self.depth / 2))
        self.vertices.append(PVector(self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, self.depth / 2))
        # back
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, self.height / 2, -self.depth / 2))
        # top
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, -self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, -self.height / 2, self.depth / 2))
        # bottom
        self.vertices.append(PVector(-self.width / 2, self.height / 2, self.depth / 2))
        self.vertices.append(PVector(-self.width / 2, self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, -self.depth / 2))
        self.vertices.append(PVector(self.width / 2, self.height / 2, self.depth / 2))

    # Cube shape itself
    def drawCube(self):
        # Draw cube
        for i in range(6):
            fill(self.QuadBG[i])
            beginShape(QUADS)
            for j in range(4):
                vertex(self.vertices[j + 4 * i].x,
                       self.vertices[j + 4 * i].y,
                       self.vertices[j + 4 * i].z)
            endShape()

    # Update location
    def update(self, bounds):
        self.position.add(self.velocity)

        # Check wall collisions
        if self.position.x > bounds / 2 or self.position.x < -bounds / 2:
            self.velocity.x *= -1
        if self.position.y > bounds / 2 or self.position.y < -bounds / 2:
            self.velocity.y *= -1
        if self.position.z > bounds / 2 or self.position.z < -bounds / 2:
            self.velocity.z *= -1

    # Display method
    def display(self):
        with pushMatrix():
            translate(self.position.x, self.position.y, self.position.z)
            rotateX(frameCount * PI / self.rotation.x)
            rotateY(frameCount * PI / self.rotation.y)
            rotateZ(frameCount * PI / self.rotation.z)
            noStroke()
            self.drawCube()  # Farm out shape to another method
