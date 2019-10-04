#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from .PObject import *
from .PLog import *

class PExecutable(PObject):
    def __init__(self, name):
        PObject.__init__(self, name) 
        self.logFileName = None
        self.logFile = None

    def dbg(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbg(txt, dbgLevel)

    def dbgl(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbgl(txt, dbgLevel)

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
