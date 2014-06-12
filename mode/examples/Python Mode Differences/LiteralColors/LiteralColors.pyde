# Color demo.
size(400, 400)

# Default color mode treats 0-255 as a range
# from black to white in gray scale.
fill(255)
rect(0, 0, width, height)

# New to Python mode, since you can't use a bare
# hash mark (because of Python comments), you can
# use a string formatted like a CSS color spec.
fill('#0000FF')
rect(100, 100, 100, 100)

fill(255)
text("I am blue", 105, 116)

# lerpColor takes hex ARGB, a CSS-style string, or the
# result of a call to color().
c1 = color(255, 0, 0, 100)
c2 = '#0000FF'
fill(lerpColor(c1, c2, .5))
rect(150, 150, 100, 100)

fill(255)
with pushMatrix():
    translate(160, 234)
    rotate(-PI / 4)
    text("I am\ntranslucent purple", 0, 0)

# You can use hex constants, but must explicitly
# specify the alpha in the high order bits.
fill(0xFFFF0000)
rect(230, 200, 100, 100)
fill(0)
text('Red here.', 240, 218)
