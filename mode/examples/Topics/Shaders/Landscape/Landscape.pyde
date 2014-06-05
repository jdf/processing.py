"""
Elevated
https://www.shadertoy.com/view/MdX3Rr by inigo quilez
Created by inigo quilez - iq/2013
License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
Processing port by Raphaël de Courville.
"""

elevatedshader = None


def setup():
    size(640, 360, P2D)
    noStroke()
    # The code of this shader shows how to integrate shaders from shadertoy
    # into Processing with minimal changes.
    elevatedshader = loadShader("landscape.glsl")
    elevatedshader.set("resolution", float(width), float(height))


def draw():
    background(0)
    elevatedshader.set("time", (float)(millis() / 1000.0))
    shader(elevatedshader)
    rect(0, 0, width, height)
    frame.setTitle("frame: " + str(frameCount) + " - fps: " + str(frameRate))

