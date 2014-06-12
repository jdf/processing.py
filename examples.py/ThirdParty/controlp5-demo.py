# Download ControlP5 from http://www.sojamo.de/libraries/controlP5/
# Drop the controlP5 folder into your processing.py libraries folder.
# This demo is adapted from one of the ControlP5 demos.

from controlP5 import ControlP5
from controlP5 import Slider

myColor = color(0,0,0)
sliderValue = 100
sliderTicks1 = 100
sliderTicks2 = 30

def demo_listener(e):
  print(e)

def setup():
  size(700,400)
  noStroke()
  cp5 = ControlP5(this)

  # add a horizontal sliders, the value of this slider will be linked
  # to variable 'sliderValue'
  cp5.addSlider("sliderValue").setPosition(100,50).setRange(0,255) \
      .addListener(demo_listener)

  # create another slider with tick marks, now without
  # default value, the initial value will be set according to
  # the value of variable sliderTicks2 then.
  cp5.addSlider("sliderTicks1").setPosition(100,140).setSize(20,100) \
      .setRange(0,255).setNumberOfTickMarks(5).addListener(demo_listener)

  # add a vertical slider
  cp5.addSlider("slider").setPosition(100,305).setSize(200,20) \
      .setRange(0,200).setValue(128).addListener(demo_listener)


  # reposition the Label for controller 'slider'
  cp5.getController("slider").getValueLabel() \
      .align(ControlP5.LEFT, ControlP5.BOTTOM_OUTSIDE).setPaddingX(0)
  cp5.getController("slider").getCaptionLabel() \
      .align(ControlP5.RIGHT, ControlP5.BOTTOM_OUTSIDE).setPaddingX(0)

  cp5.addSlider("sliderTicks2").setPosition(100,370).setWidth(400) \
     .setRange(255,0).setValue(128).setNumberOfTickMarks(7) \
     .setSliderMode(Slider.FLEXIBLE).addListener(demo_listener)

def draw():
  background(sliderTicks1)

  fill(sliderValue)
  rect(0,0,width,100)

  fill(myColor)
  rect(0,280,width,70)

  fill(sliderTicks2)
  rect(0,350,width,50)
