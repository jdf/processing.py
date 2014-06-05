add_library('opencv_processing')

opencv = OpenCV(this, "test.jpg")

size(opencv.width, opencv.height)

opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE)
faces = opencv.detect()

image(opencv.getInput(), 0, 0)
noFill()
stroke(0, 255, 0)
strokeWeight(3)
for i in range(len(faces)):
    rect(faces[i].x, faces[i].y, faces[i].width, faces[i].height)

