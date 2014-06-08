add_library('opencv_processing')

src = loadImage("test.jpg")
size(src.width, src.height/2, P2D)
opencv = OpenCV(this, src)
opencv.gray()
opencv.threshold(70)
dst = opencv.getOutput()
contours = opencv.findContours()
print "found %d contours" % contours.size()

scale(0.5)
image(src, 0, 0)
image(dst, src.width, 0)
noFill()
strokeWeight(3)

for contour in contours: 
    stroke(0, 255, 0)
    contour.draw()
    
    stroke(255, 0, 0)
    with beginShape():
        for point in contour.getPolygonApproximation().getPoints(): 
            vertex(point.x, point.y)    

