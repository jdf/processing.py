"""
 * List. 
 * 
 * A list is an ordered collection of data. Each piece of data in
 * a list is identified by an index number representing its position in 
 * the list. Lists are zero based, which means that the first 
 * element in the list is [0], the second element is [1], and so on. 
 * In this example, an array named "coswav" is created and
 * filled with the cosine values. This data is displayed three 
 * separate ways on the screen.    
 """

# You can create a new, empty list with a pair of square brackets:
coswave = []


def setup():
    size(640, 360)
    for i in range(width):
        amount = map(i, 0, width, 0, PI)
        # "append" adds an element to the end of a list.
        coswave.append(abs(cos(amount)))
    background(255)
    noLoop()


def draw():
    y1 = 0
    y2 = height / 3
    for i in range(0, width, 2):
        stroke(coswave[i] * 255)
        line(i, y1, i, y2)
    y1 = y2
    y2 = y1 + y1
    for i in range(0, width, 2):
        stroke(coswave[i] * 255 / 4)
        line(i, y1, i, y2)
    y1 = y2
    y2 = height
    for i in range(0, width, 2):
        stroke(255 - coswave[i] * 255)
        line(i, y1, i, y2)

