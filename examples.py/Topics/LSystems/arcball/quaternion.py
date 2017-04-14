from math import acos, sqrt
from processing.core import PConstants

class Quaternion(object):
    """
    Helper class, originally written for use by ArcBall class
    """
 
    def __init__(self, w = 1.0,  x = 0,  y = 0,  z = 0):   
        """
        Important to initialize default with unit matrix
        """
        self.w, self.x, self.y, self.z = w,  x,  y,  z
    
    def reset(self):
        """
        Reset quaternion to unit matrix
        """
        self.w = 1.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
    def set(self,  w, v):
        """
        Set quaternion given w float and PVector
        """
        self.w = w
        self.x = v.x
        self.y = v.y
        self.z = v.z
        
    def copy(self,  q):
        """
        Copy quaternion q
        """
        self.w = q.w
        self.x = q.x
        self.y = q.y
        self.z = q.z  
        
    @classmethod  
    def mult(clas, q1, q2): 
        """
        class method returns a new instance of Quaternion as a product of 
        two input Quaternions
        """        
        x = q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y
        y = q1.w * q2.y + q1.y * q2.w + q1.z * q2.x - q1.x * q2.z
        z = q1.w * q2.z + q1.z * q2.w + q1.x * q2.y - q1.y * q2.x
        w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
        product = Quaternion(w,  x,  y,  z)
        return product
        
    def getValue(self):
        """
        Using processing epsilon
        """
        sa = sqrt(1.0 - self.w * self.w)
  
        if (sa < PConstants.EPSILON):
            sa = 1.0
        return [acos(self.w) * 2, self.x / sa, self.y / sa, self.z / sa]
 

