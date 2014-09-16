'''
Strings

TODO: Add Python-specific description. 

TODO: Make a more Pythonic example showing string manipulation 
      in Python (e.g. string multiplication)?
'''

letter = ' ' # Strings can be written in single quotes
words = "Begin..." # Or double quotes

#Or triple quotes for multi-line strings
morewords = """
I 
am
a
multi-line
string
"""

def setup(): 
    size(640, 360)
    # Create the font
    textFont(createFont("Georgia", 36))

def draw(): 
    background(0)# Set background to black
    # Draw the letter to the center of the screen
    textSize(14)
    # Concatenate (combine) strings by juxtaposition:  
    text("Click on the program, "
    "then type to add to the String", 50, 50)
    text("Current key: " + letter, 50, 70)
    text("The String is " + str(len(words)) +    " letters long", 50, 90)    
    textSize(36)
    text(words, 50, 120)
    
def keyPressed(): 
    global letter, words

    # The variable "key" always contains the value 
    # of the most recent key pressed.
    if ('A' <= key <= 'z') or key == ' ':
        letter = key
        words += key
        
        #Hack to bound text to window
        #Remove when rectangular bounding is added for text()
        if len(words) % 30 == 0: 
            words += '\n'
        
        # Write the letter to the console
        println(key)
    
