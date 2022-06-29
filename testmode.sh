#!/bin/bash
export VERBOSE_PYTHON_MODE=true

PROCESSINGPY=$(pwd)
PROCESSING=../processing4

MODES=~/Documents/Processing/modes;
if [[ $(uname) == 'Darwin' ]]; then
	RUNPROCESSING=$PROCESSING/build/macos/work/Processing.app/Contents/MacOS/Processing
else
	RUNPROCESSING="$PROCESSING/build/linux/work/processing"
	MODES=~/sketchbook/modes;
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
