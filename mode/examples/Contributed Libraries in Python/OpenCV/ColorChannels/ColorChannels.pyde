add_library('opencv_processing')

src = loadImage("green_object.png")
src.resize(800, 0)
opencv = OpenCV(this, src)
size(int(opencv.width*1.5), int(opencv.height * 1.5), P2D)

imgH = src.height/2
imgW = src.width/2

r = opencv.getSnapshot(opencv.getR())
g = opencv.getSnapshot(opencv.getG())
b = opencv.getSnapshot(opencv.getB())

opencv.useColor(HSB)

h = opencv.getSnapshot(opencv.getH())
s = opencv.getSnapshot(opencv.getS())
v = opencv.getSnapshot(opencv.getV())

background(0)
noTint()
image(src, imgW,0, imgW, imgH)

tint(255,0,0)
image(r, 0, imgH, imgW, imgH)

tint(0,255,0)
image(g, imgW, imgH, imgW, imgH)

tint(0,0,255)
image(b, 2*imgW, imgH, imgW, imgH)

noTint()
image(h, 0, 2*imgH, imgW, imgH)
image(s, imgW, 2*imgH, imgW, imgH)
image(v, 2*imgW, 2*imgH, imgW, imgH)
