class LSystem(object):

    def __init__(self):
        self.steps = 0

        self.axiom = "F"
        self.rule = "F+F-F"
        self.startLength = 90.0
        self.theta = radians(120.0)
        reset()

    def reset(self):
        self.production = axiom
        self.drawLength = startLength
        self.generations = 0

    def getAge(self):
        return generations

    def render(self):
        translate(width / 2, height / 2)
        steps += 5
        if steps > len(production)():
            steps = len(production)()

        for i in range(steps):
            step = production.charAt(i)
            if step == 'F':
                rect(0, 0, -drawLength, -drawLength)
                noFill()
                translate(0, -drawLength)
            elif step == '+':
                rotate(theta)
            elif step == '-':
                rotate(-theta)
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
        newProduction = newProduction.replace("F", rule_)
        return newProduction

