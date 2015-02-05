"""
Sequential
by James Paterson.

Displaying a sequence of images creates the illusion of motion.
Twelve images are loaded and each is displayed individually in a loop.
"""

numFrames = 12  # The number of frames in the animation
images = [PImage] * numFrames

def setup():
    size(640, 360)
    frameRate(24)

    images[0] = loadImage("PT_anim0000.gif")
    images[1] = loadImage("PT_anim0001.gif")
    images[2] = loadImage("PT_anim0002.gif")
    images[3] = loadImage("PT_anim0003.gif")
    images[4] = loadImage("PT_anim0004.gif")
    images[5] = loadImage("PT_anim0005.gif")
    images[6] = loadImage("PT_anim0006.gif")
    images[7] = loadImage("PT_anim0007.gif")
    images[8] = loadImage("PT_anim0008.gif")
    images[9] = loadImage("PT_anim0009.gif")
    images[10] = loadImage("PT_anim0010.gif")
    images[11] = loadImage("PT_anim0011.gif")

    # If you don't want to load each image separately
    # and you know how many frames you have, you
    # can create the filenames as the program runs.
    # The nf() command does number formatting, which will
    # ensure that the number is (in this case) 4 digits.
    # Using a list comprehension:
    # images = [loadImage('PT_anim' + nf(i, 4) + '.gif')
    #           for i in range(numFrames)]
    #

def draw():
    background(0)
    # Use % to cycle through frames
    currentFrame = (frameCount + 1) % numFrames
    offset = 0
    for x in range(-100, width, images[0].width):
        image(images[(currentFrame + offset) % numFrames], x, -20)
        offset += 2
        image(images[(currentFrame + offset) % numFrames], x, height / 2)
        offset += 2

