#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

##########################################
#  File template automatically generated #
##########################################

import sys
sys.path.append(".")
from opptimizer import *

#from modules.[your_module_name] import *

def execute(argv):
    
    print("Hello world from new script")
    print("argv:" + str(argv))

    ps = PScript()
    ps.getContext(argv)
   
    context = ps.getContext(argv)            
    
    executor = PExecutor()
    
    params = ''
    test = executor.execute(P_KEY_TEST, context, params, opprange('sampleParam', 0, 1, 2))
    print ("test script: final result from " + str(test.getExecDir()))

def main(argv):

    execute(argv)
    #your code
    #...

if __name__ == "__main__":
    sys.exit(main(sys.argv))