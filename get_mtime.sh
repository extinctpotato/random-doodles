#!/bin/bash

##########################################################
# This script will print modification times              #
# of files of all files and directories                  #
# within the path provided as first positional argument. #
##########################################################

find $1 -print0 | xargs -0 stat --printf='%n\t@%Y\n' | sed "s/$1\///g"
