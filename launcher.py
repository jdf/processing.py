
import jycessing.launcher.LaunchHelper as LaunchHelper
import os, shutil

def timestamp():
	"""Returns the current timestamp"""

def create(platforms=["mac", "win"], outdir="dist.platforms"):

	# Quick check if we are already deployed. In that case, 
	# don't do anything

	# TODO

	# Clean the outdir ...
	try: shutil.rmtree(outdir) 
	except: pass

	# ... and recreate it
	os.mkdir(outdir)
	for platform in platforms: os.mkdir(outdir + "/" + platform)


	# Now the platform specific logic
	if "mac" in platforms:
		pass
		
	