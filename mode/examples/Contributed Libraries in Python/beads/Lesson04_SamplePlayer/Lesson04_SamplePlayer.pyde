add_library('beads')

ac = AudioContext()


def setup():
    size(600, 100)
    selectInput("Select an audio file:", "fileSelected")


def fileSelected(selection):
    """
    Here's how to play back a sample.

    The first line gives you a way to choose the audio file.
    The (commented, optional) second line allows you to stream the audio rather than loading it all at once.
    The third line creates a sample player and loads in the Sample.
    SampleManager is a utility which keeps track of loaded audio
    files according to their file names, so you don't have to load them again.
    """
    if not selection:
        exit()
    audioFileName = selection.getAbsolutePath()
    sample = SampleManager.sample(audioFileName)
    player = SamplePlayer(ac, sample)
    # And as before...
    g = Gain(ac, 2, 0.4)
    g.addInput(player)
    ac.out.addInput(g)
    ac.start()
    """
    Note there is a lot more you can do. e.g., Varispeed. Try adding...
        speedControl = Envelope(ac, 1)
        player.setRate(speedControl)
        speedControl.addSegment(1, 1000)    # wait a second
        speedControl.addSegment(-0.5, 3000) # now rewind
    """

# Here's the code to draw a waveform.
# The code draws the current buffer of audio across the
# width of the window. To find out what a buffer of audio
# is, read on.

# Start with some spunky colors.
fore = color(255, 102, 204)
back = color(0, 0, 0)


def draw():
    noStroke()
    background(back)
    # scan across the pixels
    for i in range(width):
        # for each pixel work out where in the current audio buffer we are
        buffIndex = i * ac.getBufferSize() / width
        # then work out the pixel height of the audio data at that point
        vOffset = int((1 + 5 * ac.out.getValue(0, buffIndex)) * height / 2)
        vOffset = min(vOffset, height)
        fill(fore)
        ellipse(i, vOffset, 3, 3)


def stop():
    ac.stop()

