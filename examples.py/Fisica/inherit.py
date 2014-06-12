from fisica import Fisica, FWorld, FBox

class Texto(FBox):
    def __init__(self, _texto):
        FBox.__init__(self, textWidth(_texto), textAscent() + textDescent())
        self.texto = _texto
        self.textOffset = textAscent() - self.getHeight()/2

    def draw(self, applet):
        FBox.draw(self, applet)
        self.preDraw(applet)
        fill(0)
        stroke(0)
        textAlign(CENTER)
        text(self.texto, 0, self.textOffset)
        self.postDraw(applet)

msg = ''
world = None

def setup():
    global world

    size(400, 400)
    smooth()
    Fisica.init(this)
    font = loadFont("FreeMonoBold-24.vlw")
    textFont(font, 24)
    world = FWorld()
    world.setEdges(this, color(120))
    world.remove(world.top)
    world.setGravity(0, 500)
    t = Texto("Type and ENTER")
    t.setPosition(width/2, height/2)
    t.setRotation(random(-1, 1))
    t.setFill(255)
    t.setNoStroke()
    t.setRestitution(0.75)
    world.add(t)

def draw():
    background(120)
    world.step()
    world.draw()

def keyPressed():
    global msg
    if key == ENTER:
        if msg:
            t = Texto(msg)
            t.setPosition(width/2, height/2)
            t.setRotation(random(-1, 1))
            t.setFill(255)
            t.setNoStroke()
            t.setRestitution(0.65)
            world.add(t)
            msg = ''
    elif key == CODED and keyCode == CONTROL:
        saveFrame("screenshot.png")
    else:
        msg += key
