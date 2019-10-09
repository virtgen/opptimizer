#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak
import os
import shutil
import csv
import glob
from .putils import *
from .pcons import *
from .PObject import *

class PPath(PObject):
        def __init__(self, path = None, name = "PPath", parent=None,
                    prefix=None, postfix=None, basename=False, noext=False):
            PObject.__init__(self, name)
            
            if path != None:
                if basename:
                    path= self.getBasename(path)
                if noext:
                    path = path.split('.')[0]
                if prefix != None:
                    path = prefix + path 
                if postfix != None:
                    path = path + postfix
                if parent != None:
                    path = parent + P_DIR_SEP + path
                
            
            self.path = path
            self.file = None
            self.csvreader = None
            self.csvwriter = None
    
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
            
        def getBasename(self, path=None):
            result = None
            pathToReturn = None
                
            if (path != None):
                pathToReturn = path
            else:
                pathToReturn = self.getPath()
                
            if pathToReturn != None:
                result = os.path.basename(pathToReturn)
            else:
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").getBasename: trying to get basename from empty path")
            return result
        
        #Create dir if given path not exists      
        def createDirIfNone(self):
            if self.path != None:
                if (not os.path.isdir(self.path)):
                    self.createDir()
            else:
                oppdbg(ERROR_KEY + ':PPath(' + self.name  + ").createDirIfNone(): path is None \n")
        
        # Creates directory for this path even if exists or is not empty.
        # Removes all content if existing directory is not empty.
        def createDirWithCleaning(self):
            
            if (os.path.isdir(self.path)):
                shutil.rmtree(self.path)
            self.createDir()
 
        # Returns new PPath object with the same attributes
        def clone(self):
            result = None
            if self.getPath() != None:
                result = PPath(self.getPath(), self.name)
            return result
               
        # Returns new PPath object with path to base directory
        def cloneDir(self):
            result = None
            if self.getPath() != None:
                result = PPath(os.path.dirname(self.getPath()), self.name)
            return result
                   
        def open(self, mode = 'r', newLineParam = None):
            result = True
            if (self.path != None):
                #if append:
                #    mode = 'a'
                #else:
                #    mode = 'w'
                if (newLineParam != None):
                    self.file = open(self.path, mode, newline = newLineParam)
                else:
                    self.file = open(self.path, mode)
                    
            else:
                result = False
                oppdbg(ERROR_KEY + ':PPath(' + self.name  + ").open(): no path specified for file \n")
            
            return result
                
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
            

        
        def openCSV(self, mode = 'r', delimiterParam = ' '):
            
            result = None
            if (self.open(mode, '') == True):
                if (self.file != None):
                    if (mode == 'r'):
                        self.csvreader = csv.reader(self.file, delimiter=delimiterParam, quotechar='|')
                        result = self.csvreader
                    elif (mode == 'w' or mode == 'a'):
                        self.csvwriter = csv.writer(self.file, delimiter=delimiterParam,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        result = self.csvwriter
                    else:
                        oppdbg(ERROR_KEY + ':PPath(' + self.getName() + ':' + self.getPath()  
                              + ").openCSV(): mode unrecognized:" + str(mode) + " \n")
                else:
                    oppdbg(ERROR_KEY + ':PPath(' + self.getName() + ':' + self.getPath()  
                              + ").openCSV(): NULL file handler:" + str(mode) + " \n")
                    
            return result
        
        def getCSVReader(self):
            return self.csvreader

        def getCSVWriter(self):
            return self.csvwriter
        
        def close(self):
            result = True
            
            if self.file != None:
                self.file.close()
                self.file = None
                self.csvreader = None
                self.csvwriter = None
            else:
                result = False
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").close(try to close the closed file \n")
            
            return result
        
        def readLines(self):
            if self.isOpened():
                return self.file.readlines()
        
        # Returns list of files in directory
        def getDirFiles(self, prefix = '', postfix = '', key=None, reverse=False): # sortKeyParam = None, reversParam = False):
            result = None

            if (self.isDir() and self.exists()): 
                filePattern = prefix + '*' + postfix
                dir_files = sorted(glob.glob(self.getPath() + P_DIR_SEP + filePattern), key=key, reverse=reverse) #, key=sortKeyForFiles, reverse=ctx_train_reverse)
                result = dir_files
            else:
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").getDirFiles: path not exists or is not directory:" + self.getPath() + " \n")

            return result
        
    #defines the key from filename used for loading files in proper order 
        def sortByPaths(x):
            return x

        
        