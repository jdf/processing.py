"""
 * Request Image
 * by Ira Greenberg ( From Processing for Flash Developers). 
 * 
 * Shows how to use the requestImage() function with preloader animation. 
 * The requestImage() function loads images on a separate thread so that 
 * the sketch does not freeze while they load. It's very useful when you are
 * loading large images. 
 * 
 * These images are small for a quick download, but try it with your own huge 
 * images to get the full effect. 
 """
imgCount = 12

imgs = []

# Keeps track of loaded images (True or False)
loadStates = []


def setup():
    size(640, 360)
    smooth()
    # Load images asynchronously
    for i in range(imgCount):
        imgs.append(requestImage("PT_anim" + nf(i, 4) + ".gif"))
        loadStates.append(False)


def draw():
    background(0)

    # Start loading animation
    runLoaderAni()

    for i, img in enumerate(imgs):
        # Check if individual images are fully loaded
        if img.width not in (0, -1):
            # As images are loaded set True in boolean array
            loadStates[i] = True

    # When all images are loaded draw them to the screen
    if all(loadStates):
        drawImages()


def drawImages():
    y = (height - imgs[0].height) / 2
    imgWidth = width / len(imgs)
    for i, img in enumerate(imgs):
        image(img, imgWidth * i, y, img.width, img.height)

# Loading animation

loaderX, loaderY = 0, 0
theta = 0

def runLoaderAni():
    global loaderX, loaderY, theta
    
    # Only run when images are loading
    if not all(loadStates):
        ellipse(loaderX, loaderY, 10, 10)
        loaderX += 2
        loaderY = height / 2 + sin(theta) * (height / 8)
        theta += PI / 22
        # Reposition ellipse if it goes off the screen
        if loaderX > width + 5:
            loaderX = -5

