import launcher
import jycessing.Runner as Runner

rval = ""

try:
    # At the moment there is no lightweight way to test these ...s
    rval += "C" if "create" in dir(launcher) else "c"
    rval += "M" if "getMainJarFile" in dir(Runner) else "m"
    rval += "L" if "getLibraries" in dir(Runner) else "l"    
    rval += "X" if "DOES_NOT_EXIST" in dir(Runner) else "x"    
except Exception:
    pass
print(rval)
exit()