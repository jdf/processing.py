#!/bin/bash
cd /Users/feinberg/processing/build && \
  ant -Dversion=feinberg macosx-dist && \
  scp -i ~/.ssh/id_rsa-processing.org macosx/processing-feinberg-macosx.zip jdf@processing.org:/var/www/py && \
  cd ../../processing.py && \
  ant upload-mode
