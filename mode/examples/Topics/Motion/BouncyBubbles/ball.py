import config

class Ball(object):
    # Exciting! *Class* variables! These are shared amongst all
    # *instances* of Ball.
    Spring = 0.05
    Gravity = 0.03
    Friction = -0.9

    def __init__(self, x, y, radius, id, others):
        self.x = x
        self.y = y
        self.radius = radius
        self.id = id
        self.others = others
        self.vx = 0
        self.vy = 0

    def collide(self):
        for i in range(self.id + 1, config.NUM_BALLS):
            dx = self.others[i].x - self.x
            dy = self.others[i].y - self.y
            distance = sqrt(dx * dx + dy * dy)
            minDist = self.others[i].radius + self.radius
            if distance < minDist:
                angle = atan2(dy, dx)
                targetX = self.x + cos(angle) * minDist
                targetY = self.y + sin(angle) * minDist
                ax = (targetX - self.others[i].x) * Ball.Spring
                ay = (targetY - self.others[i].y) * Ball.Spring
                self.vx -= ax
                self.vy -= ay
                self.others[i].vx += ax
                self.others[i].vy += ay

    def move(self):
        self.vy += Ball.Gravity
        self.x += self.vx
        self.y += self.vy

        if self.x + self.radius > width:
            self.x = width - self.radius
            self.vx *= Ball.Friction
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= Ball.Friction
        if self.y + self.radius > height:
            self.y = height - self.radius
            self.vy *= Ball.Friction
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= Ball.Friction

    def display(self):
        ellipse(self.x, self.y, self.radius, self.radius)
