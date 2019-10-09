#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

import subprocess
from .opp import *
from .pcons import *
from .PLog import *
from .PExecutable import *

class PModule(PExecutable):
    def __init__(self, name=""):
        PExecutable.__init__(self, name)
        self.name = name
        self.resultFilePath = None
        self.exec_result = None
        self.resultFile = None
        self.skipExe = False
        self.writeTestNameToResult = True
        return
    
    def init(self, testName, context):
        self.setContext(context)
        if testName == None:
            testName = 'test'
            
        testExecDir = oppval('testExecDir', self.getContext())
        if testExecDir != None:
            self.setLogFileName(testExecDir + P_DIR_SEP + testName + '-log.txt')
        else:
            print("PModule.init() ERR: log not initialized due to lack of exec dir")
        
        resultFilePath = oppval('resultFilePath', self.getContext())
        self.setResultFilePath(resultFilePath)
        
        #self.dbgl("Init module " + self.name + ", logFilename:" + self.getLogFileName())
        #self.dbgl("Init module " + self.name + " resultFilePath:" + self.getResultFilePath())

    def getName(self):
        return self.name
    
    def setSkipExe(self, val):
        self.skipExe = val

    
    #####  FILES (log/data)  INTERFACE  ################

    def resultFileOpen(self):
        if (self.getResultFilePath() != None):
            self.resultFile = PPath(self.getResultFilePath(), "ResultFile")
            self.resultFile.open('a')
        else:
            print("PModule.resulFiletOpen() ERR: log not initialized due to lack of path")

    def resultFileClose(self):
        if self.resultFile != None:
            self.resultFile.close()

    def writeToResultFile(self, resultStr):
        if self.resultFile != None:
            self.resultFile.write(resultStr)


    def setResultFilePath(self, resultFilePath):
        self.resultFilePath = resultFilePath
            
    def getResultFilePath(self):
        return self.resultFilePath
            

    
    #####  END of FILES (log/data)  INTERFACE  ################
    
    #Returns a path to result from optimization for given input file
    # @flat defines if test name prefix should be added
    # @noext cuts extension form @inFilePath before processing
    def getFileResPath(self, inFilePath, testName='', testExecDir='',
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
            
        result = PPath(inFilePath, basename=True, noext=True, prefix=testPrefix,
                        postfix=reskey+resext, parent=testExecDir)
        return result
    
    
    def setExecresult(self, execResult):
        self.exec_result = execResult
        
    def getExecResult(self):
        return self.exec_result
    
    # Executes module
    # Returns tokenData (custom global data for tests execution) 
    def execute(self, params, tokenData = None):
        
        testName = oppval(P_KEY_TESTNAME, params)
        self.dbgopen()
        
        executionParams = oppmodify(self.getContext(), params)
        if self.getLogFileName() != None:
            logFileParam = self.getLogFileName()
        else:
            logFileParam = "" 
            
        executionParams = oppmodify(executionParams, opp("logFile", logFileParam))
        
        #execDir = oppval('testExecDir', self.context)
        #if execDir != None:
        #    executionParams = oppmodify(executionParams, opp("resultFile", execDir + P_DIR_SEP + DP_RESULT_FILENAME))
        
        self.dbgl(self.name + ".execute().context: " + self.getContext())
        self.dbgl(self.name + ".execute().params: " + params)
        
        if self.writeTestNameToResult:
            self.resultFileOpen()
            if (self.resultFile != None and not self.resultFile.isEmpty()):
                self.writeToResultFile('\n')
                
            self.writeToResultFile(opp('testName', testName) + ';')
            self.resultFileClose();
        
        
        if (not self.skipExe):
            self.dbgclose()
            p = subprocess.Popen(["./runapp.sh", self.name, executionParams], cwd="../../modules/" + self.name)
            print("wait")
            p.wait()
            self.setExecresult(p.returncode)
            self.dbgopen()
        else:
            self.dbgl("Native execution skipped for module " + self.name)
            
        
        
        self.dbgl("module " + self.name +  " finished with return " + str(self.getExecResult()))
        self.dbgclose()
        
        return tokenData
        
    
    
