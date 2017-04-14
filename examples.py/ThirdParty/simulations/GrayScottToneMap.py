"""
<p>GrayScottToneMap shows how to use the ColorGradient & ToneMap classes of the
colorutils package to create a tone map for rendering the results of
the Gray-Scott reaction-diffusion.</p>

<p><strong>Usage:</strong><ul>
<li>click + drag mouse to draw dots used as simulation seed</li>
<li>press any key to reset</li>
</ul></p>

<p>UPDATES:<ul>
<li>2011-01-18 using ToneMap.getToneMappedArray()</li>
</ul></p>
"""

""" 
Copyright (c) 2010 Karsten Schmidt

This demo & library is free software you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation either
version 2.1 of the License, or (at your option) any later version.

http:#creativecommons.org/licenses/LGPL/2.1/

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import toxi.color.ColorGradient as ColorGradient
import toxi.color.NamedColor as NamedColor
import toxi.color.ToneMap as ToneMap
import toxi.sim.grayscott.GrayScott as GrayScott

NUM_ITERATIONS = 10 # NB: non-inclusive range in python

def setup():
    size(256,256)
    global gs, toneMap
    gs = GrayScott(width,height,False)
    gs.setCoefficients(0.021,0.076,0.12,0.06)
    # create a color gradient for 256 values
    grad = ColorGradient()
    # NamedColors are preset colors, but any TColor can be added
    # see javadocs for list of names:
    # http://toxiclibs.org/docs/colorutils/toxi/color/NamedColor.html
    grad.addColorAt(0,NamedColor.BLACK)
    grad.addColorAt(128,NamedColor.RED)
    grad.addColorAt(192,NamedColor.YELLOW)
    grad.addColorAt(255,NamedColor.WHITE)
    # this gradient is used to map simulation values to colors
    # the first 2 parameters define the min/max values of the
    # input range (Gray-Scott produces values in the interval of 0.0 - 0.5)
    # setting the max = 0.33 increases the contrast
    toneMap = ToneMap(0,0.33,grad)
    
def draw():
    if (mousePressed):
        gs.setRect(mouseX, mouseY,20,20)        
    loadPixels()
    # update the simulation a few time steps
    for i in range(0, NUM_ITERATIONS):
        gs.update(1)  
    # read out the V result array
    # and use tone map to render colours
    toneMap.getToneMappedArray(gs.v,pixels)
    updatePixels()
  
def keyPressed():
    gs.reset()
