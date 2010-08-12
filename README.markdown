# processing.py #

Write [Processing](http://processing.org) sketches in Python.      
[Jonathan Feinberg](http://mrfeinberg.com) &lt;[jdf@pobox.com](mailto:jdf@pobox.com)&gt;
            
## How? ##

Quick start:

    $ git clone git://github.com/jdf/processing.py.git
    $ cd processing.py
    $ ant
    $ java -jar processing-py.jar examples.py/3D/Typography/KineticType/KineticType.py
    $ java -jar processing-py.jar examples.py/Library/OpenGL/SpaceJunk/SpaceJunk.py

Put processing extension libraries in the "libraries" directory any
way you like. Import them in the usual Python way, e.g.

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

## What!? ##


    """
      Wave Gradient 
      by Ira Greenberg.
      Adapted to python by Jonathan Feinberg.  
       
      Generate a gradient along a sin() wave.
    """
    
    amplitude = 30
    fillGap = 2.5
    
    def setup():
      size(200, 200)
      background(200, 200, 200)
      noLoop()
    
    def draw():
      frequency = 0
      for i in range(-75, height + 75):
        # Reset angle to 0, so waves stack properly
        angle = 0
        # Increasing frequency causes more gaps
        frequency += .006
        for j in range(width + 75):
          py = i + sin(radians(angle)) * amplitude
          angle += frequency
          c = color(abs(py - i) * 255 / amplitude,
                    255 - abs(py - i) * 255 / amplitude,
                    j * (255.0 / (width + 50)))
          # Hack to fill gaps. Raise value of fillGap if you increase frequency
          for filler in range(fillGap):
            set(int(j - filler), int(py) - filler, c)
            set(int(j), int(py), c)
            set(int(j + filler), int(py) + filler, c)

## Why? ##

I recently gave a talk about Processing to a group of rather bright 8th-graders,
as part of a computer-programming summer camp they were attending at my office.
Their curriculum up to that point had been in Python, which is an eminently
sensible choice, given the 
[pedagogical roots](http://en.wikipedia.org/wiki/ABC_(programming_language))
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

Please play with this, report bugs, and port more of the Processing
examples!
