# Processing builtin
# set(x, y, c)
set(10, 10, color(0, 0, 128))

assert get(10,10) & 0x00FFFFFF == 128

# Python builtin
s = set()
s.add('banana')
assert 'banana' in s
assert len(s) == 1
assert 'apple' not in s

# subclass
class MySet(set):
    def __init__(self):
        set.__init__(self)
assert issubclass(MySet, set)
foo = MySet()
foo.add('baz')
assert 'baz' in foo

a = set([1, 2, 3])
b = set([3, 4, 5])
c = a.intersection(b)
import sys
assert 3 in c
assert len(c) == 1

print 'OK'
exit()
