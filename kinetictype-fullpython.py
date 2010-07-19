from processing.core import PApplet

class KineticType(PApplet):
    """
     Kinetic Type 
     by Zach Lieberman. 
     Adapted to Python by Jonathan Feinberg
     Using push() and pop() to define the curves of the lines of type. 
    """
    
    def __init__(self):
        self.words = [
                      "sometimes it's like", "the lines of text", "are so happy", 
                      "that they want to dance", "or leave the page or jump",
                      "can you blame them?", "living on the page like that",
                      "waiting to be read..."
                      ]
   
    def setup(self):
        self.size(640, 360, PApplet.P3D)
        self.textFont(self.loadFont("Univers-66.vlw"), 1.0)
        self.fill(255)
    
    def draw(self):
        self.background(0)
        self.translate(-200, -50, -450)
        self.rotateY(0.3)
        
        # Now animate every line object & draw it...
        for i in range(len(self.words)):
            f1 = self.sin((i + 1.0) * (self.millis() / 10000.0) * self.TWO_PI)
            f2 = self.sin((8.0 - i) * (self.millis() / 10000.0) * self.TWO_PI)
            line = self.words[i]
            self.pushMatrix()
            self.translate(0.0, i*75, 0.0)
            for j in range(len(line)):
                if j != 0:
                    self.translate(self.textWidth(line[j - 1]) * 75, 0.0, 0.0)
                self.rotateY(f1 * 0.005 * f2)
                self.pushMatrix()
                self.scale(75.0)
                self.text(line[j], 0.0, 0.0)
                self.popMatrix()
            self.popMatrix()

KineticType().runSketch()
try:
    print banana
except:
    print "no bananas"