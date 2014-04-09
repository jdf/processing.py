#!/bin/bash
cd /Users/feinberg/processing/build && \
  ant -Dversion=feinberg macosx-dist && \
  scp -i ~/.ssh/id_rsa-processing.org macosx/processing-feinberg-macosx.zip jdf@processing.org:/var/www/py && \
  cd ../../processing.py && \
  ant zip-mode && \
  scp -i ~/.ssh/id_rsa-processing.org PythonMode.zip jdf@processing.org:/var/www/py && \
  scp -i ~/.ssh/id_rsa-processing.org PythonMode_0211.zip jdf@processing.org:/var/www/py
