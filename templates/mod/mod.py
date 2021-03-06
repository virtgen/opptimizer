#!/usr/bin/env python

##########################################
#  File template automatically generated #
##########################################

import sys
sys.path.append("../..")
from opptimizer import *

# Your own module class extension 
# You can use it in getModule() function instead of PModule
class YourModuleClass(PModulePy):
    def __init__(self, name=""):
        PModulePy.__init__(self,name)
        return
    
 #   @override(PModule)
    def execute(self, params, tokenData = None):

        tokenData = PModulePy.execute(self, params)

        self.dbgopen()
        self.dbgl("will be writting to result:")
        
        self.resultFileOpen()
        self.writeToResultFile(opp('precision', '0.75'))
        self.resultFileClose()
        
        self.dbgclose()
    
        return tokenData
    
    def onFileProcess(self, fileToProcess, params,tokenData):
        # add your code for single data file here
        return tokenData

# If you override module class (eg. YourModuleClass) 
# you must override this method and create your class object
# instead of PModulePy
def getModule(moduleName):
    module = YourModuleClass(moduleName)
    return module




def main(argv):
    
    name = ''
    if (len(argv) > 1):
        name = argv[1]
        
    context = ''
    if (len(argv) > 2):
        context = argv[2]

    params = ''
    if (len(argv) > 3):
        params = argv[3]
        
    print ("Run module " + name + ", context:" + context + " params:" + params)
    
    module = PModulePy(name)
    module.init("test", context)
    module.execute(params)

if __name__ == "__main__":
    sys.exit(main(sys.argv))