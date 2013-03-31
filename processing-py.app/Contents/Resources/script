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
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLATFORM='unknown'


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
    BASEDIR="$BASEDIR/../../../"
fi


####
#
# Check if there is a user supplied JRE
#
####
if [ -d "./JREs/jre7.$PLATFORM" ]; then   
    JAVA="$BASEDIR/JREs/jre7.$PLATFORM/bin/java"
fi


####
#
# Check if we should run the default script or if arguments were given
#
####
if [ $# -eq 0 ]; then
    DEFAULT_SCRIPT="$BASEDIR/$DEFAULT_SCRIPT"
    echo "No script supplied, running default."
else 
    DEFAULT_SCRIPT=$1
fi 


####
#
# DJ, spin that shit!
#
####
if [ -f "$JAVA" ]; then 
    "$JAVA" $JVM_ARGS -jar "$BASEDIR/processing-py.jar" "$DEFAULT_SCRIPT"
else 
    echo "ERROR: Java not found!"    
fi
