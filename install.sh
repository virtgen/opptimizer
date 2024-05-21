#!/bin/bash

#  opPtimizer - optimization framework for AI
#  (c) Artur Bak, 2019
#
#   - installator of terminal opPtimizer

ROOT="."
#source install.cfg

if [ "$1" == "mac" ]; then
    echo "MACOS Platform"
    OPP_DIR="/Library"
    BIN_DIR="/usr/local/bin"
elif [ "$1" == "linux" ]; then
    echo "LINUX Platform"
    OPP_DIR="/usr/local/lib"
    BIN_DIR="/usr/local/bin"
else
   echo "Installaton error: no config for platform [$1]"
   exit
fi
   


INSTALL_OPP_DIR_NAME="."

OPP_DEST_DIR_NAME="opptimizer"
OPP_DEST_PATH="$OPP_DIR/$OPP_DEST_DIR_NAME"
OPP_EXE="opp"

function remove {

    echo Trying to uninstall old version of opPtimizer
    if [ -d $OPP_DEST_PATH ]; then
       echo "$OPP_DEST_PATH exists. Removing old version of opPtimizer"
       rm -Rf $OPP_DEST_PATH
    else
        echo "$OPP_DEST_PATH not exists."
    fi

    if [ -L $BIN_DIR/$OPP_EXE ]; then
        echo "Symlink $BIN_DIR/$OPP_EXE exists. Removing old version."
        rm -f $BIN_DIR/$OPP_EXE 
    else
        echo "Symlink $_BIN_DIR/$OPP_EXE not exits."
    fi
    echo Uninstallation completed.

}


###### MAIN ################

VERSION=`cat opptimizer/version.txt`

echo Installing opPtimizer $VERSION

if [ "$2" == "remove" ]; then
    remove
    exit
fi

remove
echo "Creating $OPP_DEST_PATH"
mkdir -p $OPP_DEST_PATH
echo Copying opPtimizer to $OPP_DEST_PATH
cp -r $ROOT/$INSTALL_OPP_DIR_NAME/* $OPP_DEST_PATH


echo Creating symbolic links in $BIN_DIR
ln -s $OPP_DEST_PATH/$OPP_EXE $BIN_DIR/$OPP_EXE

echo Done.