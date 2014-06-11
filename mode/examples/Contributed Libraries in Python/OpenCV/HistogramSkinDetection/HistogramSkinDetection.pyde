add_library('opencv_processing')

from org.opencv.core import Core, Mat, Point, Scalar, Size, CvType
from org.opencv.imgproc import Imgproc


def colorToScalar(c):
    # in BGR
    return Scalar(blue(c), green(c), red(c))

src = loadImage("test.jpg")
src.resize(src.width / 2, 0)
size(src.width * 2 + 256, src.height)
# third argument is: useColor
opencv = OpenCV(this, src, True)
skinHistogram = Mat.zeros(256, 256, CvType.CV_8UC1)
Core.ellipse(skinHistogram,
             Point(113.0, 155.6),
             Size(40.0, 25.2),
             43.0, 0.0, 360.0,
             Scalar(255, 255, 255), Core.FILLED)
histMask = createImage(256, 256, ARGB)
opencv.toPImage(skinHistogram, histMask)
hist = loadImage("cb-cr.png")
hist.blend(histMask, 0, 0, 256, 256, 0, 0, 256, 256, ADD)

dst = opencv.getOutput()
dst.loadPixels()

for i in xrange(len(dst.pixels)):
    input = Mat(Size(1, 1), CvType.CV_8UC3)
    input.setTo(colorToScalar(dst.pixels[i]))
    output = opencv.imitate(input)
    Imgproc.cvtColor(input, output, Imgproc.COLOR_BGR2YCrCb)
    inputComponents = output.get(0, 0)
    if skinHistogram.get(int(inputComponents[1]), int(inputComponents[2]))[0] > 0:
        dst.pixels[i] = color(255)
    else:
        dst.pixels[i] = color(0)

dst.updatePixels()

image(src, 0, 0)
image(dst, src.width, 0)
image(hist, src.width * 2, 0)

