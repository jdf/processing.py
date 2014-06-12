"""
 * Alpha Mask. 
 * 
 * Loads a "mask" for an image to specify the transparency 
 * in different parts of the image. The two images are blended
 * together using the mask() method of PImage. 
 """


def setup():
    size(640, 360)
    global img, imgMask
    img = loadImage("moonwalk.jpg")
    imgMask = loadImage("mask.jpg")
    img.mask(imgMask)
    imageMode(CENTER)


def draw():
    background(0, 102, 153)
    image(img, width / 2, height / 2)
    image(img, mouseX, mouseY)

