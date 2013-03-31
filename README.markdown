# processing.py #

Write [Processing](http://processing.org) sketches in Python. 

  * Supports [Processing 2.0 functions](http://processing.org/reference/) as well as its third party libraries.
  * The [Python 2.7.3 library](http://docs.python.org/2/library/).
  * And of course the [Java 6.x / 7.x library](http://docs.oracle.com/javase/6/docs/api/).


## Quick Start ##

To take off immediately download and unzip the [processing.py distribution](http://xr.io/d/processing.py.zip).


Then, paste this code into a file, e.g., __mysketch.py__.

	def setup():
	    size(600, 400, P3D)
	
	def draw():	   
	    ellipse(mouseX, mouseY, 10, 10)


Eventually, you can run the code by executing:

    $ java -jar processing-py.jar mysketch.py


## Documentation ##

See the official [Processing Reference](http://processing.org/reference/) for core drawing / interaction functions. For a more advanced example, see the code below:



	import jycessing.primitives.PrimitiveFloat as PF
	import launcher

	# Create a launcher (for options see below)
	launcher.create(bundle=['*.txt'])

	# Read some data 
	datafile = pwd('data.txt')
	data = open(datafile, 'r').readlines()

	# Create a primitive float
	pf = PF(10.0)

	def setup():	
		size(640, 480, P3D)	
		frame.setTitle("Test Application");
		
	def draw():
		background(0)
		ellipse(mouseX, mouseY, pf.value, pf.value)



<br/>
In this example there are a few things to note. First, you can create a launcher for your application by performing 

	import launcher
	launcher.create()


Supported arguments to the call are:

  * __name__: The final name of the application, defaults to _'Launcher'_.
  * __bundle__: Set of string-patterns to bundle with your application, defaults to _[]_.
  * __platforms__: Create launchers for these platforms, defaults to _['mac', 'win']_. 
  * __outdir__: Where to create the output, defaults to _'dist.platforms'_. 
  * __ignorelibs__: Plugin libraries to ignore, defaults to _['*video*']_.


<br/>
Along with the launcher the function __pwd()__ was introduced. For a given argument it resolves the path for an object relative to the currently running script. Very useful when loading bundled resourced in a wrapped / launched application.  

<br/>
The Java class __jycessing.primitives.PrimitiveFloat__ was added as a convenience class for mutable float objects (exposes the field __value__). Comes in handy when using libraries such as [Ani](http://www.looksgood.de/libraries/Ani/), who want to modify Java fields directly.


## Credits ##

Written by [Jonathan Feinberg](http://mrfeinberg.com) &lt;[jdf@pobox.com](mailto:jdf@pobox.com)&gt;   
Launcher & adjustments [Ralf Biedert](http://xr.io) &lt;[rb@xr.io](mailto:rb@xr.io)&gt;  

This is a slightly enhanced clone from [Jonathan's repository](https://github.com/jdf/processing.py). Differences between this and the upstream version (as of 2013/03/31):
  * Uses jython 2.7 (instead of 2.5)
  * Supports fullscreen mode
  * Creates launchers for Windows and Mac
  * Better support for frameworks such as [Ani](http://www.looksgood.de/libraries/Ani/)
  

