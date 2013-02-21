#!/bin/sh


BASEDIR=$(dirname "$0")

echo $BASEDIR
java -jar "$BASEDIR/processing-py.jar" "$1"