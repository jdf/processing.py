"""
 * Load and Display 
 * 
 * Images can be loaded and displayed to the screen at their actual size
 * or any other size. 
 """


def setup():
    size(640, 360)
    # The image file must be in the data folder of the current sketch
    # to load successfully
    global img
    img = loadImage("moonwalk.jpg")    # Load the image into the program
    noLoop()


def draw():
    # Displays the image at its actual size at point (0,0)
    image(img, 0, 0)
    # Displays the image at point (0, height/2) at half of its size
    image(img, 0, height / 2, img.width / 2, img.height / 2)

