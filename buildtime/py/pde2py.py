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
    # Remove closing brace.
    text = text.replace('}', '')
    # Remove trailing spaces - first pass.
    text = re.sub(r'(?m)[ ]{1,}$', '', text)
    # Fix inline comments.
    text = text.replace('//', '#')
    # Save "history" for indent. We may end up with extraneous double-spaces
    # after this; we have no way of distinguishing between them and
    # legitimate indent.
    text = re.sub(r' {2}', r'\t', text)
    # Fix functions - remove return type identifiers and add 'def' keyword.
    text = re.sub(
        r'(?m)^(\s*)(?:public void|void|public int|int|public float|float|public String|String)\s+([a-zA-Z0-9]+)\s*\(([^\)]*)\)',
        r'\1def \2(\3):',
        text)
    # Fix class definitions.
    text = re.sub(
        r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*$', r'class \1:', text)
    text = re.sub(
        r'(?m)^\s*(?:abstract\s+)?class\s+(\S+)\s*extends\s*(\S+)\s*$',
        r'class \1(\2):',
        text)
    text = re.sub(r'(?m)^(\s*)(?:void|int|float|String|public)\s+', r'\1', text)
    # Remove as many type identifiers as possible.
    text = re.sub(
        r'\b(int|byte|short|long|float|double|boolean|char|String|final)(\(|\s|\[)+?',
        r'',
        text)
    text = re.sub(
        r'\((int|byte|short|long|float|double|boolean|char|String|final|Integer|Object)\)',
        r'',
        text)
    # Fix 'if'.
    text = re.sub(r'(?m)^(\s*)if\s*(?:\()?(.+\)*?)(?:\))(.*)(?:\{)*$', r'\1if \2:\n\1\t\3', text)
    # Fix 'else if'.
    text = re.sub(r'(?m)^(\s*)else\s+if\s*(?:\()?(.+\)*?)(?:\))(.*)(?:\{)*$', r'\1elif \2:', text)
    # Fix 'else'.
    text = re.sub(r'(?m)^(\s*)else(.*)(?:\{)*$', r'\1else:\n\1\t\2', text)
    # Fix block comments (convert to docstrings, really).
    text = re.sub(r'/\*+|\*+/', '"""', text)
    # Remove 'new'.
    text = text.replace('new ', '')
    # Fix booleans.
    text = text.replace('true', 'True')
    text = text.replace('false', 'False')
    # Fix 'this'.
    text = text.replace('this(\.?)', 'self\1')
    # Fix boolean operators.
    text = text.replace('||', ' or ')
    text = text.replace('&&', ' and ')
    # Remove 'f' (float coercion... I guess...
    #             How is '0.09f' different from '0.09'?! ::smh::).
    text = re.sub(r'(\d)f', r'\1', text)
    # Add spaces after commas.
    text = text.replace(',', ', ')
    # Remove spaces before colons.
    text = text.replace(' :', ':')
    # Add spaces around operators.
    text = re.sub(
        r'([a-zA-Z0-9_()]+?)(!=|\*=|\+=|-=|\/=|==|>=|<=|=|\*|\+|-|\/|>|<|%|&)([a-zA-Z0-9_()]+?)',
        r'\1 \2 \3',
        text)
    # Remove spaces around parens/brackets.
    text = re.sub(r'(?: {1,})(\)|\])', r'\1', text)
    text = re.sub(r'(\(|\[)(?: {1,})', r'\1', text)
    # Fix up 'for'. Hopefully this makes it a *bit* more readable. In any
    #       case, we'll try to at least get the colon in at the end.
    text = re.sub(
        r'(?m)^(\s*)for\s*(?:\()(?:int|float)*(.*?);(.*?);(.*?)(?:\)).*$',
        r'\1for \2 in range(\3):  # \4',
        text)
    # Fix up imports. Obviously, since we're going from 'import *' to
    #       specifics, rthe end user has to figure out what to import. That
    #       being the cawse, I'm commenting out the imports to (hopefuilly)
    #       call attention to them. In any case, they'll definitely be found
    #       by any good linter
    text = re.sub(r'(?m)^import(.*)\.\*;', r'# from\1 import', text)
    # Remove brackets/remaining braces/semicolons.
    text = re.sub(r'[{;]', '', text)
    # Remove multiple spaces.
    text = re.sub(r'( ){2,}', ' ', text)
    # Remove trailing spaces, second pass.
    text = re.sub(r'(?m)[ ]{1,}$', '', text)
    # Restore indent with 4 spaces.
    text = re.sub(r'\t', '    ', text)
    # Remove multiple blank lines.
    text = re.sub(r'(?m)^\n{3}', '\n', text)
    return (d, text)


def copy(s, d):
    if os.path.isdir(s):
        copy_dir(s, d)
    elif s.endswith(".pde"):
        copy_file(s, d, xform_py)
    else:
        copy_file(s, d)

copy(src, dest)
