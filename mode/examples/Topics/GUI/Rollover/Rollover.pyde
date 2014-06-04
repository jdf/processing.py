"""
Rollover. 

Roll over the colored squares in the center of the image
to change the color of the outside rectangle. 
"""
 
 
rectX, rectY# Position of square button
circleX, circleY# Position of circle button
rectSize = 90# Diameter of rect
circleSize = 93# Diameter of circle
color rectColor
color circleColor
color baseColor
boolean rectOver = False
boolean circleOver = False
def setup(): 
    size(640, 360)
    rectColor = color(0)
    circleColor = color(255)
    baseColor = color(102)
    circleX = width/2+circleSize/2+10
    circleY = height/2
    rectX = width/2-rectSize-10
    rectY = height/2-rectSize/2
    ellipseMode(CENTER)
def draw(): 
    update(mouseX, mouseY)
    noStroke()
    if rectOver:
        background(rectColor)
    elif circleOver:
        background(circleColor)
    else:
        background(baseColor)
    
    stroke(255)
    fill(rectColor)
    rect(rectX, rectY, rectSize, rectSize)
    stroke(0)
    fill(circleColor)
    ellipse(circleX, circleY, circleSize, circleSize)
def update(x, y): 
    if  overCircle(circleX, circleY, circleSize) :
        circleOver = True
        rectOver = False
    elif  overRect(rectX, rectY, rectSize, rectSize) :
        rectOver = True
        circleOver = False
    else:
        circleOver = rectOver = False
    
boolean overRect(x, y, width, height) 
    if (mouseX >= x and mouseX <= x+width and 
            mouseY >= y and mouseY <= y+height) 
        return True
    else:
        return False
    
boolean overCircle(x, y, diameter) 
    disX = x - mouseX
    disY = y - mouseY
    if sqrt(sq(disX) + sq(disY)) < diameter/2 :
        return True
    else:
        return False
    
