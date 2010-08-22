import urllib2
# Processing builtin
# map(value, low1, high1, low2, high2)
print int(map(5, 0, 10, 0, 100))
#expect 50

# Python builtin
print map(lambda x: x + 1, (12, 16, 22))[0]
#expect 13