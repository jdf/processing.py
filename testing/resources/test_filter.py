def settings():
    size(48, 48, P2D)

def setup():
    global img, emboss
    img = loadImage("data/python.png")
    emboss = loadShader("data/emboss.glsl")

def draw():
    global img, emboss
    # Processing builtins
    # filter(PShader)
    image(img, 0, 0)
    filter(emboss)

    # filter(kind)
    filter(BLUR)

    # filter(kind, param)
    filter(POSTERIZE, 4)

    # Python builtin
    a = filter(lambda x: x == 'banana',
               ['apple', 'grape', 'banana', 'banana'])
    assert a == ['banana', 'banana']

    print 'OK'

    exit()
