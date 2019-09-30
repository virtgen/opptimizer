#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak
import os
import shutil
from putils import *
from pcons import *
from PObject import *

class PPath(PObject):
        def __init__(self, path = None, oppKey = None, name = ""):
            PObject.__init__(self, oppKey, name)
            self.path = path
            self.file = None
    
        def setPath(self, path):
            if (self.file != None):
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").setPath: path cannot be changed for opened log (operation not done), existing path:" 
                        + self.path + ", requested path " + path)
            else:
                self.path = path 
    
        def getPath(self):
            return self.path
        
        def isDir(self):
            return os.path.isdir(self.path)
        
        def isFile(self):
            return os.path.isfile(self.path)
        
        def exists(self):
            return os.path.exists(self.path)


        def createDir(self):
            os.mkdir(self.path)
        
        #Create dir if given path not exists      
        def createDirIfNone(self):
            if (not os.path.isdir(self.path)):
                self.createDir()
        
        # Creates directory for this path even if exists or is not empty.
        # Removes all content if existing directory is not empty.
        def createDirWithCleaning(self):
            
            if (os.path.isdir(self.path)):
                shutil.rmtree(self.path)
            self.createDir()
            
        def open(self, append = False):
            if (self.path != None):
                if append:
                    mode = 'a'
                else:
                    mode = 'w'
                    
                self.file = open(self.path, mode)
            else:
                oppdbg(ERROR_KEY + ':PPath(' + self.name  + ").open(): no path specified for file \n")
                
        def isOpened(self):
            return self.file != None 
        
        def isEmpty(self):
            result = True
            if self.isOpened():
                if os.path.getsize(self.path) > 0:
                    result = False
            return result 
        
        def write(self, object_to_write, flush = False):
            if self.file != None:
                self.file.write(object_to_write)
                if flush:
                    self.file.flush()
            else:
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").write(): file not open, path:"
                       + self.path + "\n")
        # Writes to file as new line
        def writeAsAppendLine(self, object_to_write, flush = False):
            if not self.isEmpty():
                self.write('\n')
            self.write(object_to_write, flush)    
                
        def close(self):
            if self.file != None:
                self.file.close()
                self.file = None
            else:
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").close(try to close the closed file \n")