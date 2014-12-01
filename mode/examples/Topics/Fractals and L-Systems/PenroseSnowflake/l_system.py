class LSystem(object):

    def __init__(self):
        self.steps = 0
        self.axiom = "F"
        self.rule = "F+F-F"
        self.startLength = 90.0
        self.theta = radians(120.0)
        self.reset()

    def reset(self):
        self.production = self.axiom
        self.drawLength = self.startLength
        self.generations = 0

    def getAge(self):
        return self.generations

    def render(self):
        translate(width / 2, height / 2)
        self.steps += 5
        if self.steps > len(self.production)():
            self.steps = len(self.production)()
        for i in range(self.steps):
            step = self.production.charAt(i)
            if step == 'F':
                rect(0, 0, -self.drawLength, -self.drawLength)
                noFill()
                translate(0, -self.drawLength)
            elif step == '+':
                rotate(self.theta)
            elif step == '-':
                rotate(-self.theta)
            elif step == '[':
                pushMatrix()
            elif step == ']':
                popMatrix()

    def simulate(self, gen):
        while self.getAge() < gen:
            self.production = self.iterate(self.production, self.rule)

    def iterate(self, prod_, rule_):
        self.drawLength = self.drawLength * 0.6
        self.generations += 1
        newProduction = prod_
        newProduction = newProduction.replaceAll("F", rule_)
        return newProduction

