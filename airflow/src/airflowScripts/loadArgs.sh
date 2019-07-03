#!/bin/bash

################################################################################
#                                                                              #
# File Name   : loadArgs.sh                                                    #
# Description : Script to dynamically load args with -- as variables           #
# Date        : 2018-06-26                                                     #
# Version     : 1.0                                                            #
#                                                                              #
################################################################################


while test $# -gt 0; do
  case $1 in
    -h|--help)
      usage
      break
      ;;
    --*)
      # if we have a value and is not an argument (doesn't start with -)
      if [[ $2 ]] && ! [[ $2 == -* ]]; then
        export var_name=`echo $1 | sed -e 's/\-//g'`
        export $var_name="$2"
        # shift the var value
        shift
      else
        # shift the argument
        shift
      fi
      ;;
    *)
      #shift argument
      shift
      ;;
  esac
done
