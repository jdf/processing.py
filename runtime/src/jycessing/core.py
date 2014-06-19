# We expose many Processing-related names as builtins, so that no imports
# are necessary, even in auxilliary modules.
import __builtin__

from numbers import Number

# PAppletJythonDriver is a PApplet that knows how to interpret a Python
# Processing sketch, and which delegates Processing callbacks (such as
# setup(), draw(), keyPressed(), etc.) to the appropriate Python code.
from jycessing import PAppletJythonDriver

# Bring all of the core Processing classes by name into the builtin namespace.
from processing.core import PApplet
__builtin__.PApplet = PApplet

from processing.core import PConstants
__builtin__.PConstants = PConstants

from processing.core import PFont
__builtin__.PFont = PFont

from processing.core import PGraphics
__builtin__.PGraphics = PGraphics

from processing.core import PGraphicsJava2D
__builtin__.PGraphicsJava2D = PGraphicsJava2D

from processing.core import PGraphicsRetina2D
__builtin__.PGraphicsRetina2D = PGraphicsRetina2D

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

from processing.opengl import FontTexture
__builtin__.FontTexture = FontTexture

from processing.opengl import FrameBuffer
__builtin__.FrameBuffer = FrameBuffer

from processing.opengl import LinePath
__builtin__.LinePath = LinePath

from processing.opengl import LineStroker
__builtin__.LineStroker = LineStroker

from processing.opengl import PGL
__builtin__.PGL = PGL

from processing.opengl import PGraphics2D
__builtin__.PGraphics2D = PGraphics2D

from processing.opengl import PGraphics3D
__builtin__.PGraphics3D = PGraphics3D

from processing.opengl import PGraphicsOpenGL
__builtin__.PGraphicsOpenGL = PGraphicsOpenGL

from processing.opengl import PJOGL
__builtin__.PJOGL = PJOGL

from processing.opengl import PShader
__builtin__.PShader = PShader

from processing.opengl import PShapeOpenGL
__builtin__.PShapeOpenGL = PShapeOpenGL

from processing.opengl import Texture
__builtin__.Texture = Texture


# PVector requires special handling, because it exposes the same method names
# as static methods and instance methods.
from processing.core import PVector as __pvector__
class PVector(__pvector__):
    def __instance_add__(self, o):
        PVector.add(self, o, self)
        
    def __instance_sub__(self, o):
        PVector.sub(self, o, self)

    def __instance_mult__(self, o):
        PVector.mult(self, o, self)

    def __instance_div__(self, f):
        PVector.div(self, f, self)

    def __instance_cross__(self, o):
        return PVector.cross(self, o, self)

    def __instance_dist__(self, o):
        return PVector.dist(self, o)

    def __instance_dot__(self, o):
        return PVector.dot(self, o)

    def __init__(self, x, y, z=None):
        if z is None:
            __pvector__.__init__(self, x, y)
        else:
            __pvector__.__init__(self, x, y, z)
        self.add = self.__instance_add__
        self.sub = self.__instance_sub__
        self.mult = self.__instance_mult__
        self.div = self.__instance_div__
        self.cross = self.__instance_cross__
        self.dist = self.__instance_dist__

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

# Construct the PApplet.
__papplet__ = PAppletJythonDriver(__interp__, __path__, __source__)
# Make it available to sketches by the name "this", to better match existing
# Java-based documentation for third-party libraries, and such.
__builtin__.this = __papplet__


# Expose all of the builtin Processing methods. Credit is due to
# https://github.com/kazimuth/python-mode-processing for the
# technique of exploiting Jython's bound methods, which is tidy
# and simple.
__builtin__.ambient = __papplet__.ambient
__builtin__.ambientLight = __papplet__.ambientLight
__builtin__.applyMatrix = __papplet__.applyMatrix
__builtin__.arc = __papplet__.arc
__builtin__.background = __papplet__.background
__builtin__.beginCamera = __papplet__.beginCamera
__builtin__.beginContour = __papplet__.beginContour
__builtin__.beginPGL = __papplet__.beginPGL
__builtin__.beginRaw = __papplet__.beginRaw
__builtin__.beginRecord = __papplet__.beginRecord
__builtin__.beginShape = __papplet__.beginShape
__builtin__.bezier = __papplet__.bezier
__builtin__.bezierDetail = __papplet__.bezierDetail
__builtin__.bezierPoint = __papplet__.bezierPoint
__builtin__.bezierTangent = __papplet__.bezierTangent
__builtin__.bezierVertex = __papplet__.bezierVertex
__builtin__.blend = __papplet__.blend
__builtin__.blendMode = __papplet__.blendMode
__builtin__.box = __papplet__.box
__builtin__.camera = __papplet__.camera
__builtin__.clear = __papplet__.clear
__builtin__.clip = __papplet__.clip
__builtin__.color = __papplet__.color
__builtin__.colorMode = __papplet__.colorMode
__builtin__.copy = __papplet__.copy
__builtin__.createFont = __papplet__.createFont
__builtin__.createGraphics = __papplet__.createGraphics
__builtin__.createImage = __papplet__.createImage
__builtin__.createInput = __papplet__.createInput
__builtin__.createOutput = __papplet__.createOutput
__builtin__.createReader = __papplet__.createReader
__builtin__.createShape = __papplet__.createShape
__builtin__.createWriter = __papplet__.createWriter
__builtin__.cursor = __papplet__.cursor
__builtin__.curve = __papplet__.curve
__builtin__.curveDetail = __papplet__.curveDetail
__builtin__.curvePoint = __papplet__.curvePoint
__builtin__.curveTangent = __papplet__.curveTangent
__builtin__.curveTightness = __papplet__.curveTightness
__builtin__.curveVertex = __papplet__.curveVertex
__builtin__.delay = __papplet__.delay
__builtin__.directionalLight = __papplet__.directionalLight
__builtin__.ellipse = __papplet__.ellipse
__builtin__.ellipseMode = __papplet__.ellipseMode
__builtin__.emissive = __papplet__.emissive
__builtin__.endCamera = __papplet__.endCamera
__builtin__.endContour = __papplet__.endContour
__builtin__.endPGL = __papplet__.endPGL
__builtin__.endRaw = __papplet__.endRaw
__builtin__.endRecord = __papplet__.endRecord
__builtin__.endShape = __papplet__.endShape
__builtin__.exit = __papplet__.exit
__builtin__.fill = __papplet__.fill

# We handle filter() by hand to permit both P5's filter() and Python's filter().
# __builtin__.filter = __papplet__.filter

__builtin__.frameRate = __papplet__.frameRate
__builtin__.frustum = __papplet__.frustum

__builtin__.hint = __papplet__.hint
__builtin__.image = __papplet__.image
__builtin__.imageMode = __papplet__.imageMode

__builtin__.lightFalloff = __papplet__.lightFalloff
__builtin__.lightSpecular = __papplet__.lightSpecular
__builtin__.lights = __papplet__.lights
__builtin__.line = __papplet__.line
__builtin__.link = __papplet__.link
__builtin__.loadBytes = __papplet__.loadBytes
__builtin__.loadFont = __papplet__.loadFont
__builtin__.loadImage = __papplet__.loadImage
__builtin__.loadJSONArray = __papplet__.loadJSONArray
__builtin__.loadJSONObject = __papplet__.loadJSONObject
__builtin__.loadPixels = __papplet__.loadPixels
__builtin__.loadShader = __papplet__.loadShader
__builtin__.loadShape = __papplet__.loadShape
__builtin__.loadTable = __papplet__.loadTable
__builtin__.loadXML = __papplet__.loadXML
__builtin__.loop = __papplet__.loop
__builtin__.millis = __papplet__.millis
__builtin__.modelX = __papplet__.modelX
__builtin__.modelY = __papplet__.modelY
__builtin__.modelZ = __papplet__.modelZ
__builtin__.noClip = __papplet__.noClip
__builtin__.noCursor = __papplet__.noCursor
__builtin__.noFill = __papplet__.noFill
__builtin__.noLights = __papplet__.noLights
__builtin__.noLoop = __papplet__.noLoop
__builtin__.noSmooth = __papplet__.noSmooth
__builtin__.noStroke = __papplet__.noStroke
__builtin__.noTint = __papplet__.noTint
__builtin__.noise = __papplet__.noise
__builtin__.noiseDetail = __papplet__.noiseDetail
__builtin__.noiseSeed = __papplet__.noiseSeed
__builtin__.normal = __papplet__.normal
__builtin__.ortho = __papplet__.ortho
__builtin__.parseXML = __papplet__.parseXML
__builtin__.perspective = __papplet__.perspective
__builtin__.point = __papplet__.point
__builtin__.pointLight = __papplet__.pointLight
__builtin__.popMatrix = __papplet__.popMatrix
__builtin__.popStyle = __papplet__.popStyle
__builtin__.printArray = __papplet__.printArray
__builtin__.printCamera = __papplet__.printCamera
__builtin__.printMatrix = __papplet__.printMatrix
__builtin__.printProjection = __papplet__.printProjection
__builtin__.quad = __papplet__.quad
__builtin__.quadraticVertex = __papplet__.quadraticVertex

# Processing's "random" function works as documented, but is blown
# away if the user does a python 'import random'. This seems
# reasonable to me.
__builtin__.random = __papplet__.random

__builtin__.randomGaussian = __papplet__.randomGaussian
__builtin__.randomSeed = __papplet__.randomSeed
__builtin__.rect = __papplet__.rect
__builtin__.rectMode = __papplet__.rectMode
__builtin__.redraw = __papplet__.redraw
__builtin__.requestImage = __papplet__.requestImage
__builtin__.resetMatrix = __papplet__.resetMatrix
__builtin__.resetShader = __papplet__.resetShader
__builtin__.rotate = __papplet__.rotate
__builtin__.rotateX = __papplet__.rotateX
__builtin__.rotateY = __papplet__.rotateY
__builtin__.rotateZ = __papplet__.rotateZ
__builtin__.save = __papplet__.save
__builtin__.saveBytes = __papplet__.saveBytes
__builtin__.saveFrame = __papplet__.saveFrame
__builtin__.saveJSONArray = __papplet__.saveJSONArray
__builtin__.saveJSONObject = __papplet__.saveJSONObject
__builtin__.saveStream = __papplet__.saveStream
__builtin__.saveStrings = __papplet__.saveStrings
__builtin__.saveTable = __papplet__.saveTable
__builtin__.saveXML = __papplet__.saveXML
__builtin__.scale = __papplet__.scale
__builtin__.screenX = __papplet__.screenX
__builtin__.screenY = __papplet__.screenY
__builtin__.screenZ = __papplet__.screenZ
__builtin__.selectFolder = __papplet__.selectFolder
__builtin__.selectInput = __papplet__.selectInput
__builtin__.selectOutput = __papplet__.selectOutput
__builtin__.shader = __papplet__.shader
__builtin__.shape = __papplet__.shape
__builtin__.shapeMode = __papplet__.shapeMode
__builtin__.shearX = __papplet__.shearX
__builtin__.shearY = __papplet__.shearY
__builtin__.shininess = __papplet__.shininess
__builtin__.size = __papplet__.size
__builtin__.smooth = __papplet__.smooth
__builtin__.specular = __papplet__.specular
__builtin__.sphere = __papplet__.sphere
__builtin__.sphereDetail = __papplet__.sphereDetail
__builtin__.spotLight = __papplet__.spotLight
__builtin__.stroke = __papplet__.stroke
__builtin__.strokeCap = __papplet__.strokeCap
__builtin__.strokeJoin = __papplet__.strokeJoin
__builtin__.strokeWeight = __papplet__.strokeWeight

# Because of two 5-arg text() methods, we have to do this in Java.
# __builtin__.text = __papplet__.text

__builtin__.textAlign = __papplet__.textAlign
__builtin__.textAscent = __papplet__.textAscent
__builtin__.textDescent = __papplet__.textDescent
__builtin__.textFont = __papplet__.textFont
__builtin__.textLeading = __papplet__.textLeading
__builtin__.textMode = __papplet__.textMode
__builtin__.textSize = __papplet__.textSize
__builtin__.textWidth = __papplet__.textWidth
__builtin__.texture = __papplet__.texture
__builtin__.textureMode = __papplet__.textureMode
__builtin__.textureWrap = __papplet__.textureWrap
__builtin__.tint = __papplet__.tint
__builtin__.translate = __papplet__.translate
__builtin__.triangle = __papplet__.triangle
__builtin__.updatePixels = __papplet__.updatePixels
__builtin__.vertex = __papplet__.vertex

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
__builtin__.acos = PApplet.acos
__builtin__.append = PApplet.append
__builtin__.arrayCopy = PApplet.arrayCopy
__builtin__.asin = PApplet.asin
__builtin__.atan = PApplet.atan
__builtin__.atan2 = PApplet.atan2
__builtin__.binary = PApplet.binary
__builtin__.blendColor = PApplet.blendColor
__builtin__.ceil = PApplet.ceil
__builtin__.concat = PApplet.concat
__builtin__.constrain = PApplet.constrain
__builtin__.cos = PApplet.cos
__builtin__.createInput = PApplet.createInput
__builtin__.createOutput = PApplet.createOutput
__builtin__.createReader = PApplet.createReader
__builtin__.createWriter = PApplet.createWriter
__builtin__.day = PApplet.day
__builtin__.debug = PApplet.debug
__builtin__.degrees = PApplet.degrees
__builtin__.dist = PApplet.dist
# __builtin__.exec = PApplet.exec
__builtin__.exp = PApplet.exp
__builtin__.expand = PApplet.expand
__builtin__.floor = PApplet.floor
__builtin__.hex = PApplet.hex
__builtin__.hour = PApplet.hour
__builtin__.join = PApplet.join
__builtin__.lerp = PApplet.lerp
__builtin__.loadBytes = PApplet.loadBytes
__builtin__.log = PApplet.log
__builtin__.mag = PApplet.mag
# We permit both Python and P5's map()s.
# __builtin__.map = PApplet.map
__builtin__.match = PApplet.match
__builtin__.matchAll = PApplet.matchAll
# __builtin__.max = PApplet.max
# __builtin__.min = PApplet.min
__builtin__.minute = PApplet.minute
__builtin__.month = PApplet.month
__builtin__.nf = PApplet.nf
__builtin__.nfc = PApplet.nfc
__builtin__.nfp = PApplet.nfp
__builtin__.nfs = PApplet.nfs
__builtin__.norm = PApplet.norm
__builtin__.pow = PApplet.pow
# __builtin__.print = PApplet.print
#__builtin__.println = PApplet.println
__builtin__.radians = PApplet.radians
__builtin__.reverse = PApplet.reverse
# __builtin__.round = PApplet.round
__builtin__.saveBytes = PApplet.saveBytes
__builtin__.saveStream = PApplet.saveStream
__builtin__.saveStrings = PApplet.saveStrings
__builtin__.second = PApplet.second
__builtin__.shorten = PApplet.shorten
__builtin__.sin = PApplet.sin
__builtin__.sort = PApplet.sort
__builtin__.splice = PApplet.splice
__builtin__.split = PApplet.split
__builtin__.splitTokens = PApplet.splitTokens
__builtin__.sq = PApplet.sq
__builtin__.sqrt = PApplet.sqrt
__builtin__.subset = PApplet.subset
__builtin__.tan = PApplet.tan
__builtin__.trim = PApplet.trim
__builtin__.unbinary = PApplet.unbinary
__builtin__.unhex = PApplet.unhex
__builtin__.year = PApplet.year


# Here are some names that resolve to static *and* instance methods.
# Dispatch them to the appropriate methods based on the type of their
# arguments.
def __createReader__(o):
    if isinstance(o, basestring):
        return __papplet__.createReader(o)
    return PApplet.createReader(o)
__builtin__.createReader = __createReader__

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

del PAppletJythonDriver

# Due to a seeming bug in Jython, the print builtin ignores the the setting of
# interp.setOut and interp.setErr.

class FakeStdOut():
    def write(self, s):
        __stdout__.print(s)
sys.stdout = FakeStdOut()

class FakeStdErr():
    def write(self, s):
        __stderr__.print(s)
sys.stderr = FakeStdErr()

del FakeStdOut, FakeStdErr

def __println__(o):
    sys.stdout.write(o)
    sys.stdout.write('\n')
__builtin__.println = __println__


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
