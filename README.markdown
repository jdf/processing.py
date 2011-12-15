# processing.py #

Write [Processing](http://processing.org) sketches in Python.
[Jonathan Feinberg](http://mrfeinberg.com) &lt;[jdf@pobox.com](mailto:jdf@pobox.com)&gt;

## Found a bug? ##

See the [open bugs in the bug tracker](http://github.com/jdf/processing.py/issues).

## Quick Start ##


Download the peasycam distribution.

    $ curl -L https://github.com/downloads/jdf/processing.py/processing.py-0019.tgz | tar zx
    $ cd processing.py-0019

Then try some examples.

    $ java -jar processing-py.jar examples.py/Basics/Math/noisefield.py
    $ java -jar processing-py.jar examples.py/3D/Typography/KineticType.py
    $ java -jar processing-py.jar examples.py/Library/OpenGL/SpaceJunk.py
    $ java -jar processing-py.jar examples.py/3D/Textures/TextureCube.py
    $ cat > mysketch.py
    def draw():
        background(0)
        text(frameRate, 20, 20)
    $ java -jar processing-py.jar mysketch.py

Put processing extension libraries in the "libraries" directory.

    $ curl -O http://mrfeinberg.com/peasycam/peasycam.zip
    $ cd libraries
    $ unzip ../peasycam.zip

Import them in the usual Python way, e.g.

    import peasy.PeasyCam
    cam = peasy.PeasyCam(this, 200)

or

    import peasy.PeasyCam as PeasyCam
    cam = PeasyCam(this, 200)

or

    from peasy import PeasyCam
    cam = PeasyCam(this, 200)

Unfortunately, `from foo import *` is not supported.

Use `this` to refer to the PApplet you're in, as in the examples above.

Put any Python libraries in the "libraries" directory, or in sketch directories.
Only pure-Python libraries will work--nothing that requires "native" code.

## Example Code ##

	"""
	  noisefield.py - demonstrate Perlin noise
	  Jonathan Feinberg
	"""
	srcSize = 50
	destSize = 400
	g = createGraphics(srcSize, srcSize, JAVA2D)
	
	def setup():
	    size(destSize, destSize, OPENGL)
	
	def draw():
	    t = .0005 * millis()
	    g.beginDraw()
	    for y in range(srcSize):
	        for x in range(srcSize):
	            blue = noise(t + .1*x, t + .05*y, .2*t)
	            g.set(x, y, color(0, 0, 255 * blue))
	    g.endDraw()
	    image(g, 0, 0, destSize, destSize)

## Why? ##

I recently gave a talk about Processing to a group of rather bright 8th-graders,
as part of a computer-programming summer camp they were attending at my office.
Their curriculum up to that point had been in Python, which is an eminently
sensible choice, given the
[pedagogical roots](http://en.wikipedia.org/wiki/ABC_%28programming_language%29)
of the language.

The kids were really turned on by the demos--I showed them the
[white glove](http://whiteglovetracking.com/), and
[Golan Levin](http://flong.com/)'s
[New Year's cards](http://www.flong.com/storage/experience/newyear/newyear10/)--but
they were bogged down by Processing's C-like syntax, which really seems arcane
and unnecessarily complex when you're used to Python.

I shared my experience with Processing creators
[Ben Fry](http://benfry.com/) and [Casey Reas](http://reas.com/), and they
told me that, indeed, the original Processing was a fork of
["Design By Numbers"](http://dbn.media.mit.edu/), with Python and Scheme
support hacked in. Support for a multi-lingual programming
environment was always part of the plan, so they were enthusiastic
about any new attempt at the problem.

I was able to hack up a proof of concept in a couple of hours, and have
managed to create something worth sharing in a couple of weeks. I was only
able to do it at all thanks to the brilliant and beautiful
[Jython](http://www.jython.org/) project.

At the time of Processing's first public release, August of 2001,
Jython was too young a project to be used in this way. But now, having done
absolutely no work to profile and optimize, I can get hundreds of frames
per second of 3D graphics on my linux box. So, kudos to the Processing
project, and kudos to Jython!

Please play with this,
[report bugs](http://github.com/jdf/processing.py/issues),
and port more of the Processing examples!

## A word from a sponsor ##

YourKit has kindly granted me a license to use their excellent Java profiler.
I'm happy to give them the space to say:

> YourKit is kindly supporting open source projects with its full-featured Java Profiler.
> YourKit, LLC is the creator of innovative and intelligent tools for profiling
> Java and .NET applications. Take a look at YourKit's leading software products:
> [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp) and
> [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp).
