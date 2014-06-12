"""
 * Create Image. 
 * 
 * The createImage() function provides a fresh buffer of pixels to play with.
 * This example creates an image gradient.
 """


def setup():
    size(640, 360)
    global img
    img = createImage(230, 230, ARGB)
    pixCount = len(img.pixels)
    for i in range(pixCount):
        a = map(i, 0, pixCount, 255, 0)
        img.pixels[i] = color(0, 153, 204, a)


def draw():
    background(0)
    image(img, 90, 80)
    image(img, mouseX - img.width / 2, mouseY - img.height / 2)

