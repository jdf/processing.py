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
from processing.core import PVector
from processing.core import PVector

def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

@monkeypatch_method(PVector)
def __deepcopy__(self, memo):
    return PVector(self.x, self.y, self.z)