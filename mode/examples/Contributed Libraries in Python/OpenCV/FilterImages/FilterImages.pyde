add_library('opencv_processing')
img = loadImage("test.jpg")
size(img.width, img.height)
opencv = OpenCV(this, img)
gray = opencv.getSnapshot()

opencv.threshold(80)
thresh = opencv.getSnapshot()

opencv.loadImage(gray)
opencv.blur(12)
blur = opencv.getSnapshot()

opencv.loadImage(gray)
opencv.adaptiveThreshold(591, 1)
adaptive = opencv.getSnapshot()

with pushMatrix():
    scale(0.5)
    image(img, 0, 0)
    image(thresh, img.width, 0)
    image(blur, 0, img.height)
    image(adaptive, img.width, img.height)
fill(0)
text("source", img.width / 2 - 100, 20)
text("threshold", img.width - 100, 20)
text("blur", img.width / 2 - 100, img.height / 2 + 20)
text("adaptive threshold", img.width - 150, img.height / 2 + 20)

