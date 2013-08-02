#!/usr/bin/python
"""
    Utility to do whatever mechanical work can be done in converting
    PDE examples to Python ones.
"""
from __future__ import with_statement

import os
import re
import shutil
import sys

src, dest = sys.argv[1:]
if not (os.path.exists(src) and os.path.isdir(src)):
    raise Exception("I expect the first argument to be the source directory.")
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)

def copy_dir(s, d):
    if not os.path.exists(d):
        os.mkdir(d)
    for file in os.listdir(s):
        if file[0] == '.':
            continue
        copy(os.path.join(s, file), os.path.join(d, file))

def copy_file(s, d, xform=None):
    with open(s, 'rb') as f:
        text = f.read()
    if xform:
        (d, text) = xform(d, text)
    if os.path.exists(d):
        raise Exception("I refuse to overwrite %s." % d)
    with open(d, 'wb') as f:
        f.write(text)

def xform_py(d, text):
    d = re.sub(r'^(.+?).pde$', r'\1.py', d)
    text = text.replace('//', '#')
    text = text.replace('  ', '    ')
    text = re.sub(r'(?m)^(\s*)(?:void|int|float|String)\s+([a-zA-Z0-9]+)\s*\(([^\)]*)\)',
                  r'\1def \2(\3):',
                  text)
    text = re.sub(r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*$', r'class \1:', text)
    text = re.sub(r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*extends\s*(\S+)\s*$', r'class \1(\2):', text)
    text = re.sub(r'(?m)^(\s*)(?:void|int|float|String)\s+', r'\1', text)
    text = re.sub(r'[{};]', '', text)
    text = re.sub(r'\n\n+', '\n', text)
    text = re.sub(r'(?m)^(\s*)if\s*\((.+?)\)\s*$', r'\1if \2:', text)
    text = re.sub(r'(?m)^(\s*)else\s+if\s*\((.+?)\)\s*$', r'\1elif \2:', text)
    text = re.sub(r'(?m)^(\s*)else\s*$', r'\1else:', text)
    text = re.sub(r'/\*+|\*+/', '"""', text)
    text = text.replace('new ', '')
    text = text.replace('true', 'True')
    text = text.replace('false', 'False')
    text=text.replace('this.', 'self.')
    return (d, text)

def copy(s, d):
    if os.path.isdir(s):
        copy_dir(s, d)
    elif s.endswith(".pde"):
        copy_file(s, d, xform_py)
    else:
        copy_file(s, d)

copy(src, dest)
