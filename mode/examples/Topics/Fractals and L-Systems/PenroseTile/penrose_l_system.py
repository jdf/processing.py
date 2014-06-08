from l_system import LSystem


class PenroseLSystem(LSystem):

    def __init__(self):
        self.axiom = "[X]++[X]++[X]++[X]++[X]"
        self.rule = ""
        self.steps = 0
        self.ruleW = "YF++ZF4-XF[-YF4-WF]++"
        self.ruleX = "+YF--ZF[3-WF--XF]+"
        self.ruleY = "-WF++XF[+++YF++ZF]-"
        self.ruleZ = "--YF++++WF[+ZF++++XF]--XF"
        self.startLength = 460.0
        self.theta = radians(36)
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
        translate(width / 2, height / 2)
        pushes = 0
        repeats = 1
        self.steps += 12
        if self.steps > len(self.production):
            self.steps = len(self.production)

        for i in range(self.steps):
            step = self.production[i]
            if step == 'F':
                stroke(255, 60)
                for j in range(repeats):
                    line(0, 0, 0, -self.drawLength)
                    noFill()
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
                pushes += 1
                pushMatrix()
            elif step == ']':
                popMatrix()
                pushes -= 1
            # Use ord to get ASCII value of letter
            elif (ord(step) >= 48) and (ord(step) <= 57):
                repeats = ord(step) - 48
        while pushes > 0:
            popMatrix()
            pushes -= 1

    def iterate(self, prod_, rule_):
        newProduction = ""
        for i in range(len(prod_)):
            step = self.production[i]
            if step == 'W':
                newProduction = newProduction + self.ruleW
            elif step == 'X':
                newProduction = newProduction + self.ruleX
            elif step == 'Y':
                newProduction = newProduction + self.ruleY
            elif step == 'Z':
                newProduction = newProduction + self.ruleZ
            elif step != 'F':
                newProduction = newProduction + step
        self.drawLength = self.drawLength * 0.5
        self.generations += 1
        return newProduction

