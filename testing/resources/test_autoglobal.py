x = 0

def setup():
    size(100, 100)
    noLoop()
    x += 1

def draw():
    assert x == 1
    print 'OK'
    exit()