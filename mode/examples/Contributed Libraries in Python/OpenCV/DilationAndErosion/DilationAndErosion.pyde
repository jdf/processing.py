add_library('opencv_processing')

src = loadImage("pen_sketch.jpg")
src.resize(src.width / 2, 0)
size(src.width * 2, src.height * 2, P2D)

opencv = OpenCV(this, src)

# Dilate and Erode both need a binary image
# So, we'll make it gray and threshold it.
opencv.gray()
opencv.threshold(100)

# We'll also invert so that erosion eats away the lines
# and dilation expands them (rather than vice-versa)
opencv.invert()

# save a snapshot to use in both operations
src = opencv.getSnapshot()

# erode and save snapshot for display
opencv.erode()
eroded = opencv.getSnapshot()

# reload un-eroded image and dilate it
opencv.loadImage(src)
opencv.dilate()

# save dilated version for display
dilated = opencv.getSnapshot()

# now erode on top of dilated version to close holes
opencv.erode()
both = opencv.getSnapshot()

image(src, 0, 0)
image(eroded, src.width, 0)
image(dilated, 0, src.height)
image(both, src.width, src.height)
fill(0, 255, 0)
text("original", 20, 20)
text("erode", src.width + 20, 20)
text("dilate", 20, src.height + 20)
text("dilate then erode\n(close holes)", src.width + 20, src.height + 20)

