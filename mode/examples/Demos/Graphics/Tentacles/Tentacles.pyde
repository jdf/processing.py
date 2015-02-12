'''A sketch inspired by (a radical misinterpretation of) the math from the
JS1K segment of Steven Wittens' "Making Things With Maths" video. Really,
everything is mine except the math in `segment.py`. See also
http://acko.net/blog/js1k-demo-the-making-of

Implemented in Processing.py/Processing 2.1 by Ben Alkov 11-16 Sept 2014.
Updates for Processing.py 0405/Processing 3.0a by Ben Alkov 12 Feb 2015.
'''
from tentacle import Tentacle


time = 0
Tick = 1 / 100.0  # Guarantee floating point.
SphereRadius = 200
Colors = [[color(169, 202, 240),  # blues
           color(160, 191, 227),
           color(142, 170, 202),
           color(115, 137, 163),
           color(70, 84, 99)],
          [color(206, 151, 96),  # reds
           color(207, 105, 43),
           color(193, 87, 37),
           color(124, 40, 12),
           color(120, 41, 13)],
          [color(115, 146, 34),  # greens
           color(104, 135, 23),
           color(92, 109, 29),
           color(78, 93, 22),
           color(63, 76, 16)]]
Tentacles = [Tentacle(i * -100, Colors[i % 3])
             for i in range(6)]

def setup():
    size(512, 512, OPENGL)
    rectMode(RADIUS)
    ellipseMode(RADIUS)
    strokeWeight(2)


def draw():
    global time
    rightHanded()
    fade()
    time += Tick
    for t in Tentacles:
        t.update(time, Tick, SphereRadius)


def rightHanded():
    # Fix flippin' coordinate system.
    # Not the *same* as right-handed, but good enough.
    # `-z` comes out of the screen.
    rotateX(TAU / 2)  # `Y` up.
    translate(256, -256, 0)  # Centered.


def fade():
    # Encapsulate alpha blend for trails.
    with pushMatrix():
        fill(0, 10)
        noStroke()
        translate(0, 0, SphereRadius)
        rect(0, 0, width, height)
