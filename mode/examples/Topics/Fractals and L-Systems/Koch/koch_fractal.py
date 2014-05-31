# Koch Curve
# A class to manage the list of line segments in the snowflake pattern.

from koch_line import KochLine


class KochFractal(object):

    def __init__(self):
        self.count = 0
        self.start = PVector(0, height - 20)  # A PVector for the start
        self.end = PVector(width, height - 20)  # A PVector for the end
        self.lines = []  # A list to keep track of all the lines
        self.restart()

    def nextLevel(self):
        # For every line that is in the list
        # create 4 more lines in a list
        self.lines = self.iterate(self.lines)
        self.count += 1

    def restart(self):
        self.count = 0  # Reset count
        self.lines = []  # Empty the list
        # Add the initial line (from one end PVector to the other)
        self.lines.append(KochLine(self.start, self.end))

    # This is easy, just draw all the lines
    def render(self):
        for i in self.lines:
            i.display()

    # This is where the **MAGIC** happens
    # Step 1: Create an empty list
    # Step 2: For every line currently in the list
    #     - calculate 4 line segments based on Koch algorithm
    #     - add all 4 line segments into the list
    # Step 3: Return the list and it becomes the list of line segments
    # for the structure

    # As we do this over and over again, each line gets broken into 4 lines,
    # which gets broken into 4 lines, and so on. . .

    def iterate(self, before):
        now = []
        for i in before:
            # Calculate 5 koch PVectors (done for us by the line object)
            a = i.start()
            b = i.kochleft()
            c = i.kochmiddle()
            d = i.kochright()
            e = i.end()
            # Make line segments between all the PVectors and add them
            now.append(KochLine(a, b))
            now.append(KochLine(b, c))
            now.append(KochLine(c, d))
            now.append(KochLine(d, e))
        return now

