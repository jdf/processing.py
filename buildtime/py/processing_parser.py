import re

from processing.core import PApplet
from java.lang.reflect import Field, Method, Modifier
from java.lang import Class

BAD_METHOD = re.compile(r'''
    ^(
    init|handleDraw|draw|parse[A-Z].*|arraycopy|openStream|str|.*Pressed
    |.*Released|(un)?register[A-Z].*|print(ln)?|setup[A-Z].+|thread
    |(get|set|remove)Cache|max|update|destroy|main|flush|addListeners|dataFile
    |die|setup|mouseE(ntered|xited)|paint|sketch[A-Z].*|stop|save(File|Path)
    |displayable|method|runSketch|start|focus(Lost|Gained)
    )$
    ''', re.X)

BAD_FIELD = re.compile(r'''
    ^(
        screen|args|recorder|frame|g|selectedFile|keyEvent|mouseEvent
        |sketchPath|screen(Width|Height)|defaultSize|firstMouse|finished
        |requestImageMax
    )$
    ''', re.X)

ALL_APPLET_METHODS = set((m.getName() 
                          for m in Class.getDeclaredMethods(PApplet)
                          if Modifier.isPublic(m.getModifiers())))

PYTHON_BUILTINS = set(("map", "filter", "set", "str"))

