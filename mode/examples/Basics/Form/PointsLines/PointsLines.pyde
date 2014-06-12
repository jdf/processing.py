"""
Points and Lines. 

Points and lines can be used to draw basic geometry.
Change the value of the variable 'd' to scale the form.
The four variables set the positions based on the value of 'd'. 
"""

d = 70
p1 = d
p2 = p1 + d
p3 = p2 + d
p4 = p3 + d
size(640, 360)
noSmooth()
background(0)
translate(140, 0)
# Draw gray box
stroke(153)
line(p3, p3, p2, p3)
line(p2, p3, p2, p2)
line(p2, p2, p3, p2)
line(p3, p2, p3, p3)
# Draw white points
stroke(255)
point(p1, p1)
point(p1, p3)
point(p2, p4)
point(p3, p1)
point(p4, p2)
point(p4, p4)

