#!/bin/bash
export VERBOSE_PYTHON_MODE=true

PROCESSINGPY=$(pwd)
PROCESSING=../processing

MODES=~/Documents/Processing/modes;
if [[ $(uname) == 'Darwin' ]]; then
	RUNPROCESSING=$PROCESSING/build/macosx/work/Processing.app/Contents/MacOS/Processing
elif [[ $(uname) == 'Linux' ]]; then
	RUNPROCESSING=$PROCESSING/build/linux/work/processing
	MODES=~/sketchbook/modes;
else 
	RUNPROCESSING="$PROCESSING/build/windows/work/processing.exe"
	MODES=/c/Users/Jonathan\ Feinberg/Documents/Processing/modes;
fi

cd "$PROCESSING/build" && \
  #ant && \
  cd "$PROCESSINGPY" && \
  ant mode.zip && \
  cd "$MODES" && \
  rm -rf PythonMode && \
  unzip "$PROCESSINGPY/work/PythonMode.zip" && \
  cd "$PROCESSINGPY" && \
  "$RUNPROCESSING"
