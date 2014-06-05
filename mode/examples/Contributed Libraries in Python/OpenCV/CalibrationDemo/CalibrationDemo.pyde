add_library('opencv_processing')

src = loadImage("checkerboard.jpg")
src.resize(500, 0)
size(src.width, src.height, P2D)
opencv = OpenCV(this, src)
opencv.gray()

cornerPoints = opencv.findChessboardCorners(9, 6)

image(opencv.getOutput(), 0, 0)
fill(255, 0, 0)
noStroke()
for p in cornerPoints:
    ellipse(p.x, p.y, 5, 5)

