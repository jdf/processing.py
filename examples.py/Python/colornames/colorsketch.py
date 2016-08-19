"""
Demonstrates using a third-party Python library
author: Jonathan Feinberg
"""
from namethatcolor import NameThatColor

namer = NameThatColor()

def setup():
    size(200, 200)
    global flag
    flag = loadImage("flag.jpg")

def draw():
    background(0)
    image(flag, 75, 40 )
    if mouseX >= 0 and mouseX <= width and mouseY >= 0 and mouseY <= height:
        c = 0x00FFFFFF & get(mouseX, mouseY)
        fill(c >> 16, c >> 8 & 0xFF, c & 0xFF)
        text(namer.name(hex(c)[2:]).name, 75, 120)