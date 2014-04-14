#!/bin/bash
#export VERBOSE_PYTHON_MODE=true

PROCESSING=~/processing
PROCESSINGPY=~/processing.py
RUNPROCESSING=$PROCESSING/build/linux/work/processing
#RUNPROCESSING=$PROCESSING/build/macosx/work/Processing.app/Contents/MacOS/Processing
MODES=~/sketchbook/modes
#MODES=/Users/feinberg/Documents/Processing/modes

cd $PROCESSING/build && \
  #ant macosx-build && \
  cd $PROCESSINGPY && \
  ant zip-mode && \
  cd $MODES && \
  rm -rf PythonMode && \
  unzip $PROCESSINGPY/PythonMode.zip && \
  cd /tmp && \
  $RUNPROCESSING

