# Processing builtin
# set(x, y, c)
set(10, 10, color(0, 0, 128))

print get(10,10) & 0x00FFFFFF

# Python builtin
s = set()
s.add('banana')
print s
#expect 13