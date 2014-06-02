"""
Soft Body 
by Ira Greenberg.    

Softbody dynamics simulation using curveVertex() and curveTightness().
"""
 
# center point
centerX = 0, centerY = 0
radius = 45, rotAngle = -90
accelX, accelY
springing = .0009, damping = .98
#corner nodes
nodes = 5
nodeStartX[] = float[nodes]
nodeStartY[] = float[nodes]
float[]nodeX = float[nodes]
float[]nodeY = float[nodes]
float[]angle = float[nodes]
float[]frequency = float[nodes]
# soft-body dynamics
organicConstant = 1
def setup(): 
    size(640, 360)
    #center shape in window
    centerX = width/2
    centerY = height/2
    # iniitalize frequencies for corner nodes
    for i in range(nodes):
        frequency[i] = random(5, 12)
    
    noStroke()
    frameRate(30)
def draw(): 
    #fade background
    fill(0, 100)
    rect(0,0,width, height)
    drawShape()
    moveShape()
def drawShape(): 
    #    calculate node    starting locations
    for i in range(nodes):
        nodeStartX[i] = centerX+cos(radians(rotAngle))*radius
        nodeStartY[i] = centerY+sin(radians(rotAngle))*radius
        rotAngle += 360.0/nodes
    
    # draw polygon
    curveTightness(organicConstant)
    fill(255)
    beginShape()
    for i in range(nodes):
        curveVertex(nodeX[i], nodeY[i])
    
    for i in range(nodes-1):
        curveVertex(nodeX[i], nodeY[i])
    
    endShape(CLOSE)
def moveShape(): 
    #move center point
    deltaX = mouseX-centerX
    deltaY = mouseY-centerY
    # create springing effect
    deltaX *= springing
    deltaY *= springing
    accelX += deltaX
    accelY += deltaY
    # move predator's center
    centerX += accelX
    centerY += accelY
    # slow down springing
    accelX *= damping
    accelY *= damping
    # change curve tightness
    organicConstant = 1-((abs(accelX)+abs(accelY))*.1)
    #move nodes
    for i in range(nodes):
        nodeX[i] = nodeStartX[i]+sin(radians(angle[i]))*(accelX*2)
        nodeY[i] = nodeStartY[i]+sin(radians(angle[i]))*(accelY*2)
        angle[i]+=frequency[i]
    
