"""
Blur.

A low-pass filter blurs an image. This program analyzes every
pixel in an image and blends it with the neighboring pixels
to blur the image.
"""
v = 1.0 / 9.0
kernel = [[v, v, v],
          [v, v, v],
          [v, v, v]]
img = loadImage("moon.jpg")  # Load the original image


def setup():
    size(640, 360)
    noLoop()


def draw():
    image(img, 0, 0)  # Displays the image from point (0,0)
    img.loadPixels()
    # Create an opaque image of the same size as the original
    edgeImg = createImage(img.width, img.height, RGB)
    # Loop through every pixel in the image
    for y in range(1, img.height - 1):  # Skip top and bottom edges
        for x in range(1, img.width - 1):  # Skip left and right edges
            kernelSum = 0  # Kernel sum for this pixel
            for ky in (-1, 0, 1):
                for kx in (-1, 0, 1):
                    # Calculate the adjacent pixel for this kernel point
                    pos = (y + ky) * img.width + (x + kx)
                    # Image is grayscale, red/green/blue are identical
                    val = red(img.pixels[pos])
                    # Multiply adjacent pixels based on the kernel values
                    kernelSum += kernel[ky + 1][kx + 1] * val

            # For this pixel in the image, set the gray value
            # based on the sum from the kernel
            edgeImg.pixels[y * img.width + x] = color(kernelSum)

    # State that there are changes to edgeImg.pixels[]
    edgeImg.updatePixels()
    image(edgeImg, width / 2, 0)  # Draw the image
