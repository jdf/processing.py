import sys


def __copyeverything(src, dst):
	"""The Machine That Copies EVERYTHING.
	https://www.youtube.com/watch?v=ibEdgQJEdTA
	"""
	import shutil, errno

	try:
		shutil.copytree(src, dst)
	except OSError as exc:
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dst)
		else: raise


# Our virtual "launcher" name space 
class __launcher(object):
    @staticmethod
    def create(
			bundle = [],
			platforms=["mac", "win"], 
			outdir="dist.platforms", 
			ignorelibs=["*video*"]
		):
		"""Creates a launcher for the given platform"""

		# Our own imports 
		import jycessing.launcher.LaunchHelper as LaunchHelper
		import jycessing.Runner as Runner
		import java.lang.System as System
		import os, shutil, zipfile, sys, inspect, stat, glob, errno

		main = System.getProperty("python.main")
		mainroot = System.getProperty("python.main.root")

		outdir = mainroot + "/" + outdir

		# Quick check if we are already deployed. In that case, 
		# don't do anything
		if "--internal" in sys.argv: return

		# Clean the outdir ...
		try: shutil.rmtree(outdir) 
		except: pass

		# ... and recreate it
		os.mkdir(outdir)
		for platform in platforms: os.mkdir(outdir + "/" + platform)


		# Now the platform specific logic
		if "mac" in platforms:	
			# Copy archive
			LaunchHelper.copyTo("launcher.mac.zip", outdir + "/" + "mac.zip")

			root = outdir + "/" + "mac/Processing.app/Contents/"			

			# Unzip
			z = zipfile.ZipFile(outdir + "/" + "mac.zip", "r")
			z.extractall(outdir + "/" + "mac")
			z.close()

			# Set launcher permissions ... mmhm, when created on Windows this 
			# might lead to trouble ... Any ideas?
			mode = os.stat(root + "/MacOS/JavaAppLauncher").st_mode
			os.chmod(root + "/MacOS/JavaAppLauncher", mode | stat.S_IXUSR)

			os.remove(outdir + "/" + "mac.zip")
			
			# Copy jars & co
			_mainjar = Runner.getMainJarFile()
			mainjar, mainjarname = _mainjar.getAbsolutePath(), _mainjar.getName()
			libraries = Runner.getLibrariesDir().getAbsolutePath()

			shutil.copyfile(mainjar, root + "Java/"+ mainjarname)
			shutil.copytree(libraries, root + "Java/libraries", ignore=shutil.ignore_patterns(*ignorelibs))

			# Adjust Info.plist
			# TODO

			# Create runtime directory 
			runtimedir = root + "/" + "Runtime"

			try: os.mkdir(runtimedir)
			except: pass

			# Copy bundled files
			for data in bundle:
				for f in list(glob.iglob(mainroot + "/" + data)):
					__copyeverything(f, runtimedir + "/" + f.replace(mainroot, ""))


			# Eventually copy the main file
			shutil.copyfile(main, runtimedir + "/sketch.py")


		# We dont want to return
		System.exit(0)

			
# Set the name space 
sys.modules["launcher2"] = __launcher
