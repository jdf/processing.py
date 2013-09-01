# processing.py #

Write real [Processing](http://processing.org/) sketches in Python.

  * Based on [Processing 2.0](http://processing.org/), and compatible with most [3rd party libraries](http://www.processing.org/reference/libraries/).
  * Source compatible with [Python 2.7.3](http://python.org).

Tested on Mac OS 10.8.3, Windows XP, Windows 7, and Ubuntu 12.10.

## Quick Start ##

### Download Processing.py 0202 ###

- [Mac OS X (83M)](http://py.processing.org/processing.py-0202-macosx.tgz)
- [Windows x64 (74M)](http://py.processing.org/processing.py-0202-windows64.zip)
- [Windows x32 (72M)](http://py.processing.org/processing.py-0202-windows32.zip)
- [Linux x64 (68M)](http://py.processing.org/processing.py-0202-linux64.tgz)
- [Linux x32 (69M)](http://py.processing.org/processing.py-0202-linux32.tgz)

Then, paste this code into a file, e.g., `mysketch.py`.

	def setup():
	    size(600, 400)

	def draw():
	    ellipse(mouseX, mouseY, 10, 10)

Drag and drop your sketch onto one of these files, according to your platform:

<img src="http://py.processing.org/howtolaunch.jpg"/>

You can also run the sketch from the command line, either with the included launcher script:

    $ ./processing-py.sh path/to/mysketch.py

or using your own Java runtime environment:

	$ java -jar processing-py.jar path/to/mysketch.py

## Documentation ##

To learn Processing.py check out these resources:

  * Built-in [Processing 2.0 functions](http://processing.org/reference/) for rendering and interaction.
  * The [Python 2.7 documentation](http://docs.python.org/2/index.html).
  * And of course the [Java 7 API documentation](http://docs.oracle.com/javase/7/docs/api/).

Processing.py comes with many [examples](https://github.com/jdf/processing.py/tree/master/examples.py), most of which are exactly like the
example sketches that come with Processing, but converted to Python.

    $ processing-py.sh examples.py/Basics/Math/noisefield.py
    $ processing-py.sh examples.py/Library/OpenGL/SpaceJunk.py
    $ processing-py.sh examples.py/3D/Typography/KineticType.py
    $ processing-py.sh examples.py/3D/Textures/TextureCube.py

## Using Processing Libraries ##

Processing.py is implemented in Java, and is designed to be compatible with the existing ecosystem of [Processing libraries](http://processing.org/reference/libraries/).

* Put processing extension libraries in the `libraries` subdirectory of your processing.py installation. Processing.py will search every jar file and directory beneath that special directory, so you don't need to be too fussy about where things go. Just unzip Processing libraries right there.

* Import the library in one of the usual Python ways, as in these snippets:

        from peasy import PeasyCam
        # or
        import peasy.PeasyCam
        # or
        import peasy.PeasyCam as PeasyCam

    Unfortunately, `from foo import *` is not supported.

* Then, in your `setup()` method:

        cam = PeasyCam(this, 200)

  Many libraries need a reference to "the current PApplet", and that's what
  `this` is for. Of course, there's no such thing as `this` in Python; it's just something that processing.py provides for you for compatibility with such libraries.

## Included Libraries ##

Some Processing libraries may not work with processing.py right out of the box. In particular, any library that uses Java reflection to call specially-named functions in your sketch will not work. However, we're happy to modify processing.py to work with any of the official Processing libraries. Here are the libraries that have required special handling in processing.py, and are included in the processing.py download:

  * [Fisica](http://www.ricardmarxer.com/fisica/), by [Ricard Marxer](http://www.ricardmarxer.com/). Included under the terms of the LGPLv3, and with the kind cooperation of Mr. Marxer. See [examples.py/Fisica](https://github.com/jdf/processing.py/tree/master/examples.py/Fisica) for examples.

If you find that some Processing library doesn't work as expected with processing.py, please let us know in the [bug tracker](http://github.com/jdf/processing.py/issues).

## FAQ ##

  * __How do I report bugs or request new features?__

    Please report any issue in the [bug tracker](http://github.com/jdf/processing.py/issues).

  * __How can I create a launcher for my sketch?__

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

  * __Why was this project created?__

    I ([Jonathan](http://MrFeinberg.com/)) recently gave a talk about Processing to a group of rather bright 8th-graders,
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

