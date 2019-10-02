#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

import subprocess
from .opp import *
from .pcons import *
from .PLog import *

class PModule:
    def __init__(self, name=""):
        self.name = name
        self.context = None
        self.resultFilePath = None
        self.exec_result = None
        self.logFileName = None
        self.logFile = None
        self.resultFile = None
        self.skipExe = False
        self.writeTestNameToResult = True
        return
    
    def init(self, testName, context):
        self.context = context
        if testName == None:
            testName = 'test'
            
        testExecDir = oppval('testExecDir', self.context)
        if testExecDir != None:
            self.setLogFileName(testExecDir + P_DIR_SEP + testName + '-log.txt')
        else:
            print("PModule.init() ERR: log not initialized due to lack of exec dir")
        
        resultFilePath = oppval('resultFilePath', context)
        self.setResultFilePath(resultFilePath)
        
        #self.dbgl("Init module " + self.name + ", logFilename:" + self.getLogFileName())
        #self.dbgl("Init module " + self.name + " resultFilePath:" + self.getResultFilePath())

    def getName(self):
        return self.name
    
    def setSkipExe(self, val):
        self.skipExe = val

    
    #####  FILES (log/data)  INTERFACE  ################
    
    def dbg(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbg(txt, dbgLevel)

    def dbgl(self, txt, dbgLevel = 1):
        if self.logFile != None:
            self.logFile.dbgl(txt, dbgLevel)

    def dbgopen(self):
        if (self.logFileName != None):
            self.logFile = PLog(self.name, self.getLogFileName())
            self.logFile.open(True)
        else:
            print("PModule.dbgopen() ERR: log not initialized due to lack of path")

    def dbgclose(self):
        if self.logFile != None:
            self.logFile.close()

    def resultFileOpen(self):
        if (self.getResultFilePath() != None):
            self.resultFile = PPath(self.getResultFilePath(), "ResultFile", 'resultFile')
            self.resultFile.open(True)
        else:
            print("PModule.resulFiletOpen() ERR: log not initialized due to lack of path")

    def resultFileClose(self):
        if self.resultFile != None:
            self.resultFile.close()

    def writeToResultFile(self, resultStr):
        if self.resultFile != None:
            self.resultFile.write(resultStr)


    def setLogFileName(self, logFileName):
        self.logFileName = logFileName
            
    def getLogFileName(self):
        return self.logFileName

    def setResultFilePath(self, resultFilePath):
        self.resultFilePath = resultFilePath
            
    def getResultFilePath(self):
        return self.resultFilePath
            
    def getLog(self):
        return self.logFile
    
    #####  END of FILES (log/data)  INTERFACE  ################
    
    
    
    
    def setExecresult(self, execResult):
        self.exec_result = execResult
        
    def getExecResult(self):
        return self.exec_result
    
    # Executes module
    # Returns tokenData (custom global data for tests execution) 
    def execute(self, params, tokenData = None):
        
        testName = oppval(P_KEY_TESTNAME, params)
        self.dbgopen()
        
        executionParams = oppmodify(self.context, params)
        if self.getLogFileName() != None:
            logFileParam = self.getLogFileName()
        else:
            logFileParam = "" 
            
        executionParams = oppmodify(executionParams, opp("logFile", logFileParam))
        
        #execDir = oppval('testExecDir', self.context)
        #if execDir != None:
        #    executionParams = oppmodify(executionParams, opp("resultFile", execDir + P_DIR_SEP + DP_RESULT_FILENAME))
        
        self.dbgl(self.name + ".execute():" + executionParams)
        
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
        
    def getDirFromContext(self, dirParamName):

        dirParam = oppval(dirParamName, self.context)
        return dirParam
    
    def getRootDir(self):
        d = self.getDirFromContext(P_KEY_ROOTDIR)
        if (d == None):
            d = P_DEFAULT_ROOTDIR
        return d
    
    def getInputDir(self):
        d = self.getDirFromContext(P_KEY_INPUTDIR)
        if (d == None):
            d = self.getRootDir() + P_DIR_SEP + P_DEFAULT_INPUTDIR
        return d

    def getOutputDir(self):
        d = self.getDirFromContext(P_KEY_OUTPUTDIR)
        if (d == None):
            d = self.getRootDir() + P_DIR_SEP + P_DEFAULT_OUTPUTDIR
        return d    
    
    
