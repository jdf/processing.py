
import jycessing.primitives.PrimitiveFloat as Float


# Enable this to create a standalone version
#import launcher
#launcher.create()

# Use this for libraries such as "Ani"
f = Float(10.0) 

# Little test that the console output (or redirection 
# if started with "--redirect") works
print("You should see this in your debug output:", f)



def sketchFullScreen():
    """Override fullscreen"""
    return True


def setup():
	"""Override setup()"""
	size(displayWidth, displayHeight, P3D)

	frame.setTitle("Simple Test Application");


def draw():
	"""Override draw()"""
	# background(0)
	ellipse(mouseX, mouseY, f.value, f.value)
