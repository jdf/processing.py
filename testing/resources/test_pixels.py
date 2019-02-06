size(100, 100)
noStroke()

fill('#0000FF')
rect(10, 10, 10, 10)
assert get(15, 15) == 0xFF0000FF

square(10, 30, 10)
assert get(15, 35) == 0xFF0000FF

fill(255)
rect(20, 10, 10, 10)
assert get(25, 15) == 0xFFFFFFFF

fill(0xFF00FF00)
rect(30, 10, 10, 10)
assert get(35, 15) == 0xFF00FF00

fill(lerpColor(0, 255, .5))
rect(40, 10, 10, 10)
assert get(45, 15) == 0xFF808080

fill(lerpColor('#0000FF', '#FF0000', .5))
rect(50, 10, 10, 10)
assert get(55, 15) == 0xFF800080

# Fill a pink square the hard way.
loadPixels()
assert pixels[15 * width + 15] == 0xFF0000FF
for x in range(60, 70):
    for y in range(10, 20):
        pixels[y * width + x] = 0xFFDD00DD
updatePixels()
assert get(65, 15) == 0xFFDD00DD

# Fill a yellow square the almost as hard way.
for x in range(70, 80):
    for y in range(10, 20):
        set(x, y, '#EEEE00')
assert get(75, 15) == 0xFFEEEE00

print 'OK'
exit()
