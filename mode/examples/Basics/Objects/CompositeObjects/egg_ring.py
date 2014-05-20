class EggRing(object): 
    Egg ovoid
    Ring circle = Ring()
    EggRing(x, y, t, sp) 
        ovoid = Egg(x, y, t, sp)
        circle.start(x, y - sp/2)
    
    def transmit(): 
        ovoid.wobble()
        ovoid.display()
        circle.grow()
        circle.display()
        if circle.on == False:
            circle.on = True
        
    
