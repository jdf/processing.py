# Make sure that the result of color() is an unsigned long, and
# compatible with pixels[] and get().

background(0)
loadPixels()
assert get(50, 50) == color(0,0,0)
assert pixels[50 * 100 + 50] == get(50, 50)
assert 0xFF000000 == color(0, 0, 0)

a = color(255, 128, 0)
assert hex(a) == 'FFFF8000'
assert alpha(a) == 255.0
assert red(a) == 255.0
assert green(a) == 128.0
assert blue(a) == 0

print 'OK'
exit()
