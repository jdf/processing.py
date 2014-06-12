"""
Boolean Operators. 

The boolean operators "and" and "or" are used to 
combine simple relational statements into more complex expressions.
The "not" operator is used to negate a boolean statement. 
"""

size(640, 360)
background(126)

test = False

for i in range(5, height + 5, 5):
    # Boolean "and"
    stroke(0)
    if i > 35 and i < 100:
        line(width / 4, i, width / 2, i)
        test = False

    # Boolean "or"
    stroke(76)
    if i <= 35 or i >= 100:
        line(width / 2, i, width, i)
        test = True

    # Testing if a boolean value is "True"
    # The expression "if test" is equivalent to "if test == True".
    if test:
        stroke(0)
        point(width / 3, i)

    # Testing if a boolean value is "False"
    # The expression "if not test" is equivalent to "if test == False".
    if not test:
        stroke(255)
        point(width / 4, i)

