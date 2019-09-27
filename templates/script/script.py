#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

##########################################
#  File template automatically generated #
##########################################

import sys
sys.path.append("../..")
from opptimizer import *
#from modules.[your_module_name] import *


def main(argv):

   #your code
   #...
   print "Hello world from new script"
   executor = PExecutor()
   
   context = opp("rootDir", "../../_out", "modules","")
   params = ''
   test = executor.execute(P_KEY_TEST, context, params, opprange('sampleParam', 0, 1, 2))
   print ("test script: final result from " + str(test.getExecDir()))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
