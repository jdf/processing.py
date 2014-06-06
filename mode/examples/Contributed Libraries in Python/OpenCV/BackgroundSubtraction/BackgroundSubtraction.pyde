add_library('video')
add_library('opencv_processing')


video = None
opencv = None


def setup():
    size(720, 480, P2D)
    video = Movie(this, "street.mov")
    opencv = OpenCV(this, 720, 480)

    opencv.startBackgroundSubtraction(5, 3, 0.5)

    video.loop()
    video.play()


def draw():
    image(video, 0, 0)
    opencv.loadImage(video)

    opencv.updateBackground()

    opencv.dilate()
    opencv.erode()
    noFill()
    stroke(255, 0, 0)
    strokeWeight(3)
    for contour in opencv.findContours():
        contour.draw()


def movieEvent(m):
    m.read()

