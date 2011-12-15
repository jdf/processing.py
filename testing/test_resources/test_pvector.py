a = PVector(5, 7, 11)
b = PVector(13, 17, 23)
assert a - b == PVector(-8.0, -10.0, -12.0)
assert b - a == PVector(8, 10, 12)
c = PVector(18, 24, 34)
assert b + a == c
assert a + b == c
assert PVector.add(a, b) == c
assert PVector.add(a, b) == c
a.add(b)
assert a == c
a.add(b)
assert a == PVector(31.0, 41.0, 57.0)

try:
    print a * b
    raise AssertionError("That shouldn't have happened.")
except TypeError:
    pass

c = PVector(310.0, 410.0, 570.0)
assert a * 10 == c
assert a * 10 == c
assert PVector.mult(a, 10) == c
assert PVector.mult(a, 10) == c
a.mult(10)
assert a == c

assert int(1000 * PVector.dist(a, b)) == 736116
assert PVector.cross(a, b) == PVector(-260.0, 280.0, -60.0)
assert a.cross(b) == PVector(-260.0, 280.0, -60.0)
assert PVector.dot(a, b) == 24110.0

import copy
x = [a, b]
y = copy.deepcopy(x)

assert x == y
x[0].sub(PVector(100, 100, 100))
assert x != y

print 'OK'

exit()
