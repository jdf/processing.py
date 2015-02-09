class Handle(object):

    def __init__(self, x, y, stretch, size, others):
        self.x = x
        self.y = y
        self.stretch = stretch
        self.size = size
        self.boxX = self.x + self.stretch - self.size / 2
        self.boxY = self.y - self.size / 2
        self.others = others
        self.over = False
        self.press = False
        self.locked = False
        self.othersLocked = False

    def update(self):
        self.boxX = self.x + self.stretch
        self.boxY = self.y - self.size / 2

        self.othersLocked = False
        for handle in self.others:
            if handle.locked:
                self.othersLocked = True
                break
        if not self.othersLocked:
            self.overEvent()
            self.pressEvent()
        if self.press:
            self.stretch = constrain(mouseX - width / 2 - self.size / 2,
                                     0, width / 2 - self.size - 1)

    def overEvent(self):
        self.over = overRect(self.boxX, self.boxY, self.size, self.size)

    def pressEvent(self):
        if self.over and mousePressed or self.locked:
            self.press = True
            self.locked = True
        else:
            self.press = False

    def releaseEvent(self):
        self.locked = False

    def display(self):
        line(self.x, self.y, self.x + self.stretch, self.y)
        fill(255)
        stroke(0)
        rect(self.boxX, self.boxY, self.size, self.size)
        if self.over or self.press:
            line(self.boxX, self.boxY,
                 self.boxX + self.size, self.boxY + self.size)
            line(self.boxX, self.boxY + self.size,
                 self.boxX + self.size, self.boxY)


def overRect(x, y, width, height):
    return x <= mouseX <= x + width and y <= mouseY <= y + height
