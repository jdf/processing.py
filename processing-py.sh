#!/usr/bin/env bash


####
#### The default script to run. Only used if none is given as an
#### optional argument
####
DEFAULT_SCRIPT="workspace/example.py"

####
#### JVM options to pass, such as requesting more RAM
####
JVM_ARGS="-Xmx1024m"


####
#
# Internal variables start here
#
####
JAVA=`which java`
THIS_FILE="$( readlink "$( which ${BASH_SOURCE[0]} )" || echo ${BASH_SOURCE[0]} )"
BASEDIR="$( cd "$( dirname $THIS_FILE )" && pwd )"
PLATFORM='unknown'
SPLASH="-splash:$BASEDIR/libraries/runtime/splash.png"
REDIRECT="--noredirect"

####
#
# Test which platform were are
#
####
if [ "$(expr $(uname -s) : 'Darwin')" != 0 ]; then
    PLATFORM="mac"
elif [ "$(expr $(uname -s) : '.*CYGWIN.*')" != 0 ]; then
    PLATFORM="win"
elif [ "$(expr $(uname -s) : '.*MINGW.*')" != 0 ]; then
    PLATFORM="win"
else
    echo "Linux / Unix support untested."
    PLATFORM="linux"
fi



####
#
# Test if we run from a wrapper (e.g., Platypus wrapper, need to go 3x up)
#
####
if [ "$(expr "$BASEDIR" : '.*Contents/Resources.*')" != 0 ]; then
    unset SPLASH
    BASEDIR="$BASEDIR/../../../"
    WRAPPED_WITH_CONSOLE=true
fi


####
#
# Check if there is a user supplied JRE
#
####
if [ -d "$BASEDIR/jre" ]; then
    JAVA="$BASEDIR/jre/bin/java"
fi


####
#
# Check if we should run the default script or if arguments were given
#
####
if [ $# -eq 0 ]; then
    DEFAULT_SCRIPT="$BASEDIR/$DEFAULT_SCRIPT"

    if [ ! -f "$DEFAULT_SCRIPT" ];
    then
        echo "No script given and no default script present. Doing nothing."
        exit
    else
        echo "No script supplied, running default."
    fi
else
    DEFAULT_SCRIPT=$1

    if [ ! -f "$DEFAULT_SCRIPT" ];
    then
        echo "The script you supplied does not exist. Doing nothing."
        exit
    fi
fi


####
#
# Check if we are running in a terminal or not
#
####
if [ -t 2 ]; then
    # In case we have a terminal connected
    REDIRECT=--noredirect
else
    # Or we don't ... In that case, redirect stdout / stderr, however
    # we only do this when we are not actually wrapped with a console.
    if $WRAPPED_WITH_CONSOLE; then
        REDIRECT=--noredirect
    else
        REDIRECT=--redirect
    fi
fi


####
#
# DJ, spin that!
#
####
if [ -f "$JAVA" ]; then
    # I have to admit, the -Xmixed move is somewhat of a hack ...
    "$JAVA" "${SPLASH:--Xmixed}" $JVM_ARGS -jar "$BASEDIR/processing-py.jar" $REDIRECT "$DEFAULT_SCRIPT"
else
    echo "ERROR: Java not found!"
fi
