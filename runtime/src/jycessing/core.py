# We expose many Processing-related names as builtins, so that no imports
# are necessary, even in auxilliary modules.
import __builtin__
import os.path

from numbers import Number

# Bring all of the core Processing classes by name into the builtin namespace.
from processing.core import PApplet
__builtin__.PApplet = PApplet

from processing.core import PConstants
__builtin__.PConstants = PConstants

from processing.core import PFont
__builtin__.PFont = PFont

from processing.core import PGraphics
__builtin__.PGraphics = PGraphics

from processing.core import PImage
__builtin__.PImage = PImage

from processing.core import PMatrix
__builtin__.PMatrix = PMatrix

from processing.core import PMatrix2D
__builtin__.PMatrix2D = PMatrix2D

from processing.core import PMatrix3D
__builtin__.PMatrix3D = PMatrix3D

from processing.core import PShape
__builtin__.PShape = PShape

from processing.core import PShapeOBJ
__builtin__.PShapeOBJ = PShapeOBJ

from processing.core import PShapeSVG
__builtin__.PShapeSVG = PShapeSVG

from processing.core import PStyle
__builtin__.PStyle = PStyle

from processing.core import PSurface
__builtin__.PSurface = PSurface 

# PVector requires special handling, because it exposes the same method names
# as static methods and instance methods.
from processing.core import PVector as __pvector__
class PVector(__pvector__):
    def __instance_add__(self, *args):
        if len(args) == 1:
            v = args[0]
            self.x += v.x
            self.y += v.y
            self.z += v.z
        else:
            self.x += args[0]
            self.y += args[1]
            self.z += args[2]
        return self
        
    def __instance_sub__(self, *args):
        if len(args) == 1:
            v = args[0]
            self.x -= v.x
            self.y -= v.y
            self.z -= v.z
        else:
            self.x -= args[0]
            self.y -= args[1]
            self.z -= args[2]
        return self

    def __instance_mult__(self, o):
        return PVector.mult(self, o, self)

    def __instance_div__(self, f):
        return PVector.div(self, f, self)

    def __instance_cross__(self, o):
        return PVector.cross(self, o, self)

    def __instance_dist__(self, o):
        return PVector.dist(self, o)

    def __instance_dot__(self, *args):
        if len(args) == 1:
            v = args[0]
            return self.x * v.x + self.y * v.y + self.z * v.z
        return self.x * args[0] + self.y * args[1] + self.z * args[2]

    def __instance_lerp__(self, *args):
        if len(args) == 4:
            x = args[0]
            y = args[1]
            z = args[2]
            t = args[3]
        elif len(args) == 2:
            v = args[0]
            x = v.x
            y = v.y
            z = v.z
            t = args[1]
        else:
            raise Exception('lerp takes either (x, y, z, t) or (v, t)')
        __pvector__.lerp(self, x, y, z, t)
        return self

    def __init__(self, x=0, y=0, z=0):
        __pvector__.__init__(self, x, y, z)
        self.add = self.__instance_add__
        self.sub = self.__instance_sub__
        self.mult = self.__instance_mult__
        self.div = self.__instance_div__
        self.cross = self.__instance_cross__
        self.dist = self.__instance_dist__
        self.dot = self.__instance_dot__
        self.lerp = self.__instance_lerp__

    def get(self):
        return PVector(self.x, self.y, self.z)

    def copy(self):
        return PVector(self.x, self.y, self.z)

    def __copy__(self):
        return PVector(self.x, self.y, self.z)

    def __deepcopy__(self, memo):
        return PVector(self.x, self.y, self.z)

    @classmethod
    def add(cls, a, b, dest=None):
        if dest is None:
            return PVector(a.x + b.x, a.y + b.y, a.z + b.z)
        dest.set(a.x + b.x, a.y + b.y, a.z + b.z)
        return dest
    
    @classmethod
    def sub(cls, a, b, dest=None):
        if dest is None:
            return PVector(a.x - b.x, a.y - b.y, a.z - b.z)
        dest.set(a.x - b.x, a.y - b.y, a.z - b.z)
        return dest

    @classmethod
    def mult(cls, a, b, dest=None):
        if dest is None:
            return PVector(a.x * b, a.y * b, a.z * b)
        dest.set(a.x * b, a.y * b, a.z * b)
        return dest

    @classmethod
    def div(cls, a, b, dest=None):
        if dest is None:
            return PVector(a.x / b, a.y / b, a.z / b)
        dest.set(a.x / b, a.y / b, a.z / b)
        return dest

    @classmethod
    def dist(cls, a, b):
        return __pvector__.dist(a, b)

    @classmethod
    def dot(cls, a, b):
        return __pvector__.dot(a, b)

    @classmethod
    def lerp(cls, a, b, f):
        v = a.copy()
        v.lerp(b, f)
        return v

    @classmethod
    def cross(cls, a, b, dest=None):
        x = a.y * b.z - b.y * a.z
        y = a.z * b.x - b.z * a.x
        z = a.x * b.y - b.x * a.y
        if dest is None:
            return PVector(x, y, z)
        dest.set(x, y, z)
        return dest

    def __add__(a, b):
        return PVector.add(a, b, None)

    def __sub__(a, b):
        return PVector.sub(a, b, None)
    
    def __isub__(a, b):
        a.sub(b)
        return a
    
    def __iadd__(a, b):
        a.add(b)
        return a
    
    def __mul__(a, b):
        if not isinstance(b, Number):
            raise TypeError("The * operator can only be used to multiply a PVector by a number")
        return PVector.mult(a, float(b), None)
    
    def __rmul__(a, b):
        if not isinstance(b, Number):
            raise TypeError("The * operator can only be used to multiply a PVector by a number")
        return PVector.mult(a, float(b), None)
    
    def __imul__(a, b):
        if not isinstance(b, Number):
            raise TypeError("The *= operator can only be used to multiply a PVector by a number")
        a.mult(float(b))
        return a
    
    def __div__(a, b):
        if not isinstance(b, Number):
            raise TypeError("The / operator can only be used to divide a PVector by a number")
        return PVector.div(a, float(b), None)
    
    def __idiv__(a, b):
        if not isinstance(b, Number):
            raise TypeError("The /= operator can only be used to divide a PVector by a number")
        a.div(float(b))
        return a
    
    def __eq__(a, b):
        return a.x == b.x and a.y == b.y and a.z == b.z
    
    def __lt__(a, b):
        return a.magSq() < b.magSq()
    
    def __le__(a, b):
        return a.magSq() <= b.magSq()
    
    def __gt__(a, b):
        return a.magSq() > b.magSq()
    
    def __ge__(a, b):
        return a.magSq() >= b.magSq()

# Now expose the funky PVector class as a builtin.
__builtin__.PVector = PVector

# Make the PApplet available to sketches by the name "this", to better match
# existing Java-based documentation for third-party libraries, and such.
__builtin__.this = __papplet__


# Expose all of the builtin Processing methods. Credit is due to
# https://github.com/kazimuth/python-mode-processing for the
# technique of exploiting Jython's bound methods, which is tidy
# and simple.

# We handle filter() by hand to permit both P5's filter() and Python's filter().
# __builtin__.filter = __papplet__.filter

# Processing's "random" function works as documented, but is blown
# away if the user does a python 'import random'. This seems
# reasonable to me.
__builtin__.random = __papplet__.random

# Because of two 5-arg text() methods, we have to do this in Java.
# __builtin__.text = __papplet__.text

for f in """
ambient ambientLight applyMatrix arc beginCamera beginContour beginPGL
beginRaw beginRecord beginShape bezier bezierDetail bezierPoint bezierTangent
bezierVertex blendMode box camera clear clip color colorMode createFont
createImage createInput createOutput createReader createShape curve curveDetail
curvePoint curveTangent curveTightness curveVertex delay directionalLight
displayDensity ellipse ellipseMode emissive endCamera endContour endPGL endRaw
endRecord endShape exit fill frameRate frustum fullScreen hint imageMode launch
lightFalloff lightSpecular lights line link loadBytes loadFont loadImage
loadJSONArray loadJSONObject loadPixels loadShader loadShape loadTable loadXML
loop millis modelX modelY modelZ noClip noCursor noFill noLights noLoop
noSmooth noStroke noTint noise noiseDetail noiseSeed normal ortho parseXML
perspective pixelDensity point pointLight popMatrix popStyle printArray printCamera
printMatrix printProjection quad quadraticVertex randomGaussian randomSeed
rect rectMode redraw requestImage resetMatrix resetShader rotate
rotateX rotateY rotateZ save saveBytes saveFrame saveJSONArray saveJSONObject
saveStream saveTable saveXML scale screenX screenY screenZ selectFolder
selectInput selectOutput shader shape shapeMode shearX shearY shininess
size sketchPath smooth specular sphere sphereDetail spotLight stroke strokeCap
strokeJoin strokeWeight textAlign textAscent textDescent textFont textLeading
textMode textSize textWidth textureMode textureWrap thread tint translate
triangle updatePixels vertex
""".split():
    assert getattr(__papplet__, f)
    setattr(__builtin__, f, getattr(__papplet__, f))

'''
In order to get colors to behave reasonably, they have to be cast to positive
long quantities on their way into Python, and 32-bit signed quantities on
their way into Java.
'''
# We have to provide a funky get() because of int/long conversion woes.
__builtin__.get = __papplet__.get

# We handle lerpColor by hand because there's an instance method and a static method.
# __builtin__.lerpColor = __papplet__.lerpColor


# These must all be implemented in Java to support our funky color arguments.
'''
__builtin__.alpha = __papplet__.alpha
__builtin__.red = __papplet__.red
__builtin__.green = __papplet__.green
__builtin__.blue = __papplet__.blue
__builtin__.hue = __papplet__.hue
__builtin__.saturation = __papplet__.saturation
__builtin__.brightness = __papplet__.brightness
'''

# And these are PApplet static methods. Some are commented out to indicate
# that we prefer or require Jython's implementation.
#__builtin__.abs = PApplet.abs
# __builtin__.exec = PApplet.exec
# We permit both Python and P5's map()s.
# __builtin__.map = PApplet.map
# __builtin__.max = PApplet.max
# __builtin__.min = PApplet.min
# __builtin__.print = PApplet.print
# __builtin__.println = PApplet.println
# __builtin__.round = PApplet.round

__builtin__.constrain = lambda x, a, b: max(min(x, b), a)

for f in """
acos append arrayCopy asin atan atan2 binary blendColor ceil
concat cos createInput createOutput createReader day debug degrees dist
exp expand floor hex hour join lerp  loadBytes log mag match matchAll
minute month nf nfc nfp nfs norm pow radians reverse saveBytes saveStream
saveStrings second shorten sin sort splice split splitTokens sq sqrt
subset tan trim unbinary unhex year
""".split():
    assert getattr(PApplet, f)
    setattr(__builtin__, f, getattr(PApplet, f))


# Here are some names that resolve to static *and* instance methods.
# Dispatch them to the appropriate methods based on the type of their
# arguments.
def __createInput__(o):
    if isinstance(o, basestring):
        return __papplet__.createInput(o)
    return PApplet.createInput(o)
__builtin__.createInput = __createInput__

def __createOutput__(o):
    if isinstance(o, basestring):
        return __papplet__.createOutput(o)
    return PApplet.createOutput(o)
__builtin__.createOutput = __createOutput__

def __createReader__(o):
    if isinstance(o, basestring):
        return __papplet__.createReader(o)
    return PApplet.createReader(o)
__builtin__.createReader = __createReader__

def __createWriter__(o):
    if isinstance(o, basestring):
        return __papplet__.createWriter(o)
    return PApplet.createWriter(o)
__builtin__.createWriter = __createWriter__

def __loadStrings__(o):
    if isinstance(o, basestring):
        return __papplet__.loadStrings(o)
    return PApplet.loadStrings(o)
__builtin__.loadStrings = __loadStrings__

def __loadBytes__(o):
    if isinstance(o, basestring):
        return __papplet__.loadBytes(o)
    return PApplet.loadBytes(o)
__builtin__.loadBytes = __loadBytes__

def __loadJSONArray__(o):
    if isinstance(o, basestring):
        return __papplet__.loadJSONArray(o)
    return PApplet.loadJSONArray(o)
__builtin__.loadJSONArray = __loadJSONArray__

def __loadJSONObject__(o):
    if isinstance(o, basestring):
        return __papplet__.loadJSONObject(o)
    return PApplet.loadJSONObject(o)
__builtin__.loadJSONObject = __loadJSONObject__

def __saveStream__(target, source):
    if isinstance(source, basestring) or isinstance(target, basestring):
        return __papplet__.saveStream(target, source)
    return PApplet.saveStream(target, source)
__builtin__.saveStream = __saveStream__

def __saveStrings__(where, data):
    if isinstance(where, basestring):
        return __papplet__.saveStrings(where, data)
    return PApplet.saveStrings(where, data)
__builtin__.saveStrings = __saveStrings__

def __saveBytes__(where, data):
    if isinstance(where, basestring):
        return __papplet__.saveBytes(where, data)
    return PApplet.saveBytes(where, data)
__builtin__.saveBytes = __saveBytes__

# Make "open" able to find files in the "data" folder, and also other folders if the sketch is in a temp directory
__realopen__ = open
def __open__(filename, *args, **kwargs):
    if os.path.isfile(filename):
        return __realopen__(filename, *args, **kwargs)
    if not os.path.isabs(filename):
        datafilename = __papplet__.dataPath(filename)
        if os.path.isfile(datafilename):
            return __realopen__(datafilename, *args, **kwargs)
        sketchfilename = __papplet__.sketchPath(filename)
	if os.path.isfile(sketchfilename):
		return __realopen__(sketchfilename, *args, **kwargs)
    # Fail naturally
    return __realopen__(filename, *args, **kwargs)
__builtin__.open = __open__

# Due to a seeming bug in Jython, the print builtin ignores the the setting of
# interp.setOut and interp.setErr.

class FakeStdOut():
    def write(self, s):
        __stdout__.print(s)
    def flush(self):
        __stdout__.flush()
sys.stdout = FakeStdOut()

class FakeStdErr():
    def write(self, s):
        __stderr__.print(s)
    def flush(self):
        __stderr__.flush()
sys.stderr = FakeStdErr()

del FakeStdOut, FakeStdErr

def __println__(o):
    print o
__builtin__.println = __println__


class PGraphicsPythonModeWrapper(object):
    class popper(object):
        def __init__(self, enter_func, exit_func, *args):
            self.exit_func = exit_func
            self.as_result = enter_func(*args)
        def __enter__(self):
            return self.as_result
        def __exit__(self, *args):
            self.exit_func()
            
    def __init__(self, g):
        self.__dict__['g'] = g
    
    def _get_wrapped_image_(self):
        return self.__dict__['g']
    
    def beginDraw(self):
        return PGraphicsPythonModeWrapper.popper(
            self.g.beginDraw, self.g.endDraw)
    
    def pushMatrix(self):
        return PGraphicsPythonModeWrapper.popper(
            self.g.pushMatrix, self.g.popMatrix)

    def beginShape(self, *args):
        return PGraphicsPythonModeWrapper.popper(
            self.g.beginShape, self.g.endShape, *args)

    def beginRaw(self, *args):
        return PGraphicsPythonModeWrapper.popper(
            self.g.beginRaw, self.g.endRaw, *args)

    def __getattr__(self, attr):
        return getattr(self.g, attr)
    
    def __setattr__(self, attr, value):
        return setattr(self.g, attr, value)  

def FakeCreateGraphics(*args):
    return PGraphicsPythonModeWrapper(__papplet__.createGraphics(*args))

__builtin__.createGraphics = FakeCreateGraphics
del FakeCreateGraphics

# Functions that expect a PImage will choke on our wrapper that delegates to
# an actual PImage. Here, we sniff out the first argument to such functions,
# and swap in the wrapped object as necessary.
def UnwrapImage(func):
    def f(*args):
        if len(args):
            first, rest = args[0], args[1:]
            if hasattr(first, '_get_wrapped_image_'):
                func(first._get_wrapped_image_(), *rest)
            else:
                func(*args)
        else:
            func()
    return f
for f in ('image', 'background', 'mask', 'blend', 'copy', 'cursor', 'texture'):
    assert getattr(__papplet__, f)
    setattr(__builtin__, f, UnwrapImage(getattr(__papplet__, f)))
del UnwrapImage


# Implement
#
# with pushFoo():
#     doSomethingInFooContext()
# doSomethingOutOfFooContext()
#
# pushFoo()/popFoo() still works as usual.

def makePopper(pushName, popName, exposed_name=None, close_args=None):
    if not close_args:
        close_args = []
    if not exposed_name:
        exposed_name = pushName

    bound_push = getattr(__papplet__, pushName)
    bound_pop = getattr(__papplet__, popName)
    
    class Popper(object):
        def __init__(self, delegate):
            self.delegate = delegate
            
        def __enter__(self):
            # The result of pushFoo/beginFoo is made available to
            # the "as" clause of the "with" statement.
            return self.delegate
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            bound_pop(*close_args)
            return False

        # If you say
        #    foo = beginPGL()
        # foo now is a Popper object, but the user will want
        # PGL methods and properties, so we delegate those
        # attribute fetches to the actual PGL object.        
        def __getattr__(self, attr):
            return getattr(self.delegate, attr)

    def shim(*args):
        return Popper(bound_push(*args))
    
    setattr(__builtin__, exposed_name, shim)

makePopper('pushStyle', 'popStyle')
makePopper('pushMatrix', 'popMatrix')
makePopper('beginContour', 'endContour')
makePopper('beginPGL', 'endPGL')
makePopper('beginShape', 'endShape')
makePopper('beginShape', 'endShape',
           close_args=[CLOSE], exposed_name='beginClosedShape')
makePopper('beginCamera', 'endCamera')

import os
os.chdir(__cwd__)
