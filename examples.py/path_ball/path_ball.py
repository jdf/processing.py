# n0vice.hasi
class turtle:
    '''
    A turtle like object in processing
    '''
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def show(self):
        '''
        updates changes to screen
        '''
        px = map(self.x, 0, 360, 0, width)
        py = map(self.y, -1, 1, 0, height)
        circle(px, py, 20)

def setup():
    size(600, 400)
    
t = turtle()
x = 0
dx = 4
switch = False
li = [] # List to store coordinates of previous points
c = (random(255), random(255), random(255))
c = (255, 102, 204)

def draw():
    global x, switch, dx, li, c
    background(0)
    
    fill(c[0], c[1], c[2])
    stroke(c[0], c[1], c[2])
    strokeWeight(3)
    
    # If angle is less than 361 follow sin(x) path
    if not switch:
        y = sin(radians(x))
        x += dx
        if x >= 361:
            switch = True
    # After 360 degree follow -sin(x) path
    if switch:
        y = -sin(radians(x))
        x -= dx
        if x == 0:
            switch = False
    plot()
    
    # Remember the coordinates of previous points
    li.append((x,y))
    for i in range(len(li)):
        stroke(c[0], c[1], c[2])
        t.x = li[i][0]
        t.y = li[i][1]
        t.show()
    
    # Remove one point after every 30 points
    if len(li) % 30 == 0:
        li.pop(0)
    
def plot():
    '''
    Function to plot the path of the curves sin(x), -sin(x) that the ball follows
    '''
    x = 0
    for i in range(360):
        y = sin(radians(x))
        px = map(x, 0, 360, 0, width)
        py = map(y, -1, 1, 0, height)
        point(px, py)
        x += dx
    x = 0
    for i in range(360):
        y = -sin(radians(x))
        px = map(x, 0, 360, 0, width)
        py = map(y, -1, 1, 0, height)
        point(px, py)
        x += dx
