"""
Demonstrates using a third-party Python library
author: Jonathan Feinberg
"""
from namethatcolor import NameThatColor

flag = loadImage("flag.jpg")
namer = NameThatColor()

def setup():
    size(200, 200)

def draw():
    background(0)
    image(flag, 75, 40 )
    if mouseX >= 0 and mouseX <= width and mouseY >= 0 and mouseY <= height: 
        text(namer.name(hex(0x00FFFFFF & get(mouseX, mouseY))[2:]).name, 60, 120)