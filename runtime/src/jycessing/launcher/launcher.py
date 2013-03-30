
import jycessing.launcher.LaunchHelper as LaunchHelper
import jycessing.Runner as Runner

import java.lang.System as System

import os, shutil, zipfile, sys, inspect, stat


class launcher(object):
    @staticmethod
    def create(
			bundle = [],
			platforms=["mac", "win"], 
			outdir="dist.platforms", 
			ignorelibs=["*video*"]
		):
		"""Creates a launcher for the given platform"""


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

			main = System.getProperty("python.main")
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

			# Copy main script 
			try: os.mkdir(root + "/" + "Runtime")
			except: pass

			shutil.copyfile(main, root + "Runtime/sketch.py")


		# We dont want to return
		System.exit(0)

				
sys.modules["launcher"] = launcher
