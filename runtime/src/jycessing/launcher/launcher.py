import sys


# Our virtual "launcher" name space 
class __launcher(object):
    @staticmethod
    def create(
            name = "Launcher",
            bundle = [],
            platforms=["mac", "win"], 
            outdir="dist.platforms", 
            ignorelibs=["*video*"]
        ):
        """Creates a launcher for the given platform"""

        import jycessing.Runner as Runner
        import jycessing.launcher.StandaloneSketch as StandaloneSketch
        import sys
        # Check if we should bail out - we're not running from a standalone sketch
        if not isinstance(Runner.sketch, StandaloneSketch):
            print >>sys.stderr, "Don't use launcher.create() from processing - use the export button instead!"
            return

        # Check if we are already deployed. In that case, 
        # don't do anything
        if "--internal" in sys.argv: return

        # Our own imports 
        import jycessing.launcher.LaunchHelper as LaunchHelper
        
        import java.lang.System as System
        import java.nio.file.Paths as Paths
        import os, shutil, zipfile, inspect, stat, glob, errno

        main = System.getProperty("python.main")
        mainroot = System.getProperty("python.main.root")

        outdir = mainroot + "/" + outdir

        # Clean the outdir ...
        try: shutil.rmtree(outdir) 
        except: pass


        def copyeverything(src, dst):
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

        def copyjars(root):
            """Copy jars & co"""
            sketch = Runner.sketch
            _mainjar = sketch.getMainJarFile()
            mainjar, mainjarname = _mainjar.getAbsolutePath(), _mainjar.getName()
            shutil.copyfile(mainjar, root + "/" + mainjarname)
            
            libraries = sketch.getLibraryDirectories()
            for lib in libraries:
                shutil.copytree(lib.getPath(), root + "/libraries", ignore=shutil.ignore_patterns(*ignorelibs))


        def copydata(runtimedir):
            """Copy the main script and the given data"""
            # Create runtime directory 

            try: os.mkdir(runtimedir)
            except: pass

            # Copy bundled files
            for data in bundle:
                for f in list(glob.iglob(mainroot + "/" + data)):
                    copyeverything(f, runtimedir + "/" + f.replace(mainroot, ""))


            # Eventually copy the main file
            shutil.copyfile(main, runtimedir + "/sketch.py")


        # ... and recreate it
        os.mkdir(outdir)
        for platform in platforms: 

            pdir = outdir + "/" + platform
            tmpfile = pdir + ".zip"

            os.mkdir(pdir)

            # Copy archive
            LaunchHelper.copyResourceTo("launcher." + platform + ".zip", Paths.get(tmpfile))
            
            # Unzip
            z = zipfile.ZipFile(tmpfile, "r")
            z.extractall(pdir)
            z.close()

            # Try to remove the platform file we created
            try:
                os.remove(tmpfile)
            except Exception, e:
                print("Could not remove %s we used for creating the launcher. Please report." % tmpfile, e)
            


        # Now the platform specific logic
        if "mac" in platforms:    
            root = outdir + "/mac/Processing.app/Contents/"            

            # Set launcher permissions ... mmhm, when created on Windows this 
            # might lead to trouble ... Any ideas?
            mode = os.stat(root + "/MacOS/JavaAppLauncher").st_mode
            os.chmod(root + "/MacOS/JavaAppLauncher", mode | stat.S_IXUSR)
        
            # Copy the jars and app
            copyjars(root + "Java")    
            copydata(root + "/Runtime")
        
            # Adjust Info.plist
            # TODO

            os.rename(outdir + "/mac/Processing.app", outdir + "/mac/" + name + ".app/")


        if "win" in platforms:    
            root = outdir + "/win/"    

            # Copy the jars and app
            copyjars(root)    
            copydata(root + "/runtime")

            os.mkdir(root + "/jre/")

            JREREADME = open(root + "/jre/README.txt", "w")            
            JREREADME.write("In the future, you can place your JRE in here (not implemented yet).")
            JREREADME.close()

            # Adjust the launcher.ini
            # TODO

            # delete the console version (for now)
            os.remove(root + "/launcherc.exe")

            os.rename(root + "/launcher.exe", root + "/" + name.lower() + ".exe")
            os.rename(root + "/launcher.ini", root + "/" + name.lower() + ".ini")


        # We dont want to return
        System.exit(0)

            
# Set the name space 
sys.modules["launcher"] = __launcher
