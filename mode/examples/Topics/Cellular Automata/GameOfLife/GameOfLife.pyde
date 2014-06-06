"""
A Processing implementation of Game of Life.
By Joan Soler-Adillon

Press SPACE BAR to pause and change the cell's values with the mouse.
On pause, click to activate/deactivate cells.
Press R to randomly reset the cells' grid.
Press C to clear the cells' grid.

The original Game of Life was created by John Conway in 1970.
"""

# Size of cells
cellSize = 5
# How likely for a cell to be alive at start (in percentage).
probabilityOfAliveAtStart = 15
# Variables for timer.
interval = 100
lastRecordedTime = 0
# Colors for active/inactive cells.
alive = color(0, 200, 0)
dead = color(0)
# Array of cells.
cells = []
# Buffer to record the state of the cells and use this while changing the
# others in the interations.
cellsBuffer = []
# Pause
paused = False


def setup():
    size(640, 360)
    # You might be tempted to create a 2D list like this:
    # cells = [[0] * (height / cellSize)] * (width / cellSize)
    # This won't work! It just creates aliases to one unique row.
    # Create a 2D list with a for loop:
    for row in range(width / cellSize):
        cells += [[0] * (height / cellSize)]
        cellsBuffer += [[0] * (height / cellSize)]
    # This stroke will draw the background grid.
    stroke(48)
    noSmooth()
    # Initialization of cells.
    for x in range(width / cellSize):
        for y in range(height / cellSize):
            state = random(100)
            state = 1 - int(state > probabilityOfAliveAtStart)
            cells[x][y] = int(state)  # Save state of each cell.
    background(0)  # Fill in black in case cells don't cover all the windows.


def draw():
    # Draw grid.
    for x in range(width / cellSize):
        for y in range(height / cellSize):
            if cells[x][y] == 1:
                fill(alive)  # If alive
            else:
                fill(dead)  # If dead
            rect(x * cellSize, y * cellSize, cellSize, cellSize)
    # Iterate if timer ticks.
    if millis() - lastRecordedTime > interval:
        if not paused:
            iteration()
            lastRecordedTime = millis()
    # Create cells manually on pause.
    if paused and mousePressed:
        # Map and avoid out of bound errors.
        xCellOver = int(map(mouseX, 0, width, 0, width / cellSize))
        xCellOver = constrain(xCellOver, 0, width / cellSize - 1)
        yCellOver = int(map(mouseY, 0, height, 0, height / cellSize))
        yCellOver = constrain(yCellOver, 0, height / cellSize - 1)
        # Change state of cell. 
        cells[xCellOver][yCellOver] = 1- int(cellsBuffer[xCellOver][yCellOver])
        # Fill cell with appropriate color. 
        if cellsBuffer[xCellOver][yCellOver] == 1:  
            fill(alive)  # Fill with alive color.
        else:  
            fill(dead)  # Fill with dead color.
    # And then save to buffer once mouse goes up.
    elif paused and not mousePressed:
        # Save cells to buffer (so we opeate with one list keeping the other
        # intact).
        for x in range(width / cellSize):
            for y in range(height / cellSize):
                cellsBuffer[x][y] = cells[x][y]


def iteration():  # When the clock ticks
    # Save cells to buffer (so we opeate with one list keeping the other
    # intact).
    for x in range(width / cellSize):
        for y in range(height / cellSize):
            cellsBuffer[x][y] = cells[x][y]
    # Visit each cell:
    for x in range(width / cellSize):
        for y in range(height / cellSize):
            # And visit all the neighbours of each cell.
            neighbours = 0  # We'll count the neighbours.
            for xx in range(x - 1, x + 2, 1):
                for yy in range(y - 1, y + 2, 1):
                    # Make sure you are not out of bounds.
                    if (xx >= 0 and xx < width / cellSize) and (yy >= 0 and yy < height / cellSize):
                        # Make sure to to check against self.
                        if not (xx == x and yy == y):
                            if cellsBuffer[xx][yy] == 1:
                                # Check alive neighbours and count them.
                                neighbours += 1
                        # End of if
                    # End of if
                # End of yy loop
            # End of xx loop
            # We've checked the neigbours: apply rules!
            # The cell is alive: kill it if necessary.
            if cellsBuffer[x][y] == 1:
                if neighbours < 2 or neighbours > 3:
                    cells[x][y] = 0  # Die unless it has 2 or 3 neighbours.
            # The cell is dead: make it live if necessary.
            elif neighbours == 3:
                cells[x][y] = 1  # Only if it has 3 neighbours.
            # End of if
        # End of y loop
    # End of x loop
# End of function


def keyPressed():
    if key == 'r' or key == 'R':
        # Restart: reinitialization of cells.
        for x in range(width / cellSize):
            for y in range(height / cellSize):
                cells[x][y] = 0 if random(100) > probabilityOfAliveAtStart else 1
    if key == ' ':  # On/off of pause.
        paused = not paused
    if key == 'c' or key == 'C':  # Clear all.
        for x in range(width / cellSize):
            for y in range(height / cellSize):
                cells[x][y] = 0  # Save all to zero.

