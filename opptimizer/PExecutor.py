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

import glob
import sys
import time
import os
import shutil
import importlib.util
import types

from .opp import *
from .pcons import *
from .PTest import *
from .PResult import *
from .putils import *
from .PLog import *
from .PPath import *
from .PModule import *
from .Mod import *
from .__about__ import *


OPEXECUTE_VER = 14
MEDEXECUTE_WITHOUT_DATAPREPARING = True

DBG_BUILD_CASE_TREE = False
DBG_REF_TEST = False
DBG_RESULT = False

#session_started = False

class PExecutor:
    def __init__(self, context = None, params = None, modules = None, cfg = None):

        if cfg is not None:
             context = self.load_cfg_to_context(cfg, context)

        self.set_context(context)
        self.set_params(params)
        self.set_modules(modules)

        #self.result = dpResult()
        self.session_started = False
        #self.summaryLog = None
        self.execLog = None
        self.testlistLog = None
        self.lasttestLog = None
        self.resultFilePath = None
        self.execDir = PPath()
        self.testExecDir = PPath()
        
        return
    
    def get_context(self):
        return self._context

    def set_context(self, value):
        self._context = value

    def get_params(self):
        return self._params

    def set_params(self, value):
        self._params = value

    def get_modules(self):
        return self._modules

    def set_modules(self, value):
        self._modules = value


    
    def version(self):
        return 'e'+ str(OPEXECUTE_VER)
    
    def dbgl(self, textToWrite, level=DBG_LOW_LEVEL):
        if self.execLog != None and self.execLog.isOpened():
            self.execLog.dbgl(textToWrite, level)

    def setCfg(self,cfg):
        if cfg is not None:
            ctxFromFile = PPath(cfg).context()
            if ctxFromFile and ctxFromFile != '':
                context = self.get_context()
                if context is None:
                    context = ''
                context = oppmodify(context, ctxFromFile)  
    
    def load_cfg_to_context(self, cfg_file, existing_context):
        ''' Load context from config file and merge it with existing_context'''
        if cfg_file is not None:
             ctxFromFile = PPath(cfg_file).context()
             if ctxFromFile and ctxFromFile != '':                
                  if existing_context is None:
                       existing_context = ''
                  existing_context = oppmodify(existing_context, ctxFromFile)
        return existing_context
    


    def remove_selected_dirs(self, path, dirs_to_clean, dirs_to_exclude=None, verbose=False, execdir_prefix = P_EXECDIR_PREFIX_DEFAULT):
        """
        Removes specified directories from the given path while excluding specified directories.
        Only considers directories whose basenames start with exec output 'exec-' (or other prefix defined by 'execdir' param).

        Parameters:
        - path (str): The base path where directories should be checked.
        - dirs_to_clean (set or list): Names of directories that should be removed.
        - dirs_to_exclude (set or list, optional): Names of directories to be excluded from removal.
        """
        dirs_to_exclude = dirs_to_exclude or set()  # Default to an empty set if not provided

        removed = []
        excluded = []
        execDirPath = PPath(path)
        if execDirPath.exists():
            for item in execDirPath.getDirFiles():
                baseName = PPath(item, basename=True).getPath()
                #print(f'-{baseName}, {item}')
                if os.path.isdir(item) and baseName.startswith(execdir_prefix + '-'):
                    if (dirs_to_clean is None or baseName in dirs_to_clean)  and baseName not in dirs_to_exclude:
                        shutil.rmtree(item)
                        removed.append(baseName)
                    elif baseName in dirs_to_exclude:
                        excluded.append(baseName)
            if verbose:
                print('Clean:Removed dirs:[{0}], excluded dirs:[{1}]'.format(removed, excluded))
        else:
            if verbose:
                print('Clean: exec path {0} not exists'.format(execDirPath.getPath()))


    def cleanExecDirs(self, path_to_clean, parmsUnion, verbose=False, execdir_prefix = P_EXECDIR_PREFIX_DEFAULT):
        ''' Removes exec dirs from path_to_clean
            Can be limited to files defined in 'cleanInclude' and exclude files defined in 'cleanExclude' ''' 
        
        directories_to_clean = opptolist('cleanInclude', parmsUnion, default = None)
        directories_to_exclude  = opptolist('cleanExclude', parmsUnion, default = None)

        if directories_to_clean is not None:
            directories_to_clean = [getExecDirForId(id, execdir_prefix) for id in directories_to_clean]
        if directories_to_exclude  is not None:
            directories_to_exclude = [getExecDirForId(id, execdir_prefix) for id in directories_to_exclude]

            
        if verbose:
            print("cleanExecDirs, path_to_clean:{0}, include:{1}, exclue:{2}".format(path_to_clean, directories_to_clean, directories_to_exclude))
        self.remove_selected_dirs(path_to_clean, directories_to_clean, directories_to_exclude, verbose=verbose, execdir_prefix = execdir_prefix)

        return
    
    # New method of execution
    def run(self, tokenData = None, context = None, params = None, modules = None, scope = (), cfg = None, verbose = False, **kwargs):
        ''' If cfg param not none, it loads addicional context from file '''
        context = self.load_cfg_to_context(cfg, context)

        # prevent to treat one-element tuple as a list eg. run( scope=([a,b]) ) may be equvalent as run(scope=[a,b])
        if not isinstance(scope, tuple):
            scope = (scope,)

        #print(f"Len: {len(scope)}, SCOPE{scope}")
        return self.execute(P_KEY_TEST, context, params, *scope, modules = modules, tokenData = tokenData, verbose = verbose)
    
    # deprecated way to use from client side
    def execute(self, command = None, context = None, params = None, *paramRange, **kwargs):
        result = None
        '''  
            Modules are extracted in following order (only one point is selected):
                1. modules list in kwargs (key='modules')
                2. modules param in context ('modules=..') - only modules names as strings
                3. PExecutor.modules attribute as a list

            Context and params are taken from PExecutor.context and PExecutor.params 
                and can be overriden by arguments of this method
            NOTE: calling this method directly (instead of 'run') does not load the context from configuration file
        '''

        if 'verbose' in kwargs:
            verbose = kwargs.get('verbose')
        else:
            verbose = False
        
        DBG_LEVEL = DBG_LOW_LEVEL if verbose else DBG_MEDIUM_LEVEL

        base_context = self.get_context()

        if base_context is not None:
            if context is not None:
                context = oppmodify(base_context, context)
            else:
                context = base_context
        else:
             pass # context from method param is used
             

        if context is None:
             context = self.get_context() if self.get_context() is not None else ''

        base_params = self.get_context()

        if base_params is not None:
            if params is not None:
                params = oppmodify(base_params, params)
            else:
                params = base_params
        else:
             pass # params from method param is used
        
        
        if params is None:
             params = self.get_params() if self.get_params() is not None else ''

        paramsUnion = oppmodify(context, params)

        outDir = oppval('dout', paramsUnion)
        if outDir == None:
            outDir = PPath(P_DOUT_DEFAULT, parent='.').getPath()

        #print(f"PARAM RANGE:{paramRange}")
        if len(paramRange) == 0 or len(paramRange[0]) == 0:
             paramRange = (['exmode', 'single'],)
     
        execdir_prefix = oppval('execdir', paramsUnion, default=P_EXECDIR_PREFIX_DEFAULT)

        removeExecDirs = oppvalbool('clean', paramsUnion, 'False')
        if removeExecDirs:
            self.cleanExecDirs(outDir, paramsUnion, verbose=verbose, execdir_prefix = execdir_prefix)

        exactDirName = oppvalbool('execdirexact', paramsUnion, 'False')
        execDir = createNewExecId(outDir, verbose, execdir_prefix, exactDirName=exactDirName)
    
#        if (command == KEY_LEARN or command == KEY_SEGMENT):
        testListDir = execDir
 #       else:
  #          testListDir = None
        self.initLogFiles(outDir, execDir, testListDir)

        tokenData = None
        if 'tokenData' in kwargs:
             tokenData = kwargs.get('tokenData')
             

        modules = None
        if 'modules' in kwargs:
            modules = kwargs.get('modules')
            self.dbgl('Modules got from args: {0}'.format(modules), DBG_LEVEL)

        if modules is None:
            modulesParam = oppval('modules', context)
            if (modulesParam != None):
                modules = opplistvals(modulesParam)
            self.dbgl('Modules got from context: {0}'.format(modules))

        if modules is None:
             print('Modules got from executor: {0}'.format(str(self.get_modules())))
             modules = self.get_modules() if self.get_modules() is not None else []

        self.dbgl('======================================================================',  DBG_LEVEL)
        self.dbgl('Executor version:{0}'.format(__version__))
        self.dbgl('Python version:' + str(sys.version_info),  DBG_LEVEL)
        #self.dbgl('Execute' + command)
        self.dbgl('context:' + context,  DBG_LEVEL)
        self.dbgl('params:' + params,  DBG_LEVEL)
        self.dbgl('modules:' + str(modules),  DBG_LEVEL)
        self.dbgl('range:' + str(paramRange),  DBG_LEVEL)
        self.dbgl('======================================================================',  DBG_LEVEL)



        
        if not self.session_started:
            #self.summaryLog.writeAsAppendLine('TestEngineVersion=' + self.version() + ';', True)
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
        
                
        #rootSummary = oppsum(rootSummary, oppRange(str(paramRange)))
    
        #self.summaryLog.write(rootSummary)
        
        self.dbgl(oppOut(getExecDirShortName(execDir)))
        
        inResultFile = oppval(P_KEY_IN, params)
        if DBG_REF_TEST:
            self.dbgl("<ref-test>in param: " + str(inResultFile))
            
        
        if command ==P_KEY_TEST:
            summaryText = oppCommand(command)
            
            param_lines = []
            if (inResultFile != None):
                inResultFile += '/' + P_RESULT_FILENAME
                if DBG_REF_TEST:
                    self.dbgl("<ref-test>inResultFile:" + inResultFile)
                summaryText =  oppsum(summaryText, opp(P_KEY_IN, inResultFile))
                
                lines = getFileLines(inResultFile)
                if DBG_REF_TEST:
                    self.dbgl("<ref-test>read " + str(len(lines)) + ' lines from result file')
                param_lines = []
                #if (learningToDo):
                for l in lines:
                    refTestName = oppval(P_KEY_TESTNAME, l)
                    param_l = oppmodify(l, oppemptyvals(P_KEY_TESTNAME, KEY_ACCURACY, KEY_PRECISION,KEY_RECALL, KEY_FALLOUT))
                    param_l = oppmodify(param_l, opp(P_KEY_REF_TEST, refTestName))
                    param_lines.append(param_l)
                    if DBG_REF_TEST:
                        self.dbgl("<ref-test>applied:"+ l)
                        self.dbgl("<ref-test>cleaned:"+ param_l)
                #else:
                #    param_lines = lines
                self.dbgl('PARAM_LINES: ' + str(param_lines))
            else:
                param_lines.append('')
            
            if (dataDir != None):
                summaryText = oppsum(summaryText, opp(P_KEY_DATADIR, dataDir))
                                    
            if (modelDir != None):
                summaryText = oppsum(summaryText, opp(P_KEY_MODELDIR, modelDir))                    
    
            summaryText = oppsum(summaryText, '\n' + oppRange(str(paramRange)))
            
            self.dbgl(summaryText)
            
            
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
                
                self.dbgl("Clean condMods: " + str(condMods), DBG_LEVEL)

                if paramRange[0] != None:
                    
                    newConsOpp = getDescriptionForProps(refTest)
                    
                    # mark all conditional modules as accepted for the first branch of tree
                    newAcceptOpp = opplist("acceptMods", *condMods)
                    newConsOpp = oppmodify(newConsOpp, newAcceptOpp)
                    
                    self.dbgl("CONST " + newConsOpp, DBG_LEVEL)
                    
                    caseTree = self.buildCaseTree(test_params, condMods, newConsOpp, paramRange)
                    self.dbgl("---- Case tree -------", DBG_LEVEL)
                    for case in caseTree:
                        self.dbgl(case, DBG_LEVEL)
                    self.dbgl("----------------------", DBG_LEVEL)
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
    
            self.execLog.dbgl('skipDataPreparing=' + str(skipDataPreparing), DBG_LEVEL)
            if (skipDataPreparing):
                for i in range(0, len(finalCaseList)):
                    finalCaseList[i] = oppmodify(finalCaseList[i],opp(KEY_PREPAREDATA,'0'))
            
            #test.setExecDir(execDir)
            finalCaseList = self.prepareChain(finalCaseList)

            self.dbgl('Final test list: {0}'.format([oppval(P_KEY_TESTNAME, t) for t in finalCaseList]), DBG_LEVEL)
            if finalCaseList and len(finalCaseList)>0: 
                lastTestName = oppval(P_KEY_TESTNAME, finalCaseList[-1],'None')
            else:
                lastTestName = 'None'
            self.lasttestLog.writeAsAppendLine(lastTestName, True)
            for c in finalCaseList:
                self.testlistLog.writeAsAppendLine(c, True)
            
            result = self.executeChain(execDir, context, finalCaseList, modules = modules, tokenData = tokenData, dbgLevel = DBG_LEVEL)
            
        elif command == P_KEY_FILTER or command == KEY_PLOT:
            if (inResultFile != None):
                inResultFile += '/' + P_RESULT_FILENAME
                #print 'INIT-FILE',inResultFile
                self.dbgl(oppsum(oppCommand(command),opp(P_KEY_IN, inResultFile)))
                plots = []
                            #print "paramRange",paramRange
                
                if DBG_RESULT:
                    self.dbgl("<result>paramRange:" + str(paramRange))
                    
                for p in paramRange:
                    print('plot',p)
                    plots.append(p)
                    self.dbgl(p)
                plots = preparePlots(plots, inResultFile)
                
                if DBG_RESULT:
                    self.dbgl("<result>plots:" + str(plots))
                
                if command == P_KEY_FILTER:
                    newResultFile = execDir + '/' + P_RESULT_FILENAME
                    if DBG_RESULT:
                        self.dbgl("<result>new resultFile:" + newResultFile)
                    saveResultToFile(newResultFile)
                elif command == KEY_PLOT:
                    displayPlots(plots, params, execDir = execDir)
                
                resetPlots()
                result = PTest(command, params)
                result.setExecDir(execDir)

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
    
    # Returns last executed test if any
    def executeChain(self, execDir, context, testchain, modules = [], tokenData = None, dbgLevel = DBG_MEDIUM_LEVEL):
        
        test_counter = 0
        _TIME_totalChainExecution = time.time()
        
        test = None
        #tokenData = None

        for testParams in testchain:
            test_counter += 1
    
            test_name = oppval(P_KEY_TESTNAME, testParams)
            if (test_name == None or test_name == ''):
                testParams = oppmodify(testParams, opp(P_KEY_TESTNAME, 'noname' + str(test_counter).zfill(6)))
            

            
            self.dbgl('Execute {0} =============> '.format(test_name))
            
    
            #medlearn.learnInit(test)
    
            prepareData = oppval('PrepareData', testParams)
    
            if (prepareData == '1'):
                self.dbgl("executeChain: PrepareData is 1 !!!")
                # here is the place to collect input data from external source (for future implementation)
            
            if (oppval('flatExecDir', context) == '1'):
                flatExecDir = True
            else:
                flatExecDir = False
            
            if flatExecDir:
                testExecDir = execDir
            else:
                testExecDir = execDir +  P_DIR_SEP + test_name
                self.dbgl('Create exec dir for test: ' + testExecDir, dbgLevel)
                self.testExecDir.setPath(testExecDir)
                self.testExecDir.createDirIfNone()
            

                
                
            dtestexecskip = oppvalbool('dtestexecskip', context)
            if not dtestexecskip:
                context = oppmodify(context, opp('dtestexec', testExecDir))
            else:
                self.dbgl('Skipping dtestexec setup for module')
            
            context = oppmodify(context, opp("dresultfile", self.resultFilePath))
            
            test = PTest(test_name, testParams)
            test.setTestExecDir(testExecDir)
            test.setExecDir(execDir) # main exec dir

            resultUse = oppvalbool('resultFileUse', context)
            if resultUse:
                self.dbgl('Result file managed by Executor.. resultFileUse:{0}'.format(resultUse))
                # Write test name to result file 
                resFile = PPath(self.resultFilePath)
                resFile.open('a')
                resFile.write(opp(P_KEY_TESTNAME, test_name) + P_PARAM_SEP)
                resFile.close()
            else:
                 self.dbgl('Result file not handled by Executor.. resultFileUse:{0}'.format(resultUse), dbgLevel)
            
            #modulesParam = oppval('modules', context)
            condMods = opplistvals(oppval('condMods', context))
            acceptMods = opplistvals(oppval('acceptMods', testParams))
            
            #if (modulesParam != None):
                                                
            modules_dir = oppval('dmods', context)
            #module_exec_dir = "../../modules/" + mod + "/"
            
            if modules_dir == None or modules_dir == '':
                modules_dir = '.'  #current directory is default dir for modules

            #modules = opplistvals(modulesParam)
            if (len(modules)>0):
                for mod in modules:

                    modName = ''
                    module = None
                    moduleToLoadFromSource = False # whether module should be loaded from file
                    if isinstance(mod, str):
                        self.dbgl("Execute module by string: {0}  ------------->".format(mod))
                        modName = mod
                        moduleToLoadFromSource = True
                    elif isinstance(mod, PModule):
                        self.dbgl("Execute module by module object: {0}  ------------->".format(mod.getName()))
                        modName = mod.getName()
                        module = mod
                    elif isinstance(mod, types.FunctionType):
                        module = Mod(mod)   # mod is passed to Mod's constructor as func_exec argument
                        self.dbgl("Execute module by function: {0} ------------->".format(module.getName()))
                        modName = module.getName()

                    if (modName != ''):
                        if (not modName in condMods) or (modName in acceptMods): 
                            self.dbgl("RUN module:" + modName, dbgLevel)
                            self.dbgl("cwd:" + os.getcwd(), dbgLevel)

                            if moduleToLoadFromSource:
                                module_exec_dir =  modules_dir + "/" + mod + "/"
                                self.dbgl("module_exec_dir:" + module_exec_dir)
                                #mod_py = imp.load_source(mod, module_exec_dir + "/" + mod + ".py")
                                modulePath = PPath(module_exec_dir + "/" + mod + ".py")

                                if modulePath.exists():
                                    # Load the module dynamically using importlib
                                    spec = importlib.util.spec_from_file_location(mod, modulePath.getPath())
                                    mod_py = importlib.util.module_from_spec(spec)

                                    try:
                                        spec.loader.exec_module(mod_py)
                                    except Exception as e:
                                        raise RuntimeError(f"Error during module execution: {e}")

                                    # Print attributes to debug
                                    # print(f"Attributes of module {mod_py.__name__}:")
                                    # for attribute in dir(mod_py):
                                    #     print(attribute)

                                    # Check if the getModule function exists before calling it
                                    if hasattr(mod_py, 'getModule'):
                                        module = mod_py.getModule(mod_py)
                                    else:
                                        raise AttributeError(f"Module '{mod_py}' has no attribute 'getModule'")
                                    
                                    module = mod_py.getModule(mod)
                                else:
                                    self.dbgl("Module not exists:" + modulePath.getPath())
                                    raise AttributeError(f"Module '{mod}' does not exist")
                                
                            module.setCurrentTest(test)

                            init_func = module.get_func_init()
                            if init_func is not None:
                                self.dbgl("Call module init by handler", dbgLevel)
                                init_func(module, test_name, context)
                            else:
                                self.dbgl("Call module init by module method", dbgLevel)
                                module.init(test_name, context)

                            #test.addModule(module)  TODO-abak-test
                            exec_func = module.get_func_exec()
                            if exec_func is not None:
                                self.dbgl("Call module exec by handler. Type of token {0}".format(type(tokenData)), dbgLevel)
                                tokenData = exec_func(module, testParams, tokenData)
                            else:
                                self.dbgl("Call module exec by module method. Type of token {0}".format(type(tokenData)), dbgLevel)
                                tokenData = module.execute(testParams, tokenData)

                            test.setTokenData(tokenData)
                            self.dbgl(' end of execution for module {0} -------------|'.format(module.getName()))

                        else:
                            self.dbgl(' -------------> Module ' + mod + 'SKIPPED  -------------|')
                    else:
                        self.dbgl(" -------------> executeChain: empty module name. SKIPPED -------------|")
            else:
                self.dbgl(" -------------> executeChain: Empty list of modules. Nothing to do. -------------|")
            # else:
            #     self.dbgl("executeChain: modules to run not defined")
        
            if resultUse:
                # Write new line to result file 
                resFile = PPath(self.resultFilePath)
                resFile.open('a')
                resFile.write(P_NEW_LINE)
                resFile.close()
          
            self.dbgl('End of test {0} extection ==================|'.format(test_name))

        return test    
  
            #TODO uncomment
            #_TIME_dump('totalChainExecution',_TIME_totalChainExecution)  
    
    #returns hanles to files [outDirHandle, execDirHandle]
    def initLogFiles(self, outDir, execDir, testListDir):
        
        #rootSummaryFileName = outDir + '/' + P_SUMMARY_FILENAME
        execSummaryFileName = execDir + '/' + P_EXEC_FILENAME
        testListFileName = execDir + '/' + P_TESTLIST_FILENAME
        lastTestFileName = execDir + '/' + P_LASTTEST_FILENAME
        
        #self.summaryLog = PPath(rootSummaryFileName, "summary")
        #self.summaryLog.open('a')
        self.execLog = PLog("ex", execSummaryFileName)
        self.execLog.LEVEL = DBG_LOW_LEVEL
        self.execLog.openLog()

        if (testListDir != None):
            self.testlistLog = PPath(testListFileName, "testList")
            self.testlistLog.open('a')
            self.lasttestLog = PPath(lastTestFileName, "lasttestLog")
            self.lasttestLog.open('a')
            
        
        self.resultFilePath = execDir + '/' + P_RESULT_FILENAME
        
    
    def closeLogFiles(self):
        #f self.summaryLog != None:
            #self.summaryLog.close()
            
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
            self.dbgl('----------- ') 
            self.dbgl(str(paramRange))
            
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
                    self.dbgl('valcase:' +  str(valCase) + ' caseInd ' + str(caseInd))
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
                    self.dbgl('new acceptMods:' + str(acceptMods))
                    
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

#returns pair [exec id exec_dir] 
def createNewExecId(outDir, verbose = False, execdir_prefix = P_EXECDIR_PREFIX_DEFAULT, exactDirName = False):
    ''' if exactDirName is True, it simpy uses execdir_prefix as dir name'''
    dir_id = 0

    if (not os.path.isdir(outDir)):
        if verbose:    print ('Create' + outDir)
        os.mkdir(outDir)

    if not exactDirName:
        dir_list = sorted(glob.glob(outDir + '/' + execdir_prefix + '-*'), key=sortKeyForDirs)
        dir_number = len(dir_list)
        if (dir_number == 0):
            dir_id = 1
        else:
            last_prev_dir = dir_list[dir_number - 1]
            last_prev_id = getExecDirShortName(last_prev_dir)[len(execdir_prefix)+1:] # len(execdir_prefix)+1 is len of 'exec-'
            dir_id = int(last_prev_id) + 1
        
        new_dir = PPath(getExecDirForId(dir_id, execdir_prefix), parent=outDir)
    else:
        new_dir = PPath(execdir_prefix, parent=outDir)
	
    if verbose:    print('Create dir (with removing old one if exeists):' + new_dir.getPath())
    new_dir.createDirWithCleaning()

    return new_dir.getPath()


def closeSummaryFiles(outDirHandle, execDir):
	outDirHandle.close()
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
	#params = oppmodify(params, oppRoot(execDir))
	
	#if oppval(P_KEY_TRAINDIR, params) == None:
	#	if dataDir != None:
	#		trainingPath = dataDir + '/' + P_DTRAIN_DEFAULT
	#		params = oppmodify(params, opp(P_KEY_TRAINDIR, trainingPath))	
		
#	if oppval(KEY_OUTPUTDIR, params) == None:
#		if outputDir != None:
#			outputPath = outputDir + '/' + MED_DEFAULT_OUTPUTDIR
#			params = oppmodify(params, opp(KEY_OUTPUTDIR, outputPath))		

	#modelDir = oppval(P_KEY_MODELDIR, params)
	#if modelDir != None:
	#	modelPath = modelDir + '/' + P_DOUT_DEFAULT
	#	params = oppmodify(params, opp(P_KEY_MODELDIR, modelPath))	
			
	#if oppval(P_KEY_RAWDATADIR, params) == None:
	#	if dataDir != None:
	#		rawPath = dataDir + '/' + P_DRAW_DEFAULT
	#		params = oppmodify(params, opp(P_KEY_RAWDATADIR, rawPath))
	
	#if oppval(KEY_RESULTFILE, params) == None:
	#	params = oppmodify(params, opp(KEY_RESULTFILE, P_RESULT_FILENAME))
	
	#if command == P_KEY_TEST:
	#	if oppval(P_KEY_TEST, params) == None:
	#		params = oppmodify(params, 'test=1')


	return params
		

