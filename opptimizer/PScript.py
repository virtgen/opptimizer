#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from .opp import *
from .pcons import *
from .PLog import *
from .PExecutable import *
from opptimizer.opp import oppmodify

class PScript(PExecutable):
    def __init__(self, name=""):
        PExecutable.__init__(self, name)
    
    def init(self, argv):
        context = self.parseArgsForContext(argv) 
        self.setContext(oppmodify(self.getContext(), context))
        
        scriptName = oppval('script', self.context)
        if scriptName != None:
            self.setName(scriptName)
        
        print('script.init, context:' + self.getContext())
        outDir = oppval('dout', self.context)
        
        PPath(outDir).createDirIfNone()
        if outDir != None:
            self.setLogFileName(outDir + P_DIR_SEP + P_SUMMARY_FILENAME)
        else:
            print("PModule.init() ERR: log not initialized due to lack of out dir")  

    # Should be overriden
    def execute(self, argv):    
        return 
    
    def parseArgsForContext(self, argv):
        context = ''   
        
        if len(argv) > 1:
            for arg in argv:
                if oppkey(arg) != None:
                    context = oppmodify(context, arg)

        
        cfgFile = oppval('dcfg', context)
        if cfgFile != None:
            cfgContext = self.parseCfgFile(cfgFile)
            if (cfgContext != ''):
                context = oppsum(context, cfgContext) 
            
        return context
    
    def parseCfgFile(self, cfgFile):
        context = ''
        
        print("parseCfgFile:" + cfgFile)
    
        if (cfgFile != None):
            
            cfg = PPath(cfgFile)
            
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
        