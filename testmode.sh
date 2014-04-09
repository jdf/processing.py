#!/bin/bash
export VERBOSE_PYTHON_MODE=true
cd /Users/feinberg/processing/build && \
  #ant macosx-build && \
  cd ../../processing.py && \
  ant zip-mode && \
  rm -rf /Users/feinberg/Documents/Processing/modes/PythonMode && \
  cd /Users/feinberg/Documents/Processing/modes && \
  unzip /Users/feinberg/processing.py/PythonMode.zip && \
  cd /tmp && \
  /Users/feinberg/processing/build/macosx/work/Processing.app/Contents/MacOS/Processing

