#!/usr/bin/python
"""
    Attempts to convert clauses of the form
    
    pushFoo()
    blah()
    blah()
    popFoo()
    
    into
    
    with pushFoo():
        blah()
        blah()
"""
import re
import os
from os.path import join

pairs = [(re.compile(r'^(\s*)(%s)\s*$' % push), re.compile(r'^\s*(%s)\s*$' % pop))
          for push, pop in ((r'pushMatrix\( *\)', r'popMatrix\( *\)'),
                            (r'pushStyle\( *\)', r'popStyle\( *\)'),
                            (r'beginContour\( *\)', r'endContour\( *\)'),
                            (r'beginPGL\( *\)', r'endPGL\( *\)'),
                            (r'beginShape\( *[A-Z]* *\)', r'endShape\( *[A-Z]* *\)'),
                            (r'pushMatrix\( *\)', r'popMatrix\( *\)'))]

def convert(lines):
    stack = []
    result = []
    for line in lines:
        special = False
        indent = '    ' * len(stack)
        for (push, pop) in pairs:
            m = push.match(line)
            if m:
                result.append('%s%swith %s:\n' % (indent, m.group(1), m.group(2)))
                stack.append(pop)
                special = True
                break
            if not stack:
                continue
            m = stack[-1].match(line)
            if m:
                stack.pop()
                # special case for closed shape
                if 'CLOSE' in m.group(1):
                    for offset in xrange(len(result)):
                        index = -(1 + offset)
                        if 'with beginShape(' in result[index]:
                            result[index] = result[index].replace('beginShape', 'beginClosedShape')
                            break                    
                special = True
                break
        if not special:
            result.append('%s%s' % (indent, line))
    if stack:
        raise Exception('Unpopped.')
    return result


for root, dirs, files in os.walk('/Users/feinberg/processing.py/mode/examples'):
    for file in files:
        if not (file.endswith('.pyde') or file.endswith('.py')):
            continue
        path = join(root, file)
        f = open(path)
        lines = f.readlines()
        f.close() 
        converted = convert(lines)
        f = open(path, 'w')
        f.writelines(converted)
        f.close()