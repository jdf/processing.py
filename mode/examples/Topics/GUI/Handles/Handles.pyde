"""
Handles. 

Click and drag the white boxes to change their position. 
"""

handles = []


def setup():
    size(640, 360)
    num = height / 15
    hsize = 10
    for i in range(num):
        handles.append(
            Handle(width / 2, 10 + i * 15, 50 - hsize / 2, 10, handles))


def draw():
    background(153)
    for i in range(len(handles)):
        handles[i].update()
        handles[i].display()
    fill(0)
    rect(0, 0, width / 2, height)


def mouseReleased():
    for i in range(len(handles)):
        handles[i].releaseEvent()


class Handle(object):

    def __init__(self, ix, iy, il, s, o):
        self.x = ix
        self.y = iy
        self.stretch = il
        self.size = s
        self.boxx = self.x + self.stretch - self.size / 2
        self.boxy = self.y - self.size / 2
        self.others = o
        self.over = False
        self.press = False
        self.locked = False
        self.otherslocked = False

    def update(self):
        self.boxx = self.x + self.stretch
        self.boxy = self.y - self.size / 2
        for i in range(len(self.others)):
            if self.others[i].locked == True:
                self.otherslocked = True
                break
            else:
                self.otherslocked = False
        if self.otherslocked == False:
            self.overEvent()
            self.pressEvent()
        if self.press:
            self.stretch = lock(
                mouseX - width / 2 - self.size / 2, 0, width / 2 - self.size - 1)

    def overEvent(self):
        self.over = overRect(self.boxx, self.boxy, self.size, self.size)

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
        rect(self.boxx, self.boxy, self.size, self.size)
        if self.over or self.press:
            line(self.boxx, self.boxy, self.boxx +
                 self.size, self.boxy + self.size)
            line(self.boxx, self.boxy + self.size,
                 self.boxx + self.size, self.boxy)


def overRect(x, y, width, height):
    return x <= mouseX <= x + width and y <= mouseY <= y + height


def lock(val, minv, maxv):
    return min(max(val, minv), maxv)

