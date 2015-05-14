# Regression test for lerpColor dying when used before setup() in a dynamic mode sketch.
assert lerpColor(0, 100, .5) == 50

def setup():
    print 'OK'
    exit()
