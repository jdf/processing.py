#!/usr/bin/python
"""
    Utility to do whatever mechanical work can be done in converting
    PDE examples to Python ones.
"""
from __future__ import with_statement

import logging
from optparse import OptionParser
import os
import re
import shutil
import sys


def usage():
    print >> sys.stderr, 'Usage: pde2py [-f|--force] srcdir destdir'
    sys.exit(1)

parser = OptionParser()
parser.add_option("-f", "--force",
                  action="store_true", dest="force", default=False,
                  help="don't print status messages to stdout")

(opts, args) = parser.parse_args()

if len(args) < 2:
    usage()

src, dest = args
if not (os.path.exists(src) and os.path.isdir(src)):
    usage()
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)


def copy_dir(s, d):
    if not os.path.exists(d):
        os.mkdir(d)
    for f in os.listdir(s):
        if f[0] == '.':
            continue
        copy(os.path.join(s, f), os.path.join(d, f))


def copy_file(s, d, xform=None):
    with open(s, 'rb') as f:
        text = f.read()
    if xform:
        (d, text) = xform(d, text)
    if os.path.exists(d):
        if opts.force:
            logging.info('Overwriting %s.' % d)
        else:
            logging.warning('Not overwriting %s.' % d)
    else:
        logging.info('Writing %s.' % d)
    with open(d, 'wb') as f:
        f.write(text)


def xform_py(d, text):
    d = re.sub(r'^(.+?).pde$', r'\1.py', d)
    text = text.replace('//', '#')
    text = text.replace('  ', '    ')
    text = re.sub(r'(?m)^(\s*)(?:void|int|float|String)\s+([a-zA-Z0-9]+)\s*\(([^\)]*)\)',
                  r'\1def \2(\3):',
                  text)
    text = re.sub(
        r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*$', r'class \1:', text)
    text = re.sub(
        r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*extends\s*(\S+)\s*$', r'class \1(\2):', text)
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
    text = text.replace('this.', 'self.')
    text = text.replace('||', 'or')
    text = text.replace('&&', 'and')
    return (d, text)


def copy(s, d):
    if os.path.isdir(s):
        copy_dir(s, d)
    elif s.endswith(".pde"):
        copy_file(s, d, xform_py)
    else:
        copy_file(s, d)

copy(src, dest)
