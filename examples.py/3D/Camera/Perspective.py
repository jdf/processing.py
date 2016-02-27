"""
Perspective. 

Move the mouse left or right to change the field of view (fov).
Click to modify the aspect ratio. The perspective() function
sets a perspective projection applying foreshortening, making 
distant objects appear smaller than closer ones. The parameters 
define a viewing volume with the shape of truncated pyramid. 
Objects near to the front of the volume appears to be in their actual size, 
while farther objects appears to be smaller than original. This projection simulates 
the perspective of the world more accurately than orthographic projection. 
The version of perspective without parameters sets the default 
perspective and the version with four parameters allows the programmer 
to set the area precisely.
"""
def setup():
    size(640, 360, P3D)
    noStroke()


def draw():
    lights()
    background(204)
    cameraY = height / 2.0
    fov = mouseX / float(width) * PI / 2
    cameraZ = cameraY / max(1, tan(fov / 2.0))
    aspect = float(width) / float(height)
    if mousePressed:
        aspect = aspect / 2.0

    perspective(fov, aspect, cameraZ / 10.0, cameraZ * 10.0)
    translate(width / 2 + 30, height / 2, 0)
    rotateX(-PI / 6)
    rotateY(PI / 3 + mouseY / float(height) * PI)
    box(45)
    translate(0, 0, -50)
    box(30)
