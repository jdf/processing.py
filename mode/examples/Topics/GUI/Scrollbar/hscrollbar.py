class HScrollbar(object):

    def __init__(self, xpos, ypos, sWidth, sHeight, loosetemp):
        # width and height of bar
        self.sWidth = sWidth
        self.sHeight = sHeight
        widthtoheight = sWidth - sHeight
        self.ratio = float(sWidth) / float(widthtoheight)
        # x and y position of bar
        self.xpos = xpos
        self.ypos = ypos - self.sHeight / 2
        self.spos = self.xpos + self.sWidth / 2 - self.sHeight / 2
        self.newspos = self.spos
        self.sposMin = self.xpos
        self.sposMax = self.xpos + self.sWidth - self.sHeight
        self.loose = loosetemp
        # is the mouse over the slider?
        self.over = False
        self.locked = False

    def update(self):
        self.over = self.overEvent()
        self.locked = mousePressed and self.over
        if self.locked:
            self.newspos = constrain(mouseX - self.sHeight / 2,
                                     self.sposMin, self.sposMax)
        if abs(self.newspos - self.spos) > 1:
            self.spos = self.spos + (self.newspos - self.spos) / self.loose

    def overEvent(self):
        return (self.xpos < mouseX < self.xpos + self.sWidth
                and self.ypos < mouseY < self.ypos + self.sHeight)

    def display(self):
        noStroke()
        fill(204)
        rect(self.xpos, self.ypos, self.sWidth, self.sHeight)
        if self.over or self.locked:
            fill(0, 0, 0)
        else:
            fill(102, 102, 102)
        rect(self.spos, self.ypos, self.sHeight, self.sHeight)

    def getPos(self):
        # Convert spos to be values between
        # 0 and the total width of the scrollbar
        return self.spos * self.ratio
