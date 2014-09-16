"""
Keyboard Functions. 
Modified from code by Martin. 
Original 'Color Typewriter' concept by John Maeda. 
  
Click on the window to give it focus and press the letter keys to type colors. 
The keyboard function keyPressed() is called whenever
a key is pressed. keyReleased() is another keyboard
function that is called when a key is released.
"""

A_code = ord('A')
Z_code = ord('Z')
a_code = ord('a')
z_code = ord('z')

maxHeight = 40
minHeight = 20
letterHeight = maxHeight  # Height of the letters
letterWidth = 20  # Width of the letter

x = -letterWidth  # X position of the letters
y = 0  # Y position of the letters

newletter = False

numChars = 26  # There are 26 characters in the alphabet
colors = []


def setup():
    size(640, 360)
    noStroke()
    colorMode(HSB, numChars)
    background(numChars / 2)
    # Set a gray value for each key
    for i in range(0, numChars, 1):
        colors.append(color(i, numChars, numChars))


def draw():
    global newletter
    if newletter:
        # Draw the letter
        if letterHeight == maxHeight:
            y_pos = y
            rect(x, y_pos, letterWidth, letterHeight)
        else:
            y_pos = y + minHeight
            rect(x, y_pos, letterWidth, letterHeight)
            fill(numChars / 2)
            rect(x, y_pos - minHeight, letterWidth, letterHeight)
        newletter = False


def keyPressed():
    global newletter, x, y, letterHeight

    # If the key is between 'A'(65) to 'Z' and 'a' to 'z'(122)
    key_code = ord(key)
    if (key_code >= A_code and key_code <= Z_code) or (key_code >= a_code and key_code <= z_code):
        if key_code <= Z_code:
            keyIndex = key_code - A_code
            letterHeight = maxHeight
            fill(colors[key_code - A_code])
        else:
            keyIndex = key_code - a_code
            letterHeight = minHeight
            fill(colors[key_code - a_code])
    else:
        fill(0)
        letterHeight = 10

    newletter = True

    # Update the "letter" position
    x = (x + letterWidth)

    # Wrap horizontally
    if x > width - letterWidth:
        x = 0
        y += maxHeight

    # Wrap vertically
    if y > height - letterHeight:
        y = 0  # reset y to 0

