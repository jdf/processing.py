#!/usr/bin/env python
# script to fix opengl on processing.py for 64-bit linux
# needs to be run in the home directory of processing
# backs-up original 32 bit binaries

import os
import os.path 
import shutil  # cross platform support
import glob
import zipfile

home = os.getcwdu()
processing_dir = os.path.join(home, "real_processing.py")

library_dir = os.path.join(processing_dir, "libraries", "processing", "opengl")
backup_dir = os.path.join(library_dir, "original-native")
unpack_dir = os.path.join(library_dir, "unpack-amd64")
if (os.path.exists(backup_dir)):
    pass
else:  
    os.mkdir(backup_dir, 0777)
if (os.path.exists(unpack_dir)):
    pass
else:  
    os.mkdir(unpack_dir, 0777)  

alljars = glob.glob(os.path.join(library_dir,"*.jar")) 
jars64 = []
for jar in alljars:
    if jar.endswith("linux-amd64.jar"):
      jars64.append(jar)

for jar64 in jars64:
    zfobj = zipfile.ZipFile(jar64)
    for name in zfobj.namelist():
        if (name.endswith('/')):
            pass
        elif (name.endswith(".so")):
            outfile = open(os.path.join(unpack_dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

libraries = glob.glob(os.path.join(unpack_dir, "*.so"))
for so_file in libraries:
        src = os.path.join(library_dir, os.path.basename(so_file))
        if (not os.path.exists(os.path.join(backup_dir, os.path.basename(so_file)))):
            shutil.move(src, backup_dir)
            shutil.copy(so_file, library_dir) 
