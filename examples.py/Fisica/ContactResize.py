"""
 *    ContactRemove
 *
 *    by Ricard Marxer
 *
 *    This example shows how to use the contact events in order to remove bodies.
 """
import fisica.*
FWorld world
def setup(): 
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setGravity(0, 100)
    world.setEdges()
def draw(): 
    background(255)
    if frameCount % 50 == 0:
        sz = random(30, 60)
        FCircle b = FCircle(sz)
        b.setPosition(random(0+30, width-30), 50)
        b.setVelocity(0, 100)
        b.setRestitution(0.7)
        b.setDamping(0.01)
        b.setNoStroke()
        b.setFill(200, 30, 90)
        world.add(b)
    
    world.draw()
    world.step()
def contactEnded(FContact c):     
    if !c.getBody1().isStatic():
        FCircle b = (FCircle)c.getBody1()
        if b.getSize()>5:
            b.setSize(b.getSize()*0.9)
        
     
    if !c.getBody2().isStatic():
        FCircle b = (FCircle)c.getBody2()
        if b.getSize()>5:
            b.setSize(b.getSize()*0.9)
        
    
def keyPressed(): 
    try 
        saveFrame("screenshot.png")
     
    catch (Exception e) 
    
