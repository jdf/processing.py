#!/bin/bash
export VERBOSE_PYTHON_MODE=true

PROCESSING=~/processing
PROCESSINGPY=~/processing.py

if [[ $(uname) == 'Darwin' ]]; then
	RUNPROCESSING=$PROCESSING/build/macosx/work/Processing.app/Contents/MacOS/Processing
	MODES=~/Documents/Processing/modes;
else 
	RUNPROCESSING=$PROCESSING/build/linux/work/processing
	MODES=~/sketchbook/modes;
fi

cd $PROCESSING/build && \
  #ant && \
  cd $PROCESSINGPY && \
  ant mode.zip && \
  cd $MODES && \
  rm -rf PythonMode && \
  unzip $PROCESSINGPY/work/PythonMode.zip && \
  cd /tmp && \
  $RUNPROCESSING
