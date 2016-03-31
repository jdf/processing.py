#!/bin/bash
export VERBOSE_PYTHON_MODE=true

PROCESSING=~/processing
PROCESSINGPY=~/processing.py

MODES=~/Documents/Processing/modes;
if [[ $(uname) == 'Darwin' ]]; then
	RUNPROCESSING=$PROCESSING/build/macosx/work/Processing.app/Contents/MacOS/Processing
else 
	RUNPROCESSING="$PROCESSING/build/windows/work/processing.exe"
	MODES=~/feinberg/Documents/Processing/modes;
fi

cd "$PROCESSING/build" && \
  #ant && \
  cd "$PROCESSINGPY" && \
  ant mode.zip && \
  cd "$MODES" && \
  rm -rf PythonMode && \
  unzip "$PROCESSINGPY/work/PythonMode.zip" && \
  cd /tmp && \
  "$RUNPROCESSING"
