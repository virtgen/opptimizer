#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

##########################################
#  File template automatically generated #
##########################################

import sys
sys.path.append(".")
from opptimizer import *

# Your own script class extension 
# You can use it in getModule() function instead of PModule
class YourScriptClass(PScript):
    def __init__(self, name=""):
        PScript.__init__(self,name)
        return

    def execute(self, argv):
    
        print("Execution in script")
        print("argv:" + str(argv))
    
        ps = PScript()
        ps.getContext(argv)
       
        context = ps.getContext(argv)            
        
        executor = PExecutor()
        
        params = ''
        test = executor.execute(P_KEY_TEST, context, params, opprange('sampleParam', 0, 1, 2))
        print ("test script: final result from " + str(test.getExecDir()))
    
# If you override script class (eg. YourScriptClass) 
# you must override this method and create your class object
# instead of PScript
def getScript(scriptName):
    script = YourScriptClass(scriptName)
    return script

def main(argv):

    script = getScript("Noname")
    script.execute(argv)
    #your code
    #...

if __name__ == "__main__":
    sys.exit(main(sys.argv))