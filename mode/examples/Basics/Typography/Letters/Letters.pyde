"""
 * Letters. 
 * 
 * Draws letters to the screen. This requires loading a font, 
 * setting the font, and then drawing the letters.
 """


def setup():
    size(640, 360)
    background(0)
    # Create the font
    printArray(PFont.list())
    f = createFont("Georgia", 24)
    textFont(f)
    textAlign(CENTER, CENTER)


def draw():
    background(0)
    # Set the left and top margin
    margin = 10
    translate(margin * 4, margin * 4)
    gap = 46
    counter = 35

    for y in range(0, height - gap, gap):
        for x in range(0, width - gap, gap):
            letter = chr(counter)
            if letter in 'AEIOU':
                fill(255, 204, 0)
            else:
                fill(255)
            # Draw the letter to the screen
            text(letter, x, y)
            # Increment the counter
            counter += 1

