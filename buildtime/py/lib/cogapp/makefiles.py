""" Dictionary-to-filetree functions, to create test files for testing.
    http://nedbatchelder.com/code/cog
    
    Copyright 2004-2009, Ned Batchelder.
"""

import path     # Non-standard, from http://www.jorendorff.com/articles/python/path
from whiteutils import reindentBlock

__version__ = '1.0.20040126'
__all__ = ['makeFiles', 'removeFiles']

def makeFiles(d, basedir='.', raw=False):
    """ Create files from the dictionary d, in the directory named by dirpath.
    """
    dirpath = path.path(basedir)
    for name, contents in d.items():
        child = dirpath / name
        if isinstance(contents, basestring):
            mode = 'w'
            if raw:
                mode = 'wb'
            f = open(child, mode)
            if not raw:
                contents = reindentBlock(contents)
            f.write(contents)
            f.close()
        else:
            if not child.exists():
                child.mkdir()
            makeFiles(contents, child, raw=raw)

def removeFiles(d, basedir='.'):
    """ Remove the files created by makeFiles.
        Directories are removed if they are empty.
    """
    dirpath = path.path(basedir)
    for name, contents in d.items():
        child = dirpath / name
        if isinstance(contents, basestring):
            child.remove()
        else:
            removeFiles(contents, child)
            if not child.files() and not child.dirs():
                child.rmdir()

if __name__ == '__main__':      #pragma: no cover
    # Try it a little.
    d = {
        'test_makefiles': {
            'hey.txt': """\
                        This is hey.txt.
                        It's very simple.
                        """,
            'subdir': {
                'fooey': """\
                            # Fooey
                                Kablooey
                            Ew.
                            """
            }
        }
    }
    makeFiles(d)
