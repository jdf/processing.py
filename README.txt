processing.py
Write processing sketches in Python.
Jonathan Feinberg <jdf@pobox.com>

    $ git clone git://github.com/jdf/processing.py.git
    $ cd processing.py
    $ ant
    $ java -jar processing-py.jar examples.py/3D/Typography/KineticType/KineticType.py
    $ java -jar processing-py.jar examples.py/Library/OpenGL/SpaceJunk/SpaceJunk.py

Put processing extension libraries in "libraries" directory any way you like.
Import them in the usual Python way, e.g.

    import peasy.PeasyCam
    cam = peasy.PeasyCam(this, 200)

or

    import peasy.PeasyCam as PeasyCam
    cam = PeasyCam(this, 200)
    
or

    from peasy import PeasyCam
    cam = PeasyCam(this, 200)

Unfortunately, "from foo import *" is not supported.

Use "this" to refer to the running applet, as in the examples above.
