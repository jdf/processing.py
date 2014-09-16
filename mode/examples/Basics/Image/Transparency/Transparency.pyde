"""
 * Transparency. 
 * 
 * Move the pointer left and right across the image to change
 * its position. This program overlays one image over another 
 * by modifying the alpha value of the image with the tint() function. 
 """

offset = 0
easing = 0.05


def setup():
    size(640, 360)
    global img
    img = loadImage("moonwalk.jpg")    # Load an image into the program


def draw():
    global offset
    image(img, 0, 0)    # Display at full opacity
    dx = (mouseX - img.width / 2) - offset
    offset += dx * easing
    tint(255, 127)    # Display at half opacity
    image(img, offset, 0)

