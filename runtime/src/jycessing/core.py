from processing.core import PApplet
from processing.core import PConstants
from processing.core import PFont
from processing.core import PGraphics
from processing.core import PGraphics2D
from processing.core import PGraphics3D
from processing.core import PGraphicsJava2D
from processing.core import PImage
from processing.core import PLine
from processing.core import PMatrix
from processing.core import PMatrix2D
from processing.core import PMatrix3D
from processing.core import PPolygon
from processing.core import PShape
from processing.core import PShapeSVG
from processing.core import PSmoothTriangle
from processing.core import PStyle
from processing.core import PTriangle
from processing.core import PVector as RealPVector

# Thanks, Guido!
# http://mail.python.org/pipermail/python-dev/2008-January/076194.html
def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class PVector(object):
    @classmethod
    def __new__(cls, *args):
        return RealPVector(*args[1:])

    @classmethod
    def add(cls, a, b, dest=None):
        return RealPVector.add(a, b, dest)

    @classmethod
    def sub(cls, a, b, dest=None):
        return RealPVector.sub(a, b, dest)

    @classmethod
    def mult(cls, a, b, dest=None):
        return RealPVector.mult(a, b, dest)

    @classmethod
    def div(cls, a, b, dest=None):
        return RealPVector.div(a, b, dest)

    @classmethod
    def cross(cls, a, b, dest=None):
        return RealPVector.cross(a, b, dest)

    @classmethod
    def dist(cls, a, b):
        return RealPVector.dist(a, b)

    @classmethod
    def dot(cls, a, b):
        return RealPVector.dot(a, b)

    @classmethod
    def angleBetween(cls, a, b):
        return RealPVector.angleBetween(a, b)

# Because PVector isn't serializable, we have to add __deepcopy__
@monkeypatch_method(RealPVector)
def __deepcopy__(self, memo):
    return PVector(self.x, self.y, self.z)

@monkeypatch_method(RealPVector)
def __sub__(a, b):
    return PVector(a.x - b.x, a.y - b.y, a.z - b.z)

@monkeypatch_method(RealPVector)
def __add__(a, b):
    return PVector(a.x + b.x, a.y + b.y, a.z + b.z)

@monkeypatch_method(RealPVector)
def __mul__(a, b):
    if isinstance(b, RealPVector):
        return PVector(a.x + b.x, a.y + b.y, a.z + b.z)
    return PVector(a.x * b, a.y * b, a.z * b)
