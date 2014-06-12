"""
Datatype Conversion. 

It is sometimes beneficial to convert a value from one type of 
data to another. Each of the conversion functions converts its parameter 
to an equivalent representation within its datatype. 
The conversion functions include int(), float(), char(), bytes(), and others. 

TODO: Explain what strings, floats, ints, and bytes are. 
"""

size(640, 360)
background(0)
noStroke()
textFont(createFont("Georgia", 24))

s = 'A'
sCode = ord(s)
f = float(sCode)  # Sets f = 65.0
i = int(f * 1.4)  # Sets i to 91
b = bytes(sCode / 2)  # Sets b to 32 

#String formatting in Python

#Use the % operator to insert the value of variables into the string. 
#You must specify the type of the variable after the % with the corresponding letter (see below). 
 
text("The value of variable s is %s" % s, 50, 100) # %s for strings
text("The value of variable f is %f" % f, 50, 150) # %f for floats
text("The value of variable i is %i" % i, 50, 200) # %i for integers
text("The value of variable b is %s" % b, 50, 250) 
text("The value of s is %s, f is %f, i is %i" % (s, f, i), 50, 300) 
