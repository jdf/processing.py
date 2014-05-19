"""
Pixelate    
by Hernando Barragan.    

Load a QuickTime file and display the video signal 
using rectangles as pixels by reading the values stored 
in the current video frame pixels array. 
"""
import processing.video.*
numPixelsWide, numPixelsHigh
blockSize = 10
Movie mov
color movColors[]
def setup(): 
    size(640, 360)
    noStroke()
    mov = Movie(this, "transit.mov")
    mov.loop()
    numPixelsWide = width / blockSize
    numPixelsHigh = height / blockSize
    println(numPixelsWide)
    movColors = color[numPixelsWide * numPixelsHigh]
# Display values from movie
def draw(): 
    if mov.available() == True:
        mov.read()
        mov.loadPixels()
        count = 0
        for j in range(numPixelsHigh): 
            for i in range(numPixelsWide): 
                movColors[count] = mov.get(i*blockSize, j*blockSize)
                count += 1
            
        
    
    background(255)
    for j in range(numPixelsHigh): 
        for i in range(numPixelsWide): 
            fill(movColors[j*numPixelsWide + i])
            rect(i*blockSize, j*blockSize, blockSize, blockSize)
        
    
