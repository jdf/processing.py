class CA(object):

    def __init__(self, r):
        # A list to store the ruleset, for example 0,1,1,0,1,1,0,1.
        self.rules = r
        self.scl = 1  # How many pixels wide/high is each cell?
        self.cells = [0] * width  # A list of 0s and 1s.
        self.generation = 0  # How many generations?
        self.restart()

    # Set the rules of the CA.
    def setRules(self, r):
        self.rules = r

    # Make a random ruleset.
    def randomize(self):
        for i in range(8):
            self.rules[i] = int(random(2))

    # Reset to generation 0.
    def restart(self):
        for cell in self.cells:
            cell = 0
        # We arbitrarily start with just the middle cell having a state of "1".
        self.cells[len(self.cells) / 2] = 1
        self.generation = 0

    # The process of creating the generation.
    def generate(self):
        # First we create an empty list for the values.
        nextgen = [0] * len(self.cells)
        # For every spot, determine state by examing current state, and neighbor states.
        # Ignore edges that only have one neighor.
        for i in range(1, len(self.cells) - 1):
            left = self.cells[i - 1]  # Left neighbor state.
            me = self.cells[i]  # Current state.
            right = self.cells[i + 1]  # Right neighbor state.
            # Compute next generation state based on ruleset.
            nextgen[i] = self.executeRules(left, me, right)
        # Copy the list into current value.
        for i in range(1, len(self.cells) - 1):
            self.cells[i] = nextgen[i]
        self.generation += 1

    # This is the easy part, just draw the cells, fill 255 for '1', fill 0 for
    # '0'.
    def render(self):
        for i in range(len(self.cells)):
            if self.cells[i] == 1:
                fill(255)
            else:
                fill(0)
            noStroke()
            rect(i * self.scl, self.generation * self.scl, self.scl, self.scl)

    # Implementing the Wolfram rules.
    # Could be improved and made more concise, but here we can explicitly see
    # what is going on for each case.
    def executeRules(self, a, b, c):
        return self.rules[int(str(a) + str(b) + str(c), base=2)]

    # The CA is done if it reaches the bottom of the screen.
    def finished(self):
        return self.generation > height / self.scl

