"""
 * <p>GrayScottImage uses the seedImage() method to use a bitmap as simulation seed.
 * In this demo the image is re-applied every frame and the user can adjust the 
 * F coefficient of the reaction diffusion to produce different patterns emerging
 * from the boundary of the bitmapped seed. Unlike some other GS demos provided,
 * this one also uses a wrapped simulation space, creating tiled patterns.</p>
 *
 * <p><strong>usage:</strong></p>
 * <ul>
 * <li>click + drag mouse to locally disturb the simulation</li>
 * <li>press 1-9 to adjust the F parameter of the simulation</li> 
 * <li>press any other key to reset</li>
 * </ul>
 *
 * <p>UPDATES:<ul>
 * <li>2011-01-18 using ToneMap.getToneMappedArray()</li>
 * </ul></p>
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

def setup():
    size(256,256)
    global gs, img, toneMap
    gs = GrayScott(width,height,True)
    img = loadImage("ti_yong.png")
    # create a duo-tone gradient map with 256 steps
    toneMap = ToneMap(0,0.33,NamedColor.CRIMSON,NamedColor.WHITE,256)
    
def draw():
    gs.seedImage(img.pixels,img.width,img.height)
    if (mousePressed):
        gs.setRect(mouseX, mouseY,20,20)        
    loadPixels()
    for i in range(0, 10):
        gs.update(1)
    # read out the V result array
    # and use tone map to render colours
    toneMap.getToneMappedArray(gs.v,pixels)
    updatePixels()

def keyPressed():
    if (ord(key)>=49 and ord(key)<=57):
        gs.setF(0.02 + (ord(key) - 48) * 0.001)
    else:
        gs.reset() 

