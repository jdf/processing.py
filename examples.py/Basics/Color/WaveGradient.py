"""
  Wave Gradient 
  by Ira Greenberg.
  Adapted to python by Jonathan Feinberg  
   
  Generate a gradient along a sin() wave.
"""
import math

amplitude = 30
fillGap = 2.5

def setup():
  size(200, 200)
  background(200, 200, 200)
  noLoop()

def draw():
  frequency = 0
  for i in range(-75, height + 75):
    # Reset angle to 0, so waves stack properly
    angle = 0
    # Increasing frequency causes more gaps
    frequency += .006
    for j in range(width + 75):
      py = i + sin(radians(angle)) * amplitude
      angle += frequency
      c = color(abs(py - i) * 255 / amplitude,
                255 - abs(py - i) * 255 / amplitude,
                j * (255.0 / (width + 50)))
      # Hack to fill gaps. Raise value of fillGap if you increase frequency
      for filler in range(int(math.ceil(fillGap))):
        set(int(j - filler), int(py) - filler, c)
        set(int(j), int(py), c)
        set(int(j + filler), int(py) + filler, c)
