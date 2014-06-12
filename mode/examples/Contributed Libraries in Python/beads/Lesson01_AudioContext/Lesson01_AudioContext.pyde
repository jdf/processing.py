add_library('beads')

# Lesson 1: Make some noise! Note, if you don't know Processing, you'd
# be well advised to follow some of the Processing tutorials first.


# Make an AudioContext. This class always the starting point for 
# any Beads project. You need it to define various things to do with 
# audio processing. It also connects the the JavaSound system and
# provides you with an output device.
ac = AudioContext()

# Make a noise-making object. Noise is a type of Class known as a
# UGen. UGens have some number of audio inputs and audio outputs
# and do some kind of audio processing or generation. Notice that
# UGens always get initialised with the AudioContext.
n = Noise(ac)


# Make a gain control object. This is another UGen. This has a few
# more arguments in its constructor: the second argument gives the
# number of channels, and the third argument can be used to initialise
# the gain level.
g = Gain(ac, 1, 0.5)

# Now things get interesting. You can plug UGens into other UGens, 
# making chains of audio processing units. Here we're just going to
# plug the Noise object into the Gain object, and the Gain object
# into the main audio output (ac.out). In this case, the Noise object
# has one output, the Gain object has one input and one output, and
# the ac.out object has two inputs. The method addInput() does its
# best to work out what to do. For example, when connecting the Gain
# to the out object, the output of the Gain object gets connected to
# both channels of the output object.
g.addInput(n)
ac.out.addInput(g)


# Finally, start things running.
ac.start()

def setup():
    size(300, 300)
    
# Here's the code to draw a scatterplot waveform.
# The code draws the current buffer of audio across the
# width of the window. To find out what a buffer of audio
# is, read on.

# Start with some spunky colors.
fore = color(255, 102, 204)
back = color(0, 0, 0)


# Just do the work straight into Processing's draw() method.
def draw():
    # set the background
    background(back)

    # scan across the pixels
    for i in range(width):
        # for each pixel work out where in the current audio buffer we are
        buffIndex = i * ac.getBufferSize() / width
        # then work out the pixel height of the audio data at that point
        vOffset = (int)((1 + ac.out.getValue(0, buffIndex)) * height / 2)
        vOffset = min(vOffset, height)
        set(i, vOffset, fore)


def stop():
    ac.stop()

