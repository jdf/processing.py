add_library('opencv_processing')

src = loadImage("robot_light.jpg")
src.resize(800, 0)
size(src.width, src.height)
opencv = OpenCV(this, src)
image(opencv.getOutput(), 0, 0)
loc = opencv.max()
stroke(255, 0, 0)
strokeWeight(4)
noFill()
ellipse(loc.x, loc.y, 10, 10)

