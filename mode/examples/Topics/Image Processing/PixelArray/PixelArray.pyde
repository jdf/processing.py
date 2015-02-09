"""
Pixel Array.

Click and drag the mouse up and down to control the signal and
press and hold any key to see the current pixel being read.
This program sequentially reads the color of every pixel of an image
and displays this color to fill the window.
"""
img = loadImage("sea.jpg")
direction = 1
signal = 0.0


def setup():
    size(640, 360)
    noFill()
    stroke(255)
    frameRate(30)


def draw():
    global signal, direction
    if signal > img.width * img.height - 1 or signal < 0:
        direction = direction * -1
    if mousePressed:
        mx = constrain(mouseX, 0, img.width - 1)
        my = constrain(mouseY, 0, img.height - 1)
        signal = my * img.width + mx
    else:
        signal += 0.33 * direction
    sx = int(signal) % img.width
    sy = int(signal) / img.width
    if keyPressed:
        set(0, 0, img)  # fast way to draw an image
        point(sx, sy)
        rect(sx - 5, sy - 5, 10, 10)
    else:
        c = img.get(sx, sy)
        background(c)
