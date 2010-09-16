a = PVector(5, 7, 11)
b = PVector(13, 17, 23)
assert a - b == PVector(-8.0, -10.0, -12.0)
print b - a
print b + a
print a + b

print PVector.add(a, b)
print PVector.add(a, b)
a.add(b)
print a
a.add(b)
print a

print a * b
print a * 10
print a * 10
a.mult(10)
print a

print PVector.dist(a, b)
print PVector.cross(a, b)
print PVector.dot(a, b)
