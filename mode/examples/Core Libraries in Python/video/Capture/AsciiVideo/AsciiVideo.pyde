"""
ASCII Video
by Ben Fry. 


Text characters have been used to represent images since the earliest computers.
This sketch is a simple homage that re-interprets live video as ASCII text.
See the keyPressed function for more options, like changing the font size.
"""
add_library('video')

cheatScreen = False

# All ASCII characters, sorted according to their visual density
letterOrder =
    " .`-_':,^=+/\"|)\\<>)iv%xclrs*I?!][1taeo7zjLu" +
    "nT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q"

fontSize = 1.5


def setup():
    size(640, 480)
    # This the default video input, see the GettingStartedCapture
    # example if it creates an error
    video = Capture(this, 160, 120)

    # Start capturing the images from the camera
    video.start()

    count = video.width * video.height

    font = loadFont("UniversLTStd-Light-48.vlw")

    # for the 256 levels of brightness, distribute the letters across
    # the an array of 256 elements to use for the lookup
    letters = []
    for i in range(256):
        index = int(map(i, 0, 256, 0, len(letterOrder)))
        letters.append(letterOrder[index])

    # current brightness for each pobright = float[count]
    # set each brightness at the midpoint to start
    bright = [128] * count


def captureEvent(Capture c):
    c.read()


def draw():
    background(0)
    pushMatrix()
    hgap = width / float(video.width)
    vgap = height / float(video.height)
    scale(max(hgap, vgap) * fontSize)
    textFont(font, fontSize)
    index = 0
    video.loadPixels()
    for y in range(1, video.height):
        # Move down for next line
        translate(0,    1.0 / fontSize)
        pushMatrix()
        for x in range(video.width):
            pixelColor = video.pixels[index]
            # Faster method of calculating r, g, b than red(), green(), blue()
            r = (pixelColor >> 16) & 0xff
            g = (pixelColor >> 8) & 0xff
            b = pixelColor & 0xff
            # Another option would be to properly calculate brightness as luminance:
            # luminance = 0.3*red + 0.59*green + 0.11*blue
            # Or you could instead red + green + blue, and make the the values[] array
            # 256*3 elements long instead of just 256.
            pixelBright = max(r, g, b)
            # The 0.1 value is used to damp the changes so that letters flicker
            # less
            diff = pixelBright - bright[index]
            bright[index] += diff * 0.1
            fill(pixelColor)
            num = int(bright[index])
            text(letters[num], 0, 0)

            # Move to the next pixel
            index += 1
            # Move over for next character
            translate(1.0 / fontSize, 0)

        popMatrix()

    popMatrix()
    if cheatScreen:
        #image(video, 0, height - video.height)
        # set() is faster than image() when drawing untransformed images
        set(0, height - video.height, video)

"""
Handle key presses:
'c' toggles the cheat screen that shows the original image in the corner
'g' grabs an image and saves the frame to a tiff image
'f' and 'F' increase and decrease the font size
"""


def keyPressed():
    switch(key)
        case 'g':
            saveFrame()break
        case 'c':
            cheatScreen = !cheatScreenbreak
        case 'f':
            fontSize *= 1.1break
        case 'F':
            fontSize *= 0.9break

