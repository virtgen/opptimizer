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
    def __init__(self):
        PScript.__init__(self)
        return

    def execute(self, argv):
        
        self.dbgopen()
        PScript.execute(self, argv)  
        self.dbgl("Execution in script")
        self.dbgl("argv:" + str(argv))
                
        executor = PExecutor()     
        params = ''
        test = executor.execute(P_KEY_TEST, self.getContext(), params, opprange('sampleParam', 0, 1, 2))
        self.dbgl("test script: final result from " + str(test.getExecDir()))
        self.dbgclose()

# If you override script class (eg. YourScriptClass) 
# you must override this method and create your class object
# instead of PScript
def getScript():
    script = YourScriptClass()
    return script

def main(argv):

    script = getScript()
    script.init(argv)
    script.execute(argv)
    #your code
    #...

if __name__ == "__main__":
    sys.exit(main(sys.argv))