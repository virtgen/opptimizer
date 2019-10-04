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
   
        cfgFileOppStr = None
        modDirOppStr = None
        modulesOppStr = None
        outOppStr = None
        scriptNameOppStr = None
        
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
                elif oppkey(arg) == 'script':
                    scriptNameOppStr = arg

        if cfgFileOppStr != None:
            context = oppmodify(context, cfgFileOppStr)
            cfgContext = self.parseCfgFile(cfgFileOppStr)
            if (cfgContext != ''):
                context = oppsum(context, cfgContext) 
                
        if scriptNameOppStr != None: 
            context = oppmodify(context, scriptNameOppStr)
            
        if modDirOppStr != None: 
            context = oppmodify(context, modDirOppStr)
            
        if modulesOppStr != None: 
            context = oppmodify(context, modulesOppStr)
            
        if outOppStr != None: 
            context = oppmodify(context, outOppStr)               
            
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
        