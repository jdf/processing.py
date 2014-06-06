add_library('opencv_processing')

img = None
opencv = None


def setup():
    img = loadImage("test.jpg")
    size(img.width, img.height, P2D)
    opencv = OpenCV(this, img)


def draw():
    opencv.loadImage(img)
    opencv.brightness(int(map(mouseX, 0, width, -255, 255)))
    image(opencv.getOutput(), 0, 0)

