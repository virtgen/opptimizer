#!/usr/bin/env python

# opPtimizer: optimization framework for AI  
# Copyright (c) 2019 Artur Bak. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pathlib import Path
import shutil
import csv
import glob
from .putils import *
from .pcons import *
from .PObject import *

class PPath(PObject):
        ''' Utility class for I/O operations (particuary filesystem) during pipeline execution.  '''

        def __init__(self, refPath = None, name = "PPath", parent=None,
                    prefix=None, postfix=None, basename=False, noext=False, isdirtocreate=False, deepParent = None):
            '''
                dedeepParent: is not None, the number causes change of relPath to its deep parent eg. '../..' for deepParent=2
            '''
            PObject.__init__(self, name)
            
            if (isinstance(refPath, PPath)):
                path = refPath.getPath()
            else:
                path = refPath

            if deepParent:
                if path and isinstance(deepParent,int):
                    path = PPath(path).getDeepParent(deepParent)

            if path != None:
                if basename:
                    path= self.getBasename(path)
                if noext:
                    #path = path.split('.')[0] ## it is incorreect if there dots in basename
                    path = os.path.splitext(path)[0]
                if prefix != None:
                    path = prefix + path 
                if postfix != None:
                    path = path + postfix
                if parent != None:
                    if (isinstance(parent, PPath)):
                        parent = parent.getPath()
                    path = parent + P_DIR_SEP + path
                          
            self._path = path
            self._file = None
            self.csvreader = None
            self.csvwriter = None

            if isdirtocreate:
                self.createDir()

        # path property
        @property
        def path(self):
            return self._path
        
        @path.setter
        def path(self, path):
            # if (not path):
            #     raise ValueError("Value not allowed")
            self._path = path

        # file property
        def set_file(self, _file):
            self._file = _file

        def get_file(self):
            return self._file

        def del_file(self):
            del self._file
        
        file = property(get_file, set_file, del_file) 

        def setPath(self, path):
            if (self._file != None):
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").setPath: path cannot be changed for opened log (operation not done), existing path:" 
                        + self.path + ", requested path " + path)
            else:
                self.path = path 
    
        def getPath(self):
            """
            Returns the path.
            """
            return self.path
        
        # Adds part of path to current path
        def add(self, pathToAdd):
            pathToAdd = P_DIR_SEP + pathToAdd if (pathToAdd and pathToAdd != '') else ''
            self.setPath(self.getPath() + pathToAdd)
            return self

        def isDir(self):
            return os.path.isdir(self.path)
        
        def isFile(self):
            return os.path.isfile(self.path)
        
        def exists(self):
            result = os.path.exists(self.path) if self.path else False
            return result


        def createDir(self):
            if self.path and not self.exists():
                os.makedirs(self.path)
            
        def getBasename(self, path=None, change_extension = None):
            result = None
            pathToReturn = None
                
            if (path != None):
                pathToReturn = path
            else:
                pathToReturn = self.getPath()
                
            if pathToReturn != None:
                result = os.path.basename(pathToReturn)
                if change_extension != None:
                    result = str(Path(result).with_suffix(change_extension))
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
        
        # Removes dir
        def removeDir(self):
            if (os.path.isdir(self.path)):
                shutil.rmtree(self.path)

                
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
            return self._file != None
        
        def isEmpty(self):
            result = True
            if self.isOpened():
                if os.path.getsize(self.path) > 0:
                    result = False
            return result 
            
         
        def write(self, object_to_write, flush = False):
            if self._file != None:
                self._file.write(object_to_write)
                if flush:
                    self._file.flush()
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
                if (self._file != None):
                    if (mode == 'r'):
                        self.csvreader = csv.reader(self._file, delimiter=delimiterParam, quotechar='|')
                        result = self.csvreader
                    elif (mode == 'w' or mode == 'a'):
                        self.csvwriter = csv.writer(self._file, delimiter=delimiterParam,
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
            
            if self._file != None:
                self._file.close()
                self._file = None
                self.csvreader = None
                self.csvwriter = None
            else:
                result = False
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").close(try to close the closed file \n")
            
            return result
        
        def readLines(self, join_lines = False, strip_newlines = False, join_sep = ''):
            if self.isOpened():
                lines = self._file.readlines()
                if join_lines:
                    lines = join_sep.join(lines)        
                    if strip_newlines:
                        lines = lines.replace('\n','')
                return lines
        
        # Returns list of files in directory
        def getDirFiles(self, pattern='*', prefix = '', postfix = '', key=None, reverse=False): # sortKeyParam = None, reversParam = False):
            result = None

            pattern = pattern if pattern else '*'
            prefix = prefix if prefix else ''
            postfix = postfix if postfix else ''
             
            if (self.exists() and self.isDir()): 
                filePattern = prefix + pattern + postfix
                dir_files = sorted(glob.glob(self.getPath() + P_DIR_SEP + filePattern), key=key, reverse=reverse) #, key=sortKeyForFiles, reverse=ctx_train_reverse)
                result = dir_files
            else:
                oppdbg(WARN_KEY + ':PPath(' + self.name  + ").getDirFiles: path not exists or is not directory:" + self.getPath() + " \n")

            return result

        #Returns a path to result from optimization for given input file
        # @flat defines if test name prefix should be added
        # @noext cuts extension form @inFilePath before processing
        # Example of use: PPath(<pathStr>).getFileResPath(..)
        def getFileResPath(self, testName='', testExecDir='',
                            noext=True, reskey=None, resext=None, flat=False):
            result = None
            testPrefix=''
            
            if flat:
                testPrefix = testName + '-'
            
            if reskey != None:
                reskey = '-' + reskey
            else:
                reskey = ''
            
            if resext != None:
                resext = '.' + resext
            else:
                resext = ''
                
            result = PPath(self, basename=True, noext=True, prefix=testPrefix,
                            postfix=reskey+resext, parent=testExecDir)
            return result
        
    #defines the key from filename used for loading files in proper order 
        def sortByPaths(x):
            return x
        
        def parseCfgFile(self):
            context = ''
    
            #oppdbg("ppath::parseCfgFile:" + self.getPath())
          
            if self.exists():
                
                self.open()
                content = self.readLines()
                
                for item in content:
                    #print('item'+item)
                    item = item.split('\n')[0]
                    #TODO: add check if line is correct OPP string
                    context = oppsum(context, item)
                    
                self.close()
            else:
                oppdbg(WARN_KEY + 'ppath::parseCfgFile: path not exists:' + self.getPath())

                
            #oppdbg("ppath::parseCfgFile: context from cfg:" + context)   
            
            return context 

        def context(self, context=''):
            ''' Read context from this PPath file if contains one
                This context from file is then merged with context param'''

            #context = oppmodify(context, 'dcfg=' + self.getPath())
            
            if self.getPath() != None:
                cfgContext = self.parseCfgFile()
                if (cfgContext != ''):
                    context = oppsum(context, cfgContext) 

            return context
        
        def getDeepParent(self, parentLevel = 2, default = None):
            ''' Returns root directory for file assuming parenting depth like '../..' for level=2'''
            path = default
            if self.path:
                parentDeep = os.path.sep.join(['..'] * parentLevel)
                path = Path(self.path) / parentDeep
                path = os.path.normpath(path)
            return path
        
        def getParent(self):
            ''' Resturn direct parent '''
            return self.getDeepParent(1)
        