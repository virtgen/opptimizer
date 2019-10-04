#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

##########################################
#  File template automatically generated #
##########################################

import sys
sys.path.append("../..")
from opptimizer import *

# Your own module class extension 
# You can use it in getModule() function instead of PModule
#class YourModuleClass(PModulePy):
#    def __init__(self, name=""):
#        dpPyModule.__init__(self,name)
#        return

# If you override module class (eg. YourModuleClass) 
# you must override this method and create your class object
# instead of PModulePy
def getModule(moduleName):
    module = PModulePy(moduleName)
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