#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from .PObject import *
from .PLog import *

class PExecutable(PObject):
    def __init__(self, name, context=''):
        PObject.__init__(self, name) 
        self.context = context
        self.logFileName = None
        self.logFile = None

    def getContext(self):
        return self.context

    def setContext(self, context):
        self.context = context
        
    def dbg(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbg(txt, dbgLevel)

    def dbgl(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbgl(txt, dbgLevel)

    # Prints WARNING log (as string)
    def wrn(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.wrn(txt, dbgLevel)
                
    def wrnl(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.wrnl(txt, dbgLevel)
            
    # Prints ERROR log (as string)
    def err(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.err(txt, dbgLevel)
                    
    def errl(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.errl(txt, dbgLevel)

    def dbgopen(self):
        if (self.logFileName != None):
            self.logFile = PLog(self.name, self.getLogFileName())
            self.logFile.openLog(True)
        else:
            print("PModule.dbgopen() ERR: log not initialized due to lack of path")

    def dbgclose(self):
        if self.logFile != None:
            self.logFile.close()
            
    def getLog(self):
        return self.logFile
    
    def setLogFileName(self, logFileName):
        self.logFileName = logFileName
            
    def getLogFileName(self):
        return self.logFileName
