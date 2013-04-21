"""
  Metaball Demo Effect
  by luis2048. (Adapted to Python by Jonathan Feinberg)

  Organic-looking n-dimensional objects. The technique for rendering
  metaballs was invented by Jim Blinn in the early 1980s. Each metaball
  is defined as a function in n-dimensions.
"""

numBlobs = 3

# Position vector for each blob
blogPx = [0, 90, 90]
blogPy = [0, 120, 45]

# Movement vector for each blob
blogDx = [1, 1, 1]
blogDy = [1, 1, 1]

pg = None 
def setup():
    global pg
    size(640, 360, OPENGL)
    pg = createGraphics(160, 90, P2D)

    frame.setTitle("Processing.py")


def draw():
    vx, vy = [], []
    for i in range(numBlobs):
        blogPx[i] += blogDx[i]
        blogPy[i] += blogDy[i]

        # bounce across screen
        if blogPx[i] < 0: blogDx[i] = 1
        if blogPx[i] > pg.width: blogDx[i] = -1
        if blogPy[i] < 0: blogDy[i] = 1
        if blogPy[i] > pg.height: blogDy[i] = -1

        vx.append(tuple(sq(blogPx[i] - x) for x in xrange(pg.width)))
        vy.append(tuple(sq(blogPy[i] - y) for y in xrange(pg.height)))

  # Output into a buffered image for reuse
    pg.beginDraw()
    for y in range(pg.height):
        for x in range(pg.width):
            m = 1
            for i in range(numBlobs):
                # Increase this number to make your blobs bigger
                m += 60000 / (vy[i][y] + vx[i][x] + 1)
                pg.set(x, y, color(0, m + x, (x + m + y) / 2))
    pg.endDraw()

  # Display the results
    image(pg, 0, 0, width, height)
