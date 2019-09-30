#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from PPath import *
from putils import *

DBG_NODEBUG_LEVEL = 0
DBG_LOW_LEVEL = 1
DBG_MEDIUM_LEVEL = 2
DBG_HIGH_LEVEL = 3

class PLog(PPath):
    def __init__(self, name = "", path = None, oppKey = None):
        PPath.__init__(self, path, oppKey, name)
        self.active = False
        self.LEVEL = DBG_LOW_LEVEL
        self.flush = False
        self.addPrefix = True  #flag if prefix ([self.name]) should be added to log
        
        
        self.setActive(True)
        if (path != None):
            self.setPath(path)
        return
    
    def setFlush(self, flush=True):
        self.flush = flush
    
    def getFlush(self):
        return self.flush
    
    def setActive(self, active):
        self.active = active
    
    def isActive(self):
        return self.active
    
    def getPrefix(self):
        if self.addPrefix:
            return '[' + self.name + ']'
    
    # Prints regular log
    def dbg(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        if self.isActive() and dbgLevel >= self.LEVEL:
            textToWrite = self.getPrefix() + object_to_write
            oppdbg(textToWrite)
            if self.isOpened():
                self.write(textToWrite, self.flush)
                
    def dbgl(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        object_to_write += '\n'
        self.dbg(object_to_write, dbgLevel)

    # Prints WARNING log (as string)
    def wrn(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        if self.isActive() and dbgLevel >= self.LEVEL:
            textToWrite = WARN_KEY + self.getPrefix() + ':' + object_to_write 
            oppdbg(textToWrite)
            if self.isOpened():
                self.write(textToWrite, self.flush)
                
    def wrnl(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        object_to_write += '\n'
        self.wrn(object_to_write, dbgLevel)
    
    # Prints ERROR log (as string)
    def err(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        if self.isActive() and dbgLevel >= self.LEVEL:
            textToWrite = ERROR_KEY + self.getPrefix() + ':' + object_to_write 
            oppdbg(textToWrite)
            if self.isOpened():
                self.write(textToWrite, self.flush)
                
    def errl(self, object_to_write, dbgLevel=DBG_LOW_LEVEL):
        object_to_write += '\n'
        self.err(object_to_write, dbgLevel)
           
