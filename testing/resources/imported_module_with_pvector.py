def sayok():
    a = PVector(5, 7, 11)
    b = PVector(13, 17, 23)
    assert a - b == PVector(-8.0, -10.0, -12.0)
    print "OK!"
