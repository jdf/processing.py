"""
 * Listing files in directories and subdirectories
 * inspired by an example by Daniel Shiffman.
 *
 * 1) List the names of files in a directory
 * 2) List the names along with metadata (size, lastModified)
 *        of files in a directory
 * 3) List the names along with metadata (size, lastModified)
 *        of files in a directory and all subdirectories (using recursion)
"""

from datetime import datetime
import os

def sizeof_fmt(num):
    for fmt in ['%3d bytes', '%3dK', '%3.1fM', '%3.1fG']:
        if num < 1024.0:
            return fmt % num
        num /= 1024.0

def print_file_details(f, depth=0):
    if os.path.basename(f)[0] == '.':
        return            # no dotfiles
    print '  ' * depth,   # funny Python syntax: trailing comma means no newline
    if os.path.isdir(f):
        print "+%s" % os.path.basename(f)
    else:
        mtime = datetime.fromtimestamp(os.path.getmtime(f))
        info = '%s, modified %s' % (sizeof_fmt(os.path.getsize(f)),
                                    mtime.strftime("%Y-%m-%d %H:%M:%S"))
        print "%-30s %s" % (os.path.basename(f), info)

def list_recursively(f, depth=0):
    if os.path.basename(f)[0] == '.':
        return # no dotfiles
    print_file_details(f, depth)
    if os.path.isdir(f):
        for g in os.listdir(f):
            path = os.path.join(f, g)
            list_recursively(path, depth + 1)

topdir = os.getcwd()

print "Listing names of all files in %s:" % topdir
for f in os.listdir(topdir):
    print f

print "Listing info about all files in %s:" % topdir
for f in os.listdir(topdir):
    print_file_details(f)

print "---------------------------------------"
print "Descending into %s:" % topdir
list_recursively(topdir)

exit()
