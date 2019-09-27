#!/bin/bash

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak


ROOT="."
source config.sh

echo opPtimizer v1.01
if [ "$1" == "mod" -o "$1" == "script" ]; then
   echo "Mod or script"
   if [ "$1" == "mod" ]; then
      DIR=$MODULES_DIR
   elif [ "$1" == "script" ]; then
      DIR=$SCRIPTS_DIR
   else
      echo "Internal SH error 01 (run.sh)"
   fi

   echo "Dir $DIR"

   if [ ! "$2" == "" ]; then
      if [ -d "$DIR/$2" ]; then
         cd $DIR/$2
         python $2.py $2 $3 $4 
         cd $ROOT
      else
          echo "Error: $2 not found."
      fi
   else
      echo "Error: Exec script name must be given."
   fi
elif [ "$1" == "create" ]; then
   if [ "$2" == "mod" ]; then     
# here you can define template dir depending on module technology (cpp,py,R etc)       
      if [ "$4" == "cpp" ]; then
         TEMPLATE_DIR=$TEMPLATES_DIR/modcpp/
      else
# default technology is py
         TEMPLATE_DIR=$TEMPLATES_DIR/mod/          
      fi

#      TEMPLATE_SH=runmod.sh
      TEMPLATE_PY=mod.py
      TARGET_DIR=$MODULES_DIR/$3
   elif [ "$2" == "script" ]; then
      TEMPLATE_DIR=$TEMPLATES_DIR/script/
 #     TEMPLATE_SH=runscript.sh
      TEMPLATE_PY=script.py
      TARGET_DIR=$SCRIPTS_DIR/$3
   else
       echo "Error: no template $2 found for creation."
       exit
   fi

   echo "Creation of $TARGET_DIR from template $TEMPLATE_DIR:"
   if [ -d $TARGET_DIR ]; then
      echo "$TARGET_DIR exists. Operation skipped.."
   else
      mkdir -p $TARGET_DIR
      cp -r $TEMPLATE_DIR/* $TARGET_DIR
      mv $TARGET_DIR/$TEMPLATE_PY $TARGET_DIR/$3.py

# here you can do additionl actions on target dir depending 
# on module technology (cpp, py, R etc.)
      if [ "$2" == "mod" ]; then
        if [ "$4" == "cpp" ]; then
            mv $TARGET_DIR/mod.cpp $TARGET_DIR/$3.cpp
        fi
      fi
      echo "Done."
   fi


elif [ "$1" == "clean" ]; then
	echo Cleaning temporary files..
	rm -Rf $OUTPUT_DIR
	rm -Rf $EXT_DIR/cpp/_obj
	rm -Rf $MOVIES_DIR/*
        find . -name "*~" -exec rm {} \;
	find . -name "*pyc" -exec rm {} \;
else
  echo Undefined parameter: $1
fi
