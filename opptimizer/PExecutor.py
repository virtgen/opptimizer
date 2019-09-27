#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

import glob
import sys
import time
import os
from opp import *
from pcons import *
from PTest import *
from PResult import *
from putils import *
from PLog import *
from opptimizer.opp import opplistvals, oppmodify

OPEXECUTE_VER = 8
MEDEXECUTE_WITHOUT_DATAPREPARING = True

DBG_BUILD_CASE_TREE = False
DBG_REF_TEST = True
DBG_RESULT = True

#session_started = False

class PExecutor:
    def __init__(self):
        #self.result = dpResult()
        self.session_started = False
        self.summaryLog = None
        self.execLog = None
        self.testlistLog = None
        self.resultFilePath = None
        
        return
    
    def version(self):
        return 'e'+ str(OPEXECUTE_VER)
    
    def execute(self, command, context, params, *paramRange):
        result = None
        
        print('----------------------------------------')
        print('--------------ver:' + self.version())
        print('----------------------------------------')
        print('Execute' + command)
        print('context:' + context)
        print('params:' + params)
        rootDir = oppval('rootDir', context)
        if rootDir == None:
            rootDir = '.'

        execDir = createNewExecId(rootDir)
    
#        if (command == KEY_LEARN or command == KEY_SEGMENT):
        testListDir = execDir
 #       else:
  #          testListDir = None
        self.initLogFiles(rootDir, execDir, testListDir)
        
        if not self.session_started:
            self.summaryLog.dbgl('TestEngineVersion=' + self.version())
            self.session_started = True
            
        dataDir = oppval(P_KEY_DATADIR, params)
    #    outputDir = oppval(KEY_OUTPUTDIR, params)
    
                        
        params = applyDefaultValues(params, command, execDir, dataDir)
        modelDir = oppval(P_KEY_MODELDIR, params)
    
        rootSummary = oppsum(oppOut(getExecDirShortName(execDir)),oppCommand(command))
        
        #oppLearn = None
        #oppClassify = None
        #oppSegment = None
        #if (command == KEY_LEARN):
        #    oppLearn = oppval(KEY_LEARN, params)
        #    oppClassify = oppval(KEY_CLASSIFY, params)
        #   if (oppLearn != '1'):
        #       rootSummary = oppsum(rootSummary, opp(KEY_LEARN,oppLearn))
        #    if (oppClassify == '1'):
         #       rootSummary = oppsum(rootSummary, opp(KEY_CLASSIFY,oppClassify))
        #if (command == KEY_SEGMENT):
        #    oppSegment = oppval(KEY_SEGMENT, params)
        #    if (oppSegment != '1'):
        #        rootSummary = oppsum(rootSummary, opp(KEY_SEGMENT,oppSegment))
        
                
        rootSummary = oppsum(rootSummary, oppRange(str(paramRange)))
    
        self.summaryLog.dbgl(rootSummary)
        
        self.execLog.dbgl(oppOut(getExecDirShortName(execDir)))
        
        inResultFile = oppval(P_KEY_IN, params)
        if DBG_REF_TEST:
            self.execLog.dbgl("<ref-test>in param: " + str(inResultFile))
            
        
        if command ==P_KEY_TEST:
            summaryText = oppCommand(command)
            
            param_lines = []
            if (inResultFile != None):
                inResultFile += '/' + P_RESULT_FILENAME
                if DBG_REF_TEST:
                    self.execLog.dbgl("<ref-test>inResultFile:" + inResultFile)
                summaryText =  oppsum(summaryText, opp(P_KEY_IN, inResultFile))
                
                lines = getFileLines(inResultFile)
                if DBG_REF_TEST:
                    self.execLog.dbgl("<ref-test>read " + str(len(lines)) + ' lines from result file')
                param_lines = []
                #if (learningToDo):
                for l in lines:
                    param_l = oppmodify(l, oppemptyvals(P_KEY_TESTNAME, KEY_ACCURACY, KEY_PRECISION,KEY_RECALL, KEY_FALLOUT))
                    param_lines.append(param_l)
                    if DBG_REF_TEST:
                        self.execLog.dbgl("<ref-test>applied:"+ l)
                        self.execLog.dbgl("<ref-test>cleaned:"+ param_l)
                #else:
                #    param_lines = lines
                self.execLog.dbgl('PARAM_LINES: ' + str(param_lines))
            else:
                param_lines.append('')
            
            if (dataDir != None):
                summaryText = oppsum(summaryText, opp(P_KEY_DATADIR, dataDir))
                                    
            if (modelDir != None):
                summaryText = oppsum(summaryText, opp(P_KEY_MODELDIR, modelDir))                    
    
            summaryText = oppsum(summaryText, '\n' + oppRange(str(paramRange)))
            
            self.execLog.dbgl(summaryText)
            
            
            finalCaseList = []
            for refTest in param_lines:
                if (refTest != ''):
                    #refTestKeys = oppkeys(refTest)
                    #prepareDataNeeded = False
                    #for k in refTestKeys:
                    #    if self.isPrepareDataNeeded(k):
                    #        prepareDataNeeded = True
                    #        break
                        
                    test_params = oppmodify(params, refTest)
                    
                    
                    # TODO: cases when the same testName as input should be handled properly
                    # classification w/o learning should have the name of previous learning test
                    #if (not learningToDo):
                    #    learnFile = oppval(KEY_LEARNFILE, test_params)
                    #    if (learnFile != None):
                    #        test_params = oppmodify(test_params, opp(KEY_TESTNAME, learnFile))
                else:
                    test_params = params
                    #prepareDataNeeded = False
                    
                #self.execLog.dbgl('PrepareData:' + str(prepareDataNeeded))
    
                caseTree = []
                
                condModsParam = oppval("condMods", context)
                condMods = opplistvals(condModsParam)
                #limit conditional modules to those defined to run in context
                condMods = self.cleanCondMods(condMods, context)
                
                self.execLog.dbgl("Clean condMods: " + str(condMods))
                
                if paramRange[0] != None:
                    
                    newConsOpp = getDescriptionForProps(refTest)
                    
                    # mark all conditional modules as accepted for the first branch of tree
                    newAcceptOpp = opplist("acceptMods", *condMods)
                    newConsOpp = oppmodify(newConsOpp, newAcceptOpp)
                    
                    self.execLog.dbgl("CONST " + newConsOpp)
                    
                    caseTree = self.buildCaseTree(test_params, condMods, newConsOpp, paramRange)
                    self.execLog.dbgl("====================")
                    for case in caseTree:
                        self.execLog.dbgl(case)
                else:
                    #if (prepareDataNeeded):
                    #    test_params = oppmodify(test_params,opp(KEY_PREPAREDATA,'1'))
                    caseTree = [test_params]
                    
                finalCaseList.extend(caseTree)
            
            #Should always prepare data for the first test in execution
            #if str(oppClassify) == '1' and len(finalCaseList)>0:
            if len(finalCaseList)>0:
                finalCaseList[0] = oppmodify(finalCaseList[0],opp(KEY_PREPAREDATA,'1'))
                
            skipDataPreparing = MEDEXECUTE_WITHOUT_DATAPREPARING
            
            skipDataPreparingParam = oppval('skipDataPreparing', params)
            if skipDataPreparingParam != None:
                if skipDataPreparingParam == '0':
                    skipDataPreparing = False
                else:
                    skipDataPreparing = True
    
            self.execLog.dbgl('skipDataPreparing=' + str(skipDataPreparing))
            if (skipDataPreparing):
                for i in range(0, len(finalCaseList)):
                    finalCaseList[i] = oppmodify(finalCaseList[i],opp(KEY_PREPAREDATA,'0'))
            
            #test.setExecDir(execDir)
            finalCaseList = self.prepareChain(finalCaseList)
            for c in finalCaseList:
                print c
                self.testlistLog.dbgl(c, True)
                self.execLog.dbgl(opp(P_KEY_TESTNAME, oppval(P_KEY_TESTNAME, c)) + '\n')
            
            
            result = self.executeChain(execDir, context, finalCaseList)
            
        elif command == P_KEY_FILTER or KEY_PLOT:
            if (inResultFile != None):
                inResultFile += '/' + P_RESULT_FILENAME
                #print 'INIT-FILE',inResultFile
                self.execLog.dbgl(oppsum(oppCommand(command),opp(P_KEY_IN, inResultFile)))
                plots = []
                            #print "paramRange",paramRange
                
                if DBG_RESULT:
                    self.execLog.dbgl("<result>paramRange:" + str(paramRange))
                    
                for p in paramRange:
                    #print 'plot',p
                    plots.append(p)
                    self.execLog.dbgl(p)
                plots = preparePlots(plots, inResultFile)
                
                if DBG_RESULT:
                    self.execLog.dbgl("<result>plots:" + str(plots))
                
                if command == P_KEY_FILTER:
                    newResultFile = execDir + '/' + P_RESULT_FILENAME
                    if DBG_RESULT:
                        self.execLog.dbgl("<result>new resultFile:" + newResultFile)
                    saveResultToFile(newResultFile)
                elif command == KEY_PLOT:
                    displayPlots(plots)
                
                resetPlots()
                return execDir
        
        else:
            return None
        
        self.closeLogFiles()
        return result
    
    def prepareChain(self, testchain):

        test_counter = 0
        newTestChain = []
        for testParams in testchain:
            test_counter += 1
    
            test_name = oppval(P_KEY_TESTNAME, testParams)        
            if (test_name == None or test_name == ''):
                test_name = 'T' + str(test_counter).zfill(6)
                testParams = oppmodify(testParams, opp(P_KEY_TESTNAME, test_name))
            newTestChain.append(testParams)
                
        return newTestChain
    
    def executeChain(self, execDir, context, testchain):
        
        test_counter = 0
        _TIME_totalChainExecution = time.time()
        
        tokenData = None
        for testParams in testchain:
            test_counter += 1
    
            test_name = oppval(P_KEY_TESTNAME, testParams)
            if (test_name == None or test_name == ''):
                testParams = oppmodify(testParams, opp(P_KEY_TESTNAME, 'noname' + str(test_counter).zfill(6)))
            
            test = PTest(test_name, context, testParams)
            test.setExecDir(execDir)
            
            self.execLog.dbgl('Execute ' +  test_name)
            
    
            #medlearn.learnInit(test)
    
            prepareData = oppval('PrepareData', testParams)
    
            if (prepareData == '1'):
                self.execLog.dbgl("executeChain: PrepareData is 1 !!!")
                #itkServiceSocket = connectToServiceITK()
                #itkServiceSocket.send(test)
    
                #data = itkServiceSocket.recv(MEDSERVICE_MAX_REPLY_MSG_LEN)
                #print('Received ' +  data)
        
                #itkServiceSocket.close()
            
            if (oppval('flatExecDir', context) == '1'):
                flatExecDir = True
            else:
                flatExecDir = False
            
            if flatExecDir:
                testExecDir = execDir
            else:
                testExecDir = execDir +  P_DIR_SEP + test_name
                self.createTestDir(testExecDir)
                
            contextForModules = oppmodify(context, opp('testExecDir', testExecDir))
            contextForModules = oppmodify(contextForModules, opp("resultFilePath", self.resultFilePath))
            
            modulesParam = oppval('modules', context)
            condMods = opplistvals(oppval('condMods', context))
            acceptMods = opplistvals(oppval('acceptMods', testParams))
            
            if (modulesParam != None):
                modules = opplistvals(modulesParam)
                if (len(modules)>0):
                    for mod in modules:
                        if (mod != ''):
                            if (not mod in condMods) or (mod in acceptMods): 
                                self.execLog.dbgl("RUN module:" + mod)
                                self.execLog.dbgl("cwd:" + os.getcwd())
                                module_exec_dir = "../../modules/" + mod + "/"
                                self.execLog.dbgl("module_exec_dir:" + module_exec_dir)
                                #mod_py = imp.load_source(mod, module_exec_dir + "/" + mod + ".py")
                                mod_py = imp.load_source(mod, module_exec_dir + "/" + mod + ".py")
                                print("mod_y============== will call getModule()")
                                module = mod_py.getModule(mod)
                                module.init(test_name, contextForModules)
                                test.addModule(module)
                                tokenData =  module.execute(testParams, tokenData)
                            else:
                                self.execLog.dbgl('Module ' + mod + 'SKIPPED')
                        else:
                            self.execLog.dbgl("executeChain: empty module name. SKIPPED")
                else:
                    self.execLog.dbgl("executeChain: Empty list of modules. Nothing to do.")   
            else:
                self.execLog.dbgl("executeChain: modules to run not defined")
          
        return test    
  
            #TODO uncomment
            #_TIME_dump('totalChainExecution',_TIME_totalChainExecution)  

    def createTestDir(self, testDir):
        
        if (not os.path.isdir(testDir)):
            self.execLog.dbgl('create test dir: ' + testDir)
            os.mkdir(testDir)
        else:
            self.execLog.dbgl(testDir + ' already exists, creation skipped.')
    
    #returns hanles to files [rootDirHandle, execDirHandle]
    def initLogFiles(self, rootDir, execDir, testListDir):
        
        rootSummaryFileName = rootDir + '/' + P_SUMMARY_FILENAME
        execSummaryFileName = execDir + '/' + P_EXEC_FILENAME
        testListFileName = execDir + '/' + P_TESTLIST_FILENAME
        
        self.summaryLog = PLog("summary", rootSummaryFileName)
        self.summaryLog.open(True)
        self.execLog = PLog("exec", execSummaryFileName)
        self.execLog.open()

        if (testListDir != None):
            self.testlistLog = PLog("result", testListFileName)
            self.testlistLog.open()
        
        self.resultFilePath = execDir + '/' + P_RESULT_FILENAME
        
    
    def closeLogFiles(self):
        if self.summaryLog != None:
            self.summaryLog.close()
            
        if self.execLog != None:
            self.execLog.close()
            
        if self.testlistLog != None:
            self.testlistLog.close()
    
    # Remove from the condMods list the modules that do not exist in modules
    def cleanCondMods(self, condMods, context):

        result = []
        
        if condMods != None and len(condMods) > 0:        
            modulesParam = oppval("modules", context)
            modules = opplistvals(modulesParam)
                    
            result = []
            
            for condMod in condMods:
                if condMod in modules:
                    result.append(condMod)

        return result
    
    # executes one depth in prams range
    def buildCaseTree(self, params, condMods, constOpp, paramRange):
    
        resultSubTree = []
        if DBG_BUILD_CASE_TREE:
            self.execLog.dbgl('----------- ') 
            self.execLog.dbgl(str(paramRange))
            
        if (len(paramRange) > 0):
            
            
            currCase = paramRange[0]
            
            descVal = oppval(KEY_DESCRIPTION, constOpp)
            #modify description if curr prop is not there yet
            if (descVal == None or not isPropInDesc(currCase[0], descVal)):
                
                if (descVal == None):
                    descVal = ''
                if descVal != '':
                    descVal += ','
    
                descVal += str(currCase[0])
                descOpp = opp(KEY_DESCRIPTION, descVal)
                constOpp = oppmodify(constOpp, descOpp)
    
            caseInd = 0
            for valCase in currCase[1:]:
                if DBG_BUILD_CASE_TREE:
                    self.execLog.dbgl('valcase:' +  str(valCase) + ' caseInd ' + str(caseInd))
                newConsOpp = oppsum(constOpp, opp(currCase[0], valCase))
                
                #if (valCase == currCase[1] and prepareData):
                #    newConsOpp = oppmodify(newConsOpp, oppPrepareData('1'))
                
                acceptMods = opplistvals(oppval("acceptMods", constOpp))
                
                if caseInd > 0:
                    acceptMods = [] #Note that for after first item in this branch level all upper decisions sre satisfied already
                      
                for condMod in condMods:
                    if currCase[0].startswith(condMod + '_'):
                        if not condMod in  acceptMods:
                            acceptMods.append(condMod)
                            
                if DBG_BUILD_CASE_TREE:
                    self.execLog.dbgl('new acceptMods:' + str(acceptMods))
                    
                newAcceptOpp = opplist("acceptMods", *acceptMods)
                newConsOpp = oppmodify(newConsOpp, newAcceptOpp)
                
                #prepareDataForKey = (caseInd == 0 and prepareData) or isPrepareDataNeeded(currCase[0])
                
                subTree = self.buildCaseTree(params, condMods, newConsOpp, paramRange[1:])
                resultSubTree.extend(subTree)
                caseInd += 1
        else:
            #if (prepareData):
            #    constOpp = oppsum(constOpp, oppPrepareData('1'))
            finalOppPath =  oppmodify(params, constOpp)
            #print 'final-case:',finalOppPath
            resultSubTree = [finalOppPath]
        
        return resultSubTree
            
        

def isPrepareDataNeeded(key):
    result = False
    if key[0] == '_':
        result = True

    return result
                       
def sortKeyForDirs(x):
	return x.split('/')[-1][2:]

def getDirnameForId(id):
	return 'exec-' + str(id).zfill(3)

def getExecDirShortName(execDir):
	return execDir.split('/')[-1]

#returns pair [exec id exec_dir] 
def createNewExecId(rootDir):
	dir_id = 0

	if (not os.path.isdir(rootDir)):
		print ('medaap.Create' + rootDir)
		os.mkdir(rootDir)
		
	dir_list = sorted(glob.glob(rootDir + '/exec-*'), key=sortKeyForDirs)
	dir_number = len(dir_list)
	if (dir_number == 0):
		dir_id = 1
	else:
		last_prev_dir = dir_list[dir_number - 1]
		last_prev_id = getExecDirShortName(last_prev_dir)[5:]
		dir_id = int(last_prev_id) + 1
	
	new_dir = rootDir + '/' + getDirnameForId(dir_id)
	
	if (not os.path.isdir(new_dir)):
		print('Create dir:' + new_dir)
		os.mkdir(new_dir)
	
	return new_dir


def closeSummaryFiles(rootDirHandle, execDir):
	rootDirHandle.close()
	execDir.close()

def getDescriptionForProps(params):
	result = ''
	if (params != ''):
		
		keys = oppkeys(params)
		descVals = ''
		for k in keys:
			if (descVals != ''):
				descVals += ','
			descVals += k
		
		result = opp(KEY_DESCRIPTION,descVals)

	return result

def isPropInDesc(key, desc):
	result = False
	desc_list = desc.split(',')
	for desc in desc_list:
		if desc == key:
			result = True
			break

	return result

def applyDefaultValues(params, command, execDir, dataDir):
	params = oppmodify(params, oppRoot(execDir))
	
	if oppval(P_KEY_TRAINDIR, params) == None:
		if dataDir != None:
			trainingPath = dataDir + '/' + P_DEFAULT_TRAININGDIR
			params = oppmodify(params, opp(P_KEY_TRAINDIR, trainingPath))	
		
#	if oppval(KEY_OUTPUTDIR, params) == None:
#		if outputDir != None:
#			outputPath = outputDir + '/' + MED_DEFAULT_OUTPUTDIR
#			params = oppmodify(params, opp(KEY_OUTPUTDIR, outputPath))		

	modelDir = oppval(P_KEY_MODELDIR, params)
	if modelDir != None:
		modelPath = modelDir + '/' + P_DEFAULT_OUTPUTDIR
		params = oppmodify(params, opp(P_KEY_MODELDIR, modelPath))	
			
	if oppval(P_KEY_RAWDATADIR, params) == None:
		if dataDir != None:
			rawPath = dataDir + '/' + P_DEFAULT_RAWDIR
			params = oppmodify(params, opp(P_KEY_RAWDATADIR, rawPath))
	
	if oppval(KEY_RESULTFILE, params) == None:
		params = oppmodify(params, opp(KEY_RESULTFILE, P_RESULT_FILENAME))
	
	if command == P_KEY_TEST:
		if oppval(P_KEY_TEST, params) == None:
			params = oppmodify(params, 'test=1')


	return params
		
