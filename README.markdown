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
    
Processing is a graphics library utilized by artists, educators, students, and hobbyists to create sketches without the hassle of traditional graphics libraries. Processing provides a simplified API that allows for visual tasks that would take dozens of lines in other software to be completed in just a couple of lines. Processing is also a community with extensive support in developing, maintaining, as well as creating educational resources for this software. Please see https://processing.org/ for more information.
    
</details><details>

<summary>Should I use Processing?</summary>
<br/>
    
Processing is the perfect enviornment for programmers of all experience levels. It is a great starting point for programmers with no graphics programming experience. The [documentation](https://processing.org/environment/#overview) is a great place to start and learn the basics. Processing is also a vehicle for learning how to code, since you can see the changes you make in your code visually. [Here](http://learningprocessing.com/videos/) is a great video tutorial for getting started. For users with graphics programming experience, Processing is very effective for fun projects and quick prototypes. For extremely complex, performance heavy, and commerical applications - Processing may not be the best choice.
    
</details><details>

<summary>Structure of a Processing Project</summary>
<br/>
    
 ```python
def setup():
    # This code is only run once
    size(800, 800)

def draw():
    # This code is run on a loop
    background(255, 0, 0)
```
    
A graphics library has three essential components: before the main loop; the code the consists of the main loop; and code that is executed after the main loop. In processing we write all of the code that will be executed before the main loop in a function that we define as `setup`. This function is only called once at the start of program execution. Typically we will define the size of the graphics window we want to generate using the called `size(w, h)`, where w is the width we desire (in pixels) and h is the height we desire (in pixels). If we want the window to take up the entire screen we can call `fullScreen()`.
    
We write the code that we want to continously execute in the function defined as `draw`. This code is run on a loop and is only terminated if we tell it to (or the program exits in an error). Typically we will define a background using a call to the `bacground()` function. This function accepts a wide variety of values from [RGB](https://en.wikipedia.org/wiki/RGB_color_model), [RGBA](https://en.wikipedia.org/wiki/RGBA_color_model), [HSB](https://en.wikipedia.org/wiki/HSL_and_HSV), and [HEX](https://en.wikipedia.org/wiki/Web_colors#Hex_triplet). By placing `background` in draw the screen is 'refreshed' each execution, which mean what we drew to the screen last cycle is erased. We can also move `background` to setup if we wish to not have this behavior.
    
</details><details>

<summary>Drawing Shapes</summary>
<br/>
    
 ```python
def setup():
    # This code is only run once
    size(800, 800)

def draw():
    # This code is run on a loop
    background(255, 0, 0)
    fill(0, 0, 0)
    rectMode(CENTER)
    rect(width / 2, height / 2, 10, 20)
```

 One of the most basic things we can do in Processing is draw shapes. There are a [wide variety of shapes](https://processing.org/reference/#shape) that we can draw, but for this example we will be drawing a rectangle. Processing uses a [Caretsian Coordinate System](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) where the origin (0,0) is in the top left corner, and the maximal (x,y) is in the bottom right corner. The function `rect(x,y,w,h)` allows us to draw a rectangle. The first and second parameters, x and y, defines the coordinates where we want to draw the rectangle. Processing also provides a variety of defined constants; `width` and `height` are the width and height of the current window. By setting `rectMode(CENTER)` and passing `width / 2` and `height / 2` as the arguments for x and y we draw a rectangle in the center of the window.
    
The function `fill(r,g,b)` allows us to change the color of the rectangle we are drawing. Think of `fill` as changing the color of the paint brush you are using. Once you call `fill` every call after will use that color until `fill` is called again. This is why we call fill before drawing our rectangle. We pass the value `(0,0,0)` to 'fill` to set the color to black.
    
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
