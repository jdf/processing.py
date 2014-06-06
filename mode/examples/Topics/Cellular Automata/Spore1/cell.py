import config


class Cell(object):

    def __init__(self, xin, yin):
        self.x = xin
        self.y = yin

    # Perform action based on surroundings.
    def run(self):
        # Fix cell coordinates.
        while(self.x < 0):
            self.x += width
        while(self.x > width - 1):
            self.x -= width
        while(self.y < 0):
            self.y += height
        while(self.y > height - 1):
            self.y -= height
        # Cell instructions.
        if config.w.getpix(self.x + 1, self.y) == config.black:
            self.move(0, 1)
        elif (config.w.getpix(self.x, self.y - 1) != config.black
              and config.w.getpix(self.x, self.y + 1) != config.black):
            self.move(int(random(9)) - 4, int(random(9)) - 4)

    # Will move the cell (dx, dy) units if that space is empty.
    def move(self, dx, dy):
        if config.w.getpix(self.x + dx, self.y + dy) == config.black:
            config.w.setpix(
                self.x + dx, self.y + dy, config.w.getpix(self.x, self.y))
            config.w.setpix(self.x, self.y, color(0))
            self.x += dx
            self.y += dy

