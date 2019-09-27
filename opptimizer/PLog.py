#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak
import os

class PLog:
    def __init__(self, name, path = None):
        self.name = name
        self.path = None
        self.active = False
        self.logFile = None
        
        self.setActive(True)
        if (path != None):
            self.setPath(path)
        return
    
    def setPath(self, path):
        self.path = path
        if (path == None and self.logFile != None):
            print("PLog.setPath() ERR: path cannot be None foe opened log("
                  + self.name + "):" + self.path)
        else:
            self.path = path
    
    def getPath(self):
        return self.path
    
    def setActive(self, active):
        self.active = active
    
    def isActive(self):
        return self.active
    
    def open(self, append = False):
        if (self.path != None):
            if append:
                mode = 'a'
            else:
                mode = 'w'
                
            self.logFile = open(self.path, mode)
        else:
            print("PLog.open() ERR: no path specified for log " + self.name)
            
    def isOpened(self):
        return self.logFile != None 
    
    def isEmpty(self):
        result = True
        if self.isOpened():
            if os.path.getsize(self.path) > 0:
                result = False
        return result 
        
    
    def close(self):
        if self.logFile != None:
            self.logFile.close()
            self.logFile = None
                        
    def dbg(self, object_to_write, flush = False):
        
        if self.isActive():
            print(object_to_write)
            if self.logFile != None:
                self.logFile.write(object_to_write)
                if flush:
                    self.logFile.flush()

    def dbgl(self, object_to_write, flush = False):
        self.dbg(object_to_write, flush)
        print ("")
        if self.logFile != None:
            self.logFile.write('\n')
            if flush:
                self.logFile.flush()
           
