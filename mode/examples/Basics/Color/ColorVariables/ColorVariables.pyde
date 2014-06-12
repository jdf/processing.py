"""
Color Variables (Homage to Albers). 

This example creates variables for colors that may be referred to 
in the program by a name, rather than a number. 
"""
size(640, 360)
noStroke()
background(51, 0, 0)
inside = color(204, 102, 0)
middle = color(204, 153, 0)
outside = color(153, 51, 0)
# These statements are equivalent to the statements above.
# Programmers may use the format they prefer.
#inside = 0xCC6600
#middle = 0xCC9900
#outside = 0x993300
with pushMatrix():
    translate(80, 80)
    fill(outside)
    rect(0, 0, 200, 200)
    fill(middle)
    rect(40, 60, 120, 120)
    fill(inside)
    rect(60, 90, 80, 80)
with pushMatrix():
    translate(360, 80)
    fill(inside)
    rect(0, 0, 200, 200)
    fill(outside)
    rect(40, 60, 120, 120)
    fill(middle)
    rect(60, 90, 80, 80)

