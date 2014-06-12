"""
/**
* ControlP5 Textfield
*
*
* find a list of public methods available for the Textfield Controller
* at the bottom of this sketch.
*
* by Andreas Schlegel, 2012
* www.sojamo.de/libraries/controlp5
*
*/
"""
add_library('controlP5')


class TextListener(ControlListener):

    def controlEvent(self, e):
        print '%s -> %s' % (e.getName(), e.getStringValue())


def setup():
    size(700, 400)
    font = createFont("sansserif", 20)
    global cp5
    cp5 = ControlP5(this)

    cp5.addTextfield("input").setPosition(20, 100).setSize(
        200, 40).setFont(font).setFocus(True).setColor(color(255, 0, 0))

    cp5.addTextfield("textValue").setPosition(20, 170).setSize(
        200, 40).setFont(createFont("arial", 20)).setAutoClear(False)

    cp5.addBang("clear").setPosition(240, 170).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)

    cp5.addTextfield("default").setPosition(20, 350).setAutoClear(False)

    textFont(font)

	# You can use a lambda as a callback...
    cp5.getController("input").addListener(
        lambda e: println('%s -> %s' % (e.getName(), e.getStringValue())))
    # Or you can use a class that implements the ControlP5 callback interface...
    cp5.getController("textValue").addListener(TextListener())
    cp5.getController("default").addListener(TextListener())
    # Or you can use a function.
    def listenToClear(e):
        if e.getAction() == ControlP5.ACTION_RELEASED:
            clear()        
    cp5.addCallback(listenToClear)


def draw():
    background(0)
    fill(255)
    text(cp5.get(Textfield, "input").getText(), 360, 130)
    text(cp5.get(Textfield, "textValue").getText(), 360, 180)


def clear():
    cp5.get(Textfield, "textValue").clear()
