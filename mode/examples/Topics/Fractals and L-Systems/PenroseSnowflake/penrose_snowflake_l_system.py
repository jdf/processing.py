from l_system import LSystem


class PenroseSnowflakeLSystem(LSystem):

    def __init__(self):
        self.axiom = "F3-F3-F3-F3-F"
        self.rule = ""
        self.steps = 0
        self.ruleF = "F3-F3-F45-F++F3-F"
        self.startLength = 450.0
        self.theta = radians(18)
        self.reset()

    def useRule(self, r_):
        self.rule = r_

    def useAxiom(self, a_):
        self.axiom = a_

    def useLength(self, l_):
        self.startLength = l_

    def useTheta(self, t_):
        self.theta = radians(t_)

    def reset(self):
        self.production = self.axiom
        self.drawLength = self.startLength
        self.generations = 0

    def getAge(self):
        return self.generations

    def render(self):
        translate(width, height)
        repeats = 1
        self.steps += 3
        if self.steps > len(self.production):
            self.steps = len(self.production)
        for i in range(self.steps):
            step = self.production[i]
            if step == 'F':
                for j in range(repeats):
                    line(0, 0, 0, -self.drawLength)
                    translate(0, -self.drawLength)
                repeats = 1
            elif step == '+':
                for j in range(repeats):
                    rotate(self.theta)
                repeats = 1
            elif step == '-':
                for j in range(repeats):
                    rotate(-self.theta)
                repeats = 1
            elif step == '[':
                pushMatrix()
            elif step == ']':
                popMatrix()
            # Use ord to get ASCII value of letter
            elif 48 <= ord(step) <= 57:
                repeats += ord(step) - 48

    def iterate(self, prod_, rule_):
        newProduction = ""
        for i in range(len(prod_)):
            step = self.production[i]
            if step == 'F':
                newProduction = newProduction + self.ruleF
            elif step != 'F':
                newProduction = newProduction + step

        self.drawLength = self.drawLength * 0.4
        self.generations += 1
        return newProduction

