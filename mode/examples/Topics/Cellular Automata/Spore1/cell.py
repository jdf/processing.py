class Cell(object):
    
    x = 0
    y = 0

    def __init__(self, xin, yin):
        self.x = xin
        self.y = yin

        # Perform action based on surroundings
    def run(self):
        # Fix cell coordinates
        while(self.x < 0):
            self.x += width

        while(self.x > width - 1):
            self.x -= width

        while(self.y < 0):
            self.y += height

        while(self.y > height - 1):
            self.y -= height

        # Cell instructions
        if w.getpix(self.x + 1, self.y) == black:
            move(0, 1)
        elif w.getpix(self.x, self.y - 1) != black and w.getpix(self.x, self.y + 1) != black:
            move(int(random(9)) - 4, int(random(9)) - 4)

    # Will move the cell (dx, dy) units if that space is empty
    def move(self, dx, dy):
        if w.getpix(self.x + dx, self.y + dy) == black:
            w.setpix(self.x + dx, self.y + dy, w.getpix(self.x, self.y))
            w.setpix(x, y, color(0))
            x += dx
            y += dy

