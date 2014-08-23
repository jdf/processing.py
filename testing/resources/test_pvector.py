a = PVector()
assert a.x == 0
assert a.y == 0
assert a.z == 0

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
assert PVector.dot(a, b) == 0

d = a.get()
d += b
assert d == a + b
d = a.get()
d -= c
assert d == a - c
d = a.get()
d *= 5.0
assert d == a * 5.0
d = a.get()
d /= 5.0
assert d == a / 5.0

assert b * 5 == b * 5.0
assert b / 5 == b / 5.0
d = b.get()
d *= 391
assert d == b * 391.0
d = b.get()
d /= 10203
assert d == b / 10203.0

d = a.get()
d += a + a
assert d == a + a + a

assert a * 57.0 == 57.0 * a

assert (a / 5.0) == (1.0 / 5.0) * a

m, n = b, c
a += b * 5 - c / 2 + PVector(0, 1, 2)
assert (m, n) == (b, c)

import copy
x = [a, b]
y = copy.deepcopy(x)

assert x == y
x[0].sub(PVector(100, 100, 100))
assert x != y

a = PVector(1, 1)
b = PVector(-2, -2)
assert a < b
assert a <= b
assert b > a
assert b >= a
a = PVector(1, 2, 3)
b = PVector(3, 2, 1)
assert a != b
assert a >= b
assert b >= a
assert a.magSq() == b.magSq()

v1 = PVector(10, 20);
v2 = PVector(60, 80); 
a = PVector.angleBetween(v1, v2);
assert a == 0.17985349893569946  # more or less

# Regression test for https://github.com/jdf/Processing.py-Bugs/issues/67
assert isinstance(PVector(1,2), PVector)

# Regression test for https://github.com/jdf/Processing.py-Bugs/issues/101
v = PVector(10, 20, 0)
d = v.dot(60, 80, 0)
assert d == 2200.0
v2 = PVector(60, 80, 0)
d = v.dot(v2)
assert d == 2200.0

print 'OK'

exit()
