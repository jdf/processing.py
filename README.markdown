# Python Mode for Processing #

Write real [Processing](http://processing.org/) sketches in Python.

* Based on [Processing 3.0](http://processing.org/), and compatible with most [3rd party libraries](http://www.processing.org/reference/libraries/).
* Source compatible with [Python 2.7.3](http://python.org).

Tested on Mac OS 10.10 and Ubuntu 14.

[![Build Status](https://travis-ci.org/jdf/processing.py.svg?branch=master)](https://travis-ci.org/jdf/processing.py)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjdf%2Fprocessing.py.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjdf%2Fprocessing.py?ref=badge_shield)

## Quick Start ##

<details>

<summary>Processing Development Environment</summary>
<br/>
If you're looking to write Processing sketches in Python, your best bet is to use
Python Mode. The project is still in its early days, and documentation is lacking,
but there are many example sketches to get you started. In general, the Processing
reference works just fine for Python mode.

First, [download Processing](http://processing.org/download). Then, install
Python Mode:

<img src="http://py.processing.org/add_mode.png"/>
<img src="http://py.processing.org/install.png"/>

Then try your first sketch:

```python
def setup():
    size(600, 600)
    colorMode(HSB)
    noStroke()

def draw():
    fill(0x11000000)
    rect(0, 0, width, height)
    fill(frameCount % 255, 255, 255)
    ellipse(mouseX, mouseY, 20, 20)
```

If you are just getting started, it is a good idea to go through the [tutorials on our website](http://py.processing.org/tutorials/), and alternatively some [examples](mode/examples).
    
</details>

## Processing Basics ##

<details>

<summary>What is Processing?</summary>
<br/>

    
</details><details>

<summary>Should I use Processing?</summary>
<br/>

    
</details><details>

<summary>Structure of a Processing Project</summary>
<br/>
    
</details><details>

<summary>Drawing Shapes</summary>
<br/>

    
</details><details>
    
<summary>User Input</summary>
<br/>

    
</details><details>

<summary>Next Steps</summary>
<br/>

    
</details>

## Advanced Usage ##

<details>
    
<summary>Using Processing Libraries</summary>
<br/>

Python Mode is implemented in Java, and is designed to be compatible with the existing ecosystem of [Processing libraries](http://processing.org/reference/libraries/).

Many libraries need a reference to "the current PApplet", and that's what
`this` is for. Of course, there's no such thing as `this` in Python; it's just something that processing.py provides for you for compatibility with such libraries.

If you find that some Processing library doesn't work as expected with processing.py, please let us know in the [bug tracker](http://github.com/jdf/processing.py/issues).
    
</details><details>

<summary>How do I report bugs or request new features?</summary>
<br/>

Please report any issue in the [bug tracker](http://github.com/jdf/processing.py/issues).

### How can I create a launcher for my sketch? ###

Add these lines near the top of your script:

```python
import launcher
launcher.create()
```

</details><details>
    
<summary>How can I use Ani, or any other library that modifies fields?</summary>
<br/>

Some libraries such as [Ani](http://www.looksgood.de/libraries/Ani/) require you to specify a variable name for animation. Unfortunately they cannot access Python variables directly (and Java's built in classes are immutable).

To solve this problem we instead create a mutable `PrimitiveFloat` object. This object has a field `.value`, which you can use for these purposes.

```python
import jycessing.primitives.PrimitiveFloat as Float
x = Float(100.0)
Ani.to(x, 200, "value", 50);  # "value" is the name of the Float's internal field
```

In case you need other primitive values, please [let us know](http://github.com/jdf/processing.py/issues)!

</details>

## Why was this project created? ##

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

Much of the work in achieving compatibility with Processing 3.x was
was done by Luca Damasco
(Google Summer of Code student), under the supervision of Golan Levin,
with additional support from the Frank-Ratchye STUDIO for Creative Inquiry at Carnegie
Mellon University. Without Luca, the porject may well have died.

Also, [YourKit, LLC](http://www.yourkit.com) was so kind to sponsor a license for their excellent [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp). Thank you very much! They've asked me to place this message here in return for their sponsorship:

<img src="https://www.yourkit.com/images/yklogo.png"/>
YourKit supports open source projects with its full-featured Java Profiler.
YourKit, LLC is the creator of <a href="https://www.yourkit.com/java/profiler/">YourKit Java Profiler</a>
and <a href="https://www.yourkit.com/.net/profiler/">YourKit .NET Profiler</a>,
innovative and intelligent tools for profiling Java and .NET applications.

## License ##

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjdf%2Fprocessing.py.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjdf%2Fprocessing.py?ref=badge_large)
