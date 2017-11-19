def settings():
	size(48, 48, P2D)

def draw():
    if frameCount > 1:
    	raise Exception("Expected to exit.")
    assert(keyPressed == False)
    __keyPressed__()

def keyPressed():
	print "OK"
	exit()