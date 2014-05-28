"""
Keyboard. 

Click on the image to give it focus and press the letter keys 
to create forms in time and space. Each key has a unique identifying 
number. These numbers can be used to position shapes in space. 
"""


def setup():
    size(640, 360)
    noStroke()
    background(0)
    global rectWidth
    rectWidth = width / 4


def draw():
    # Keep draw() here to continue looping while waiting for keys
    pass


def keyPressed():
    keyIndex = -1
    if 'A' <= key <= 'Z':
        keyIndex = ord(key) - ord('A')
    elif 'a' <= key <= 'z':
        keyIndex = ord(key) - ord('a')
    if keyIndex == -1:
        # If it's not a letter key, clear the screen
        background(0)
    else:
        # It's a letter key, fill a rectangle
        fill(millis() % 255)
        x = map(keyIndex, 0, 25, 0, width - rectWidth)
        rect(x, 0, rectWidth, height)

