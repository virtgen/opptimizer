#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from .opp import *
from .pcons import *
from .PLog import *

class PScript(PObject):
    def __init__(self, name=""):
        PObject.__init__(self, name)
        
    def getContext(self, argv):
        context = ''   
   
        cfgFileOppStr = None
        modDirOppStr = None
        modulesOppStr = None
        outOppStr = None
        
        if len(argv) > 1:
            for arg in argv:
                if oppkey(arg) == 'dcfg':
                    cfgFileOppStr = arg
                elif oppkey(arg) == 'dmods':
                    modDirOppStr = arg
                elif oppkey(arg) == 'modules':
                    modulesOppStr = arg
                elif oppkey(arg) == 'rootDir':
                    outOppStr = arg

        if cfgFileOppStr != None:
            context = oppsum(context, cfgFileOppStr)
            cfgContext = self.parseCfgFile(cfgFileOppStr)
            if (cfgContext != ''):
                context = oppsum(context, cfgContext)        
        
        if modDirOppStr != None: 
            context = oppsum(context, modDirOppStr)
            
        if modulesOppStr != None: 
            context = oppsum(context, modulesOppStr)
            
        if outOppStr != None: 
            context = oppsum(context, outOppStr)               
            
        return context
    
    def parseCfgFile(self, cfgFileOpp):
        context = ''
        
        print("parseCfgFile:" + cfgFileOpp)
        
        cfgPath = oppval("dcfg", cfgFileOpp)
    
        
        if (cfgPath != None):
            
            cfg = PPath(cfgPath)
            
            if cfg.exists():
                
                cfg.open()
                content = cfg.readLines()
                
                for item in content:
                    print('item'+item)
                    item = item.split('\n')[0]
                    #TODO: add check if line is correct OPP string
                    context = oppsum(context, item)
                    
                cfg.close()
            else:
                print('WARN parseCfgFile: path not exists:' + cfg.getPath())
        else:
            print('WARN parseCfgFile: path not exists:' + cfg.getPath())
            
        print("context from cfg:" + context)   
        
        return context 
        