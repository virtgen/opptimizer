#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak


from .PModule import *
from .PLog import *
from .opp import *
from .pcons import *

class PModulePy(PModule):
    def __init__(self, name=""):
        PModule.__init__(self,name)
        self.setSkipExe(True)
        
        return
        
 #   @override(PModule)
    def execute(self, params, tokenData = None):
        tokenData = PModule.execute(self, params)
        return tokenData
    
