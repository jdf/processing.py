# processing.py #

Write Processing sketches in Python.

  * Based on [Processing 2.0](http://processing.org/), runtime compatible with most [3rd party libraries](http://www.processing.org/reference/libraries/).
  * Source compatible with [Python 2.7.3](http://python.org).

Tested on Mac OS 10.8.3, Windows XP and Ubuntu 12.10.

## Quick Start ##

### Download Processing.py 0200 ###

- [Mac OS X (83M)](http://py.processing.org/processing.py-0200-macosx.tgz)
- [Windows x64 (74M)](http://py.processing.org/processing.py-0200-windows64.zip)
- [Windows x32 (72M)](http://py.processing.org/processing.py-0200-windows32.zip)
- [Linux x64 (68M)](http://py.processing.org/processing.py-0200-linux64.tgz)
- [Linux x32 (69M)](http://py.processing.org/processing.py-0200-linux32.tgz)

Then, paste this code into a file, e.g., `mysketch.py`.

	def setup():
	    size(600, 400)

	def draw():
	    ellipse(mouseX, mouseY, 10, 10)


Eventually, you can run the code by drag-dropping your sketch onto one of these files according to your platform:

<img src="http://py.processing.org/howtolaunch.jpg"/>

If that does not work for one of your platforms (such as Linux), you can run the sketch either semi-manually (with automated JRE detection) ...

    $ ./processing-py.sh mysketch.py

... or fully by hand.

	$ java -jar processing-py.jar mysketch.py



## Documentation ##

To learn Processing.py check out these resources:


  * Built-in [Processing 2.0 functions](http://processing.org/reference/) for rendering and interaction.
  * The [Python 2.7.3 library](http://docs.python.org/2/index.html).
  * And of course the [Java 6.x / 7.x library](http://docs.oracle.com/javase/6/docs/api/).

In addition, we are a great fan of learning by doing, and a number of converted examples outline how to use Processing.py:

    $ processing-py.sh examples.py/Basics/Math/noisefield.py
    $ processing-py.sh examples.py/Library/OpenGL/SpaceJunk.py
    $ processing-py.sh examples.py/3D/Typography/KineticType.py
    $ processing-py.sh examples.py/3D/Textures/TextureCube.py

As always, on Windows use `processing-py.bat` instead, on Mac the `processing-py` app, or simply drag-drop the example on the launcher / batch.

## FAQ ##

  * __Can I use all of the existing Processing libraries?__


  Yes! Processing.py is implemented in Java, and is meant to be compatible with the whole existing ecosystem of [Processing libraries](http://processing.org/reference/libraries/).

    * Put processing extension libraries in the `libraries` subdirectory of your processing.py installation.

    * Import them in on of the usual Python ways, as in these snippets:


            from peasy import PeasyCam # or
            import peasy.PeasyCam      # or
            import peasy.PeasyCam as PeasyCam

        Unfortunately, `from foo import *` is not supported.

    * In your `setup()` method

            cam = PeasyCam(this, 200)


        Use `this` to refer to the PApplet you're in, as in the examples above.
        Many libraries need a reference to "the current PApplet", and that's what
        `this` is for.


  * __How can I create a wrapper?__

    Add these lines near the top of your script:

        import launcher
        launcher.create()

  * __How should I load data?__

    [Tentative] Along with the launcher, consider using `pwd()` for file paths. For a given argument it resolves the path for an object relative to the currently running script:

        data = load(pwd("data.txt"))

    In that case, processing.py will try to search `data.txt` always where your script resides.


  * __How can I use Ani, or any other library that modifies fields?__

    Some libraries such as [Ani](http://www.looksgood.de/libraries/Ani/) require you to specify a variable name for animation. Unfortunately they cannot access Python variables directly (and Java's built in classes are immutable).

    To solve this problem we instead create a mutable `PrimitiveFloat` object. This object has a field `.value`, which you can use for these purposes.

        import jycessing.primitives.PrimitiveFloat as Float
        x = Float(100.0)
        Ani.to(x, 200, "value", 50);  # "value" is the name of the Float's internal field


    In case you need other primitive values, please [let us know](http://github.com/jdf/processing.py/issues)!

  * __I found a bug, what should I do?__

    Please report any issue in the [bug tracker](http://github.com/jdf/processing.py/issues).


  * __Why was this project created?__


    I (Jonathan) recently gave a talk about Processing to a group of rather bright 8th-graders,
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


## Credits ##

Written by [Jonathan Feinberg](http://mrfeinberg.com) &lt;[jdf@pobox.com](mailto:jdf@pobox.com)&gt;
Launcher & many improvements by [Ralf Biedert](http://xr.io) &lt;[rb@xr.io](mailto:rb@xr.io)&gt;

Also, [YourKit, LLC](http://www.yourkit.com) was so kind to sponsor a license for their excellent [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp). Thank you very much!

