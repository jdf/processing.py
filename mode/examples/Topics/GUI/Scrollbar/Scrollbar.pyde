"""
Scrollbar. 

Move the scrollbars left and right to change the positions of the images. 
"""
# The next line is needed if running in JavaScript Mode with Processing.js
""" @pjs preload="seedTop.jpg,seedBottom.jpg"""" 
HScrollbar hs1, hs2# Two scrollbars
PImage img1, img2# Two images to load
def setup(): 
    size(640, 360)
    noStroke()
    
    hs1 = HScrollbar(0, height/2-8, width, 16, 16)
    hs2 = HScrollbar(0, height/2+8, width, 16, 16)
    
    # Load images
    img1 = loadImage("seedTop.jpg")
    img2 = loadImage("seedBottom.jpg")
def draw(): 
    background(255)
    
    # Get the position of the img1 scrollbar
    # and convert to a value to display the img1 image 
    img1Pos = hs1.getPos()-width/2
    fill(255)
    image(img1, width/2-img1.width/2 + img1Pos*1.5, 0)
    
    # Get the position of the img2 scrollbar
    # and convert to a value to display the img2 image
    img2Pos = hs2.getPos()-width/2
    fill(255)
    image(img2, width/2-img2.width/2 + img2Pos*1.5, height/2)
 
    hs1.update()
    hs2.update()
    hs1.display()
    hs2.display()
    
    stroke(0)
    line(0, height/2, width, height/2)
class HScrollbar(object): 
    swidth, sheight# width and height of bar
    xpos, ypos# x and y position of bar
    spos, newspos# x position of slider
    sposMin, sposMax# max and min values of slider
    loose# how loose/heavy
    boolean over# is the mouse over the slider?
    boolean locked
    ratio
    HScrollbar (xp, yp, sw, sh, l) 
        swidth = sw
        sheight = sh
        widthtoheight = sw - sh
        ratio = (float)sw / (float)widthtoheight
        xpos = xp
        ypos = yp-sheight/2
        spos = xpos + swidth/2 - sheight/2
        newspos = spos
        sposMin = xpos
        sposMax = xpos + swidth - sheight
        loose = l
    
    def update(): 
        if overEvent():
            over = True
        else:
            over = False
        
        if mousePressed and over:
            locked = True
        
        if !mousePressed:
            locked = False
        
        if locked:
            newspos = constrain(mouseX-sheight/2, sposMin, sposMax)
        
        if abs(newspos - spos) > 1:
            spos = spos + (newspos-spos)/loose
        
    
    def constrain(val, minv, maxv): 
        return min(max(val, minv), maxv)
    
    boolean overEvent() 
        if (mouseX > xpos and mouseX < xpos+swidth and
             mouseY > ypos and mouseY < ypos+sheight) 
            return True
        else:
            return False
        
    
    def display(): 
        noStroke()
        fill(204)
        rect(xpos, ypos, swidth, sheight)
        if over or locked:
            fill(0, 0, 0)
        else:
            fill(102, 102, 102)
        
        rect(spos, ypos, sheight, sheight)
    
    def getPos(): 
        # Convert spos to be values between
        # 0 and the total width of the scrollbar
        return spos * ratio
    
