# Don't lose precision when constrain()ing.

assert 8.3 == constrain(8.3, 5, 10)
assert 5 == constrain(4.99999, 5, 10)
assert 8 == constrain(8, 5, 10)
assert 10.001 == constrain(37, 5, 10.001)

print 'OK'
exit()
