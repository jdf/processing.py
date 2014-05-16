"""
Loop. 

Shows how to load and play a QuickTime movie file.    

"""
import processing.video.*
Movie movie
def setup(): 
    size(640, 360)
    background(0)
    # Load and play the video in a loop
    movie = Movie(this, "transit.mov")
    movie.loop()
def movieEvent(Movie m): 
    m.read()
def draw(): 
    #if (movie.available() == True) 
    #    movie.read()
    #
    image(movie, 0, 0, width, height)
