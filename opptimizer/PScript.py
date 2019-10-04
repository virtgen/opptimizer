#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from .opp import *
from .pcons import *
from .PLog import *

class PScript(PObject):
    def __init__(self, name=""):
        PObject.__init__(self, "script", name)
        
    def getContext(self, argv):
        context = ''   
   
        modDirOppStr = None
        modulesOppStr = None
        outOppStr = None
        
        if len(argv) > 1:
            for arg in argv:
                if oppkey(arg) == 'dmods':
                    modDirOppStr = arg
                elif oppkey(arg) == 'modules':
                    modulesOppStr = arg
                elif oppkey(arg) == 'rootDir':
                    outOppStr = arg
                    
        if modDirOppStr != None: 
            context = oppsum(context, modDirOppStr)
            
        if modulesOppStr != None: 
            context = oppsum(context, modulesOppStr)
            
        if outOppStr != None: 
            context = oppsum(context, outOppStr)               
            
        return context