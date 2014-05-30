"""
True/False. 

A Boolean variable has only two possible values: True or False. 
It is common to use Booleans with control statements to 
determine the flow of a program. In this example, when the
boolean value "x" is True, vertical black lines are drawn and when
the boolean value "x" is False, horizontal gray lines are drawn. 
"""

b = False
size(640, 360)
background(0)
stroke(255)
d = 20
middle = width / 2

for i in range(d, width + d, d):

    if i < middle:
        b = True
    else:
        b = False

    '''    
    Analogous to the above is:

    b = i < middle 
    
    Note: i < middle evaluates to a boolean True or False.
    '''

    if b:  # If b is True, run this block
        # Vertical line
        line(i, d, i, height - d)
    else:  # Otherwise, if b is False, run this block
        # Horizontal line
        line(middle, i - middle + d, width - d, i - middle + d)

