class CA:
    
    def __init__(self, r):
        self.rules = r  # List that stores the ruleset, i.e. 0,1,1,0,1,1,0,1
        self.scl = 1    # How many pixels wide/high is each cell?
        self.cells = [0] * int(width / self.scl)
        self.restart()  # Sets self.generation to 0, only middle cell to 1

    # Set the rules of the CA
    def setRules(self, r):
        self.rules = r

    # Make a random ruleset
    def randomize(self):
        for i in range(8):
            self.rules[i] = int(random(2))

    # Reset to generation 0
    def restart(self):
        for i in range(len(self.cells)):
            self.cells[i] = 0

        # We arbitrarily start with just the middle cell having a state of "1"
        self.cells[len(self.cells) / 2] = 1
        self.generation = 0

    # The process of creating the new generation
    def generate(self):
        # First we create an empty array for the new values
        nextgen = [0] * len(self.cells)
        # For every spot, determine new state by examing current state,
        # and neighbor states
        # Ignore edges that only have one neighbor
        for i in range(1, len(self.cells) - 1):
            left = self.cells[i - 1]     # Left neighbor state
            me = self.cells[i]           # Current state
            right = self.cells[i + 1]    # Right neighbor state
            # Compute next generation state based on ruleset
            nextgen[i] = self.executeRules(left, me, right)

        # Copy the array into current value
        for i in range(1, len(self.cells) - 1):
            self.cells[i] = nextgen[i]

        self.generation += 1

    # This is the easy part, just draw the cells, 
    # fill 255 for '1', fill 0 for'0'
    def render(self):
        scl = self.scl
        for i in range(len(self.cells)):
            if (self.cells[i] == 1):
                fill(255)
            else:
                fill(0)

            noStroke()
            rect(i * scl, self.generation * scl, scl, scl)

    # Implementing the Wolfram rules
    # Could be improved and made more concise, but here we can 
    # explicitly see what is going on for each case
    def executeRules(self, a, b, c):
        if a == 1 and b == 1 and c == 1:
            return self.rules[0]
        if a == 1 and b == 1 and c == 0:
            return self.rules[1]
        if a == 1 and b == 0 and c == 1:
            return self.rules[2]
        if a == 1 and b == 0 and c == 0:
            return self.rules[3]
        if a == 0 and b == 1 and c == 1:
            return self.rules[4]
        if a == 0 and b == 1 and c == 0:
            return self.rules[5]
        if a == 0 and b == 0 and c == 1:
            return self.rules[6]
        if a == 0 and b == 0 and c == 0:
            return self.rules[7]
        return 0

    # The CA is done if it reaches the bottom of the screen
    def finished(self):
        if self.generation > height / self.scl:
            return True
        else:
            return False
