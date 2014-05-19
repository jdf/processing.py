from collections import defaultdict
from java.awt.event import KeyEvent
from java.lang.reflect import Modifier

key_names = defaultdict(lambda: 'UNKNOWN')
for f in KeyEvent.getDeclaredFields():
    if Modifier.isStatic(f.getModifiers()):
        name = f.getName()
        if name.startswith("VK_"):
            key_names[f.getInt(None)] = name[3:]


def draw():
    pass


def keyPressed():
    if key == CODED:
        print key_names[keyCode]
    else:
        print "key " + key

