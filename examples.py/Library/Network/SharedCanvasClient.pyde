"""
Shared Drawing Canvas (Client) by Alexander R. Galloway. 

The Processing Client class is instantiated by specifying a remote 
address and port number to which the socket connection should be made. 
Once the connection is made, client may read (or write) data to the server.
Before running this program, the Shared Drawing Canvas (Server) program.
"""

add_library('net')  # import processing.net.*

def setup():
    global c
    size(450, 255)
    background(204)
    stroke(0)
    frameRate(5)  # Slow it down a little
    # Connect to the server's IP address and port
    c = Client(this, "127.0.0.1", 12345)
    # Replace with your server's IP and port

def draw():
    if mousePressed == True:
        # Draw our line
        stroke(255)
        line(pmouseX, pmouseY, mouseX, mouseY)
        # Send mouse coords to other person
        c.write(str(pmouseX) + " " +
                str(pmouseY) + " " +
                str(mouseX) + " " +
                str(mouseY) + "\n")

    # Receive data from server
    if c.available():  # c.available > 0
        input = c.readString()
        input = input[:input.find("\n")]  # Only up to the newline
        data = [int(coord)
                for coord in input.split()]  # Split values into list
        # Draw line using received coords
        stroke(0)
        line(data[0], data[1], data[2], data[3])
