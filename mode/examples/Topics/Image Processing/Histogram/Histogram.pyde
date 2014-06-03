"""
Histogram. 

Calculates the histogram of an image. 
A histogram is the frequency distribution 
of the gray levels with the number of pure black values
displayed on the left and number of pure white values on the right. 

Note that this sketch will behave differently on Android, 
since most images will no longer be full 24-bit color.
"""
size(640, 360)
# Load an image from the data directory
# Load a different image by modifying the comments
img = loadImage("frontier.jpg")
image(img, 0, 0)
hist = [0] * 256
# Calculate the histogram
for i in range(img.width):
    for j in range(img.height):
        bright = int(brightness(get(i, j)))
        hist[bright] += 1

# Find the largest value in the histogram
histMax = max(hist)
stroke(255)
# Draw half of the histogram (skip every second value)
for i in range(0, img.width, 2):
    # Map i (from 0..img.width) to a location in the histogram (0..255)
    which = int(map(i, 0, img.width, 0, 255))
    # Convert the histogram value to a location between
    # the bottom and the top of the picture
    y = int(map(hist[which], 0, histMax, img.height, 0))
    line(i, img.height, i, y)

