add_library('video')
add_library('opencv_processing')

video = None
opencv = None
show_fps = False

def setup():
    global opencv
    global video
    size(640, 480)
    video = Capture(this, 640 / 2, 480 / 2)
    opencv = OpenCV(this, 640 / 2, 480 / 2)
    opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE)
    video.start()
    frameRate(12)


def draw():
    scale(2)
    opencv.loadImage(video)
    image(video, 0, 0)
    noFill()
    stroke(0, 255, 0)
    strokeWeight(3)
    faces = opencv.detect()
    for face in faces:
        rect(face.x, face.y, face.width, face.height)
    if show_fps:
        text("%d fps" % frameRate, 20, 20)


def captureEvent(c):
    c.read()

def mousePressed():
    show_fps = not show_fps
