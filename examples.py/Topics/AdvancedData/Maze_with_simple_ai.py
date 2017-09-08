"""
RANDOM EXIT SEEKER

character wanders randomly to find exit
illustration of 2D array and maze

Author : Abdur-Rahmaan Janhangeer
"""
SIZE = 100
ROWS = 4
COLS = 4

wall = 0
ground = 1
player = 2

N = 0 #North - up
S = 1 #South - down
E = 2 #East  - to the right
W = 3 #West  - to the left

posX = 1 # in areaMap
posY = 1

areaMap = [[0,0,0,0], # rendering is done according to this map
           [0,1,2,0],
           [0,1,1,0],
           [0,0,1,0]]

def setup():  
    size(500, 500)
    frameRate(15)

def draw():
    global SIZE, ROWS, COLS, wall, ground, player, posX, posY, areaMap
    background(50)
    
    # rendering part based on map - can be wrapped in a function
    for col in range(COLS):
        for row in range(ROWS):
            tile = areaMap[col][row]
            if (tile == wall):
                fill(255)
                rect(row*SIZE, col*SIZE, SIZE, SIZE)
            elif (tile == ground):
                fill(100)
                rect(row*SIZE, col*SIZE, SIZE, SIZE)
            elif (tile == player):
                fill(255,0,0)
                rect(row*SIZE, col*SIZE, SIZE, SIZE)
                
    # map changed
    move = int(random(4)) 
    if (move == N):
        # checks if out of map and if wall is in front
        if (posY-1 >= 0 and areaMap[posY-1][posX] != wall):
            areaMap[posY][posX] = ground #draw ground where player is
            posY -= 1
            areaMap[posY][posX] = player #one tile up draw player
    elif (move == S):
        if (posY+1 < ROWS and areaMap[posY+1][posX] != wall):
            areaMap[posY][posX] = ground
            posY += 1
            areaMap[posY][posX] = player
    elif (move == E):     #to the right
        if (posX+1 < COLS and areaMap[posY][posX+1] != wall):
            areaMap[posY][posX] = ground
            posX += 1
            areaMap[posY][posX] = player
    elif (move == W):    #to the left
        if (posX-1 >= 0 and areaMap[posY][posX-1] != wall):
            areaMap[posY][posX] = ground
            posX -= 1
            areaMap[posY][posX] = player
            
    if(posX==2 and posY ==3): 
        fill(0,255,0)
        text("EXIT REACHED",50,450)
       
            
    
