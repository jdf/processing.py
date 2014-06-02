"""
Springs. 

Move the mouse over one of the circles and click to re-position. 
When you release the mouse, it will snap back into position. 
Each circle has a slightly different behavior.    
"""
 
num = 3
Spring[] springs = Spring[num]
def setup():
    size(640, 360)
    noStroke()
    springs[0] = Spring(240, 260,    40, 0.98, 8.0, 0.1, springs, 0)
    springs[1] = Spring(320, 210, 120, 0.95, 9.0, 0.1, springs, 1)
    springs[2] = Spring(180, 170, 200, 0.90, 9.9, 0.1, springs, 2)
def draw(): 
    background(51)
    
    for i in range(num): 
        springs[i].update()
        springs[i].display()
    
def mousePressed(): 
    for i in range(num): 
        springs[i].pressed()
    
def mouseReleased(): 
    for i in range(num): 
        springs[i].released()
    
class Spring(object): 
    # Screen values 
    xpos, ypos
    tempxpos, tempypos
    size = 20
    boolean over = False
    boolean move = False
    # Spring simulation constants 
    mass# Mass 
    k = 0.2# Spring constant 
    damp# Damping 
    rest_posx# Rest position X 
    rest_posy# Rest position Y 
    # Spring simulation variables 
    #pos = 20.0# Position 
    velx = 0.0# X Velocity 
    vely = 0.0# Y Velocity 
    accel = 0# Acceleration 
    force = 0# Force 
    Spring[] friends
    me
    
    # Constructor
    Spring(x, y, s, d, m, 
                 k_in, Spring[] others, id) 
    
        xpos = tempxpos = x
        ypos = tempypos = y
        rest_posx = x
        rest_posy = y
        size = s
        damp = d
        mass = m
        k = k_in
        friends = others
        me = id
    
    def update(): 
    
        if move:
            rest_posy = mouseY
            rest_posx = mouseX
        
        force = -k * (tempypos - rest_posy)# f=-ky 
        accel = force / mass# Set the acceleration, f=ma == a=f/m 
        vely = damp * (vely + accel)# Set the velocity 
        tempypos = tempypos + vely# Updated position 
        force = -k * (tempxpos - rest_posx)# f=-ky 
        accel = force / mass# Set the acceleration, f=ma == a=f/m 
        velx = damp * (velx + accel)# Set the velocity 
        tempxpos = tempxpos + velx# Updated position 
        
        if (overEvent() or move) and !otherOver() :
            over = True
        else:
            over = False
        
    
    
    # Test to see if mouse is over this spring
    boolean overEvent() 
        disX = tempxpos - mouseX
        disY = tempypos - mouseY
        if sqrt(sq(disX) + sq(disY)) < size/2 :
            return True
        else:
            return False
        
    
    
    # Make sure no other springs are active
    boolean otherOver() 
        for i in range(num): 
            if i != me:
                if friends[i].over == True:
                    return True
                
            
        
        return False
    
    def display(): 
    
        if over:
            fill(153)
        else:
            fill(255)
        
        ellipse(tempxpos, tempypos, size, size)
    
    def pressed(): 
    
        if over:
            move = True
        else:
            move = False
        
    
    def released(): 
    
        move = False
        rest_posx = xpos
        rest_posy = ypos
    
