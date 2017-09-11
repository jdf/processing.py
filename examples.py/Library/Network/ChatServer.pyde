"""
Chat Server by Tom Igoe. 

Press the mouse to stop the server.
"""

add_library('net')  # import processing.net.*

port = 10002
myServerRunning = True
bgColor = 0
direction = 1
textLine = 60

def setup():
    global myServer
    size(400, 400)
    textFont(createFont("SanSerif", 16))
    myServer = Server(this, port)  # Starts a myServer on port 10002
    background(0)

def mousePressed():
    global myServerRunning
    # If the mouse clicked the myServer stops
    myServer.stop()
    myServerRunning = False

def draw():
    if myServerRunning:
        text("server", 15, 45)
        thisClient = myServer.available()
        if thisClient:  # not None
            if thisClient.available():  # thisClient.available() > 0
                text("mesage from: " + thisClient.ip() + " : " +
                     thisClient.readString(), 15, textLine)
                textLine = textLine + 35
    else:
        text("server", 15, 45)
        text("stopped", 15, 65)
