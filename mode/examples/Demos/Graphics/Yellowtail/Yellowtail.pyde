"""
 * Yellowtail
 * by Golan Levin (www.flong.com).
 * Translated to Python by Jonathan Feinberg.
 *
 * Click, drag, and release to create a kinetic gesture.
 *
 * Yellowtail (1998-2000) is an interactive software system for the gestural
 * creation and performance of real-time abstract animation. Yellowtail repeats
 * a user's strokes end-over-end, enabling simultaneous specification of a
 * line's shape and quality of movement. Each line repeats according to its
 * own period, producing an ever-changing and responsive display of lively,
 * worm-like textures.
 """

from gesture import Gesture

nGestures = 36    # Number of gestures
minMove = 3       # Minimum travel for a point
gestureArray = []


def setup():
    global gestureArray, currentGestureID
    size(1024, 768, P2D)
    background(0, 0, 0)
    noStroke()
    for _ in range(nGestures):
        gestureArray.append(Gesture(width, height))
    currentGestureID = -1
    clearGestures()


def draw():
    background(0)
    updateGeometry()
    fill(255, 255, 245)
    for gesture in gestureArray:
        renderGesture(gesture, width, height)


def mousePressed():
    global currentGestureID
    currentGestureID = (currentGestureID + 1) % nGestures
    gesture = gestureArray[currentGestureID]
    gesture.clear()
    gesture.clearPolys()
    gesture.addPoint(mouseX, mouseY)


def mouseDragged():
    if currentGestureID >= 0:
        gesture = gestureArray[currentGestureID]
        if gesture.distToLast(mouseX, mouseY) > minMove:
            gesture.addPoint(mouseX, mouseY)
            gesture.smooth()
            gesture.compile()


def keyPressed():
    if key in ('+', '='):
        if currentGestureID >= 0:
            th = gestureArray[currentGestureID].thickness
            gestureArray[currentGestureID].thickness = min(96, th + 1)
            gestureArray[currentGestureID].compile()
    elif key == '-':
        if currentGestureID >= 0:
            th = gestureArray[currentGestureID].thickness
            gestureArray[currentGestureID].thickness = max(2, th - 1)
            gestureArray[currentGestureID].compile()
    elif key == ' ':
        clearGestures()


def renderGesture(gesture, w, h):
    if not gesture.exists:
        return
    if gesture.nPolys <= 0:
        return
    with beginShape(QUADS):
        for i, p in enumerate(gesture.polygons):
            xpts = p.xpoints
            ypts = p.ypoints
            vertex(xpts[0], ypts[0])
            vertex(xpts[1], ypts[1])
            vertex(xpts[2], ypts[2])
            vertex(xpts[3], ypts[3])
            cr = gesture.crosses[i]
            if cr > 0:
                if (cr & 3) > 0:
                    vertex(xpts[0] + w, ypts[0])
                    vertex(xpts[1] + w, ypts[1])
                    vertex(xpts[2] + w, ypts[2])
                    vertex(xpts[3] + w, ypts[3])
                    vertex(xpts[0] - w, ypts[0])
                    vertex(xpts[1] - w, ypts[1])
                    vertex(xpts[2] - w, ypts[2])
                    vertex(xpts[3] - w, ypts[3])
                if (cr & 12) > 0:
                    vertex(xpts[0], ypts[0] + h)
                    vertex(xpts[1], ypts[1] + h)
                    vertex(xpts[2], ypts[2] + h)
                    vertex(xpts[3], ypts[3] + h)
                    vertex(xpts[0], ypts[0] - h)
                    vertex(xpts[1], ypts[1] - h)
                    vertex(xpts[2], ypts[2] - h)
                    vertex(xpts[3], ypts[3] - h)
                # I have knowingly retained the small flaw of not
                # completely dealing with the corner conditions
                # (the case in which both of the above are True).


def updateGeometry():
    for i in range(nGestures):
        gesture = gestureArray[i]
        if not gesture.exists:
            continue
        if (i != currentGestureID or not mousePressed):
            advanceGesture(gesture)


def advanceGesture(gesture):
    # Move a Gesture one step
    if (not gesture.exists) or (gesture.nPoints < 1):
        return
    jx = gesture.jumpDx
    jy = gesture.jumpDy
    path = gesture.path
    for i in range(gesture.nPoints - 1, 0, -1):
        path[i].x = path[i - 1].x
        path[i].y = path[i - 1].y
    path[0].x = path[gesture.nPoints - 1].x - jx
    path[0].y = path[gesture.nPoints - 1].y - jy
    gesture.compile()


def clearGestures():
    for g in gestureArray:
        g.clear()

