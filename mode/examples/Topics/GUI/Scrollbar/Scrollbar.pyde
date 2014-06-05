"""
Scrollbar. 

Move the scrollbars left and right to change the positions of the images. 
"""
# Two scrollbars
hs1 = None
hs2 = None
# Two images to load
img1 = None
img2 = None


def setup():
    size(640, 360)
    noStroke()
    hs1 = HScrollbar(0, height / 2 - 8, width, 16, 16)
    hs2 = HScrollbar(0, height / 2 + 8, width, 16, 16)
    # Load images
    img1 = loadImage("seedTop.jpg")
    img2 = loadImage("seedBottom.jpg")


def draw():
    background(255)
    # Get the position of the img1 scrollbar
    # and convert to a value to display the img1 image.
    img1Pos = hs1.getPos() - width / 2
    fill(255)
    image(img1, width / 2 - img1.width / 2 + img1Pos * 1.5, 0)
    # Get the position of the img2 scrollbar
    # and convert to a value to display the img2 image.
    img2Pos = hs2.getPos() - width / 2
    fill(255)
    image(img2, width / 2 - img2.width / 2 + img2Pos * 1.5, height / 2)
    hs1.update()
    hs2.update()
    hs1.display()
    hs2.display()
    stroke(0)
    line(0, height / 2, width, height / 2)


class HScrollbar(object):

    def __init__(self, xp, yp, sw, sh, loosetemp):
        # width and height of bar
        self.swidth = sw
        self.sheight = sh
        widthtoheight = sw - sh
        self.ratio = float(sw) / float(widthtoheight)
        # x and y position of bar
        self.xpos = xp
        self.ypos = yp - self.sheight / 2
        self.spos = self.xpos + self.swidth / 2 - self.sheight / 2
        self.newspos = self.spos
        self.sposMin = self.xpos
        self.sposMax = self.xpos + self.swidth - self.sheight
        self.loose = loosetemp
        # is the mouse over the slider?
        self.over = False
        self.locked = False

    def update(self):
        self.over = self.overEvent()
        self.locked = mousePressed and self.over
        if self.locked:
            self.newspos = constrain(
                mouseX - self.sheight / 2, self.sposMin, self.sposMax)
        if abs(self.newspos - self.spos) > 1:
            self.spos = self.spos + (self.newspos - self.spos) / self.loose

    def overEvent(self):
        return self.xpos < mouseX < self.xpos + self.swidth and self.ypos < mouseY < self.ypos + self.sheight

    def display(self):
        noStroke()
        fill(204)
        rect(self.xpos, self.ypos, self.swidth, self.sheight)
        if self.over or self.locked:
            fill(0, 0, 0)
        else:
            fill(102, 102, 102)
        rect(self.spos, self.ypos, self.sheight, self.sheight)

    def getPos(self):
        # Convert spos to be values between
        # 0 and the total width of the scrollbar
        return self.spos * self.ratio

