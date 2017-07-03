"""
Wolfram Cellular Automata by Daniel Shiffman.

Simple demonstration of a Wolfram 1-dimensional cellular automata
When the system reaches bottom of the window, it restarts with a new ruleset
Mouse click restarts as well. 
"""

from CA import CA   # Object to describe the Wolfram basic Cellular Automata

def setup():
    global ca
    size(640, 360)
    ruleset = [0, 1, 0, 1, 1, 0, 1, 0]  # An initial rule system
    ca = CA(ruleset)                    # Initialize CA
    background(0)


def draw():
    ca.render()      # Draw the CA
    ca.generate()    # Generate the next level

    # If we're done, clear the screen, pick a new ruleset and restart
    if ca.finished():
        background(0)
        ca.randomize()
        ca.restart()

def mousePressed():
    background(0)
    ca.randomize()
    ca.restart()
