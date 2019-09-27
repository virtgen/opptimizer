#!/bin/bash

##########################################
#  DP Optimization framework             #
#  File template automatically generated #
##########################################

ROOT="../.."
source $ROOT/config.sh
source $MAKE_DIR/config.mk

echo Module app $1 start with params["${@:2}"] 

./$PLATFORM/$1 "${@:2}"
