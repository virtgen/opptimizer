#!/usr/bin/env python

from .PModulePy import *
from .PLog import *
from .opp import *
from .pcons import *
import pandas as pd

class PSplitModule(PModulePy):
    def __init__(self, name=""):
        PModulePy.__init__(self,name)
        return
    
    def execute(self, params, tokenData = None):

        tokenData = PModulePy.execute(self, params)

        self.dbgopen()
        self.dbgl("SPLIT DATA ---------------- ")

        self.createSetByOpps(params, 'trainset', 'trainlices', 'trainsteps', 'traincolsfile', 'traincols', 
            'trainfile', P_TRAINSET_DEFAULT_FILENAME, 'trainfileformat' )
 
        self.createSetByOpps(params, 'testset', 'testslices', 'teststeps', 'testcolsfile', 'testcols', 
            'testfile', P_TESTSET_DEFAULT_FILENAME, 'testfileformat' )

        self.createSetByOpps(params, 'validateset', 'validateslices', 'validatesteps', 'validatecolsfile', 'validatecols', 
            'validatefile', P_VALIDATESET_DEFAULT_FILENAME, 'validatefileformat' )

        self.resultFileClose()
        
        self.dbgclose()
    
        return tokenData

    def createSetByOpps(self, params, inputFilesOpp, slicesOpp, stepsOpp, colsFileOpp, colsOpp, 
            fileOpp, defaultResultFileName, fileFormatOpp):
        self.dbgl(" ---- createSetByOpps for " + str(inputFilesOpp) + " ----")

        paramsUnion = oppmodify(self.getContext(), params)

        inputFiles = opptolist(inputFilesOpp, paramsUnion)
        if inputFiles and len(inputFiles) > 0:
            slices = opptopairs(slicesOpp, paramsUnion)
            steps = opptolist(stepsOpp, paramsUnion)
            colsFile = oppval(colsFileOpp, paramsUnion)
            cols = opptolist(colsOpp, paramsUnion)
            cols = self.resolveCols(colsFile, cols)
            resultFile = oppval(fileOpp, paramsUnion, defaultResultFileName)
            resultFileFormat = oppval(fileFormatOpp, paramsUnion, P_SET_DEFAULT_FILFORMAT)
            self.createSet(inputFiles, slices, steps, cols, resultFile, resultFileFormat)
        else:
            self.dbgl("createSetByOpps: No data files defined for " + str(inputFilesOpp))


    def createSet(self, setInputFiles = None, slices = None, steps = None, cols = None,
        setResultFileName = P_SET_DEFAULT_FILENAME, resultFileFormat = P_SET_DEFAULT_FILFORMAT):

        self.dbgl('SplitData::createSet resultFileName: ' + setResultFileName
            + ' format ' + resultFileFormat)

        if (setInputFiles and len(setInputFiles) > 0):

            file_ind = 0
            files_number = len(setInputFiles)
            slices_number = len(slices) if slices else 0
            steps_number = len(steps) if steps else 0
            finalPdData = []
            while file_ind < files_number:
                inputFile = setInputFiles[file_ind]
                file_slice = slices[file_ind] if file_ind < slices_number else None
                file_step =  steps[file_ind] if file_ind < steps_number else None
                pdData = self.loadInputFile(inputFile, file_slice, file_step, cols)
                if pdData is not  None:
                    self.dbgl('Addig input data items in size of ' + str(len(pdData.index)))
                    finalPdData.append(pdData)
                else:
                    self.dbgl('No input data available in ' + str(inputFile) + ' ' + str(pdData))
                file_ind += 1

            processed_files_count = len(finalPdData)
            if processed_files_count > 0:
                self.dbgl('Collecting data from ' + str(processed_files_count) + ' files')
                finalDataFrame = pd.concat(finalPdData)
                self.saveFinalInputFile(finalDataFrame, setResultFileName, resultFileFormat)
            else:
                self.dbgl('No data from input files have been collected. Generation of ' + str(setResultFileName) + ' skipped.')
        else:
             self.dbgl('SplitData::createSet: No input files given')
        return

    # Loads one input file and generates PD data from it limited by file_slice
    # - if file_slice is None, all data (rows) are used for reultant data
    def loadInputFile(self, inputFile, file_slice, file_step, file_cols):
        start_ind, end_ind = file_slice if file_slice else (None,None)
        file_step = int(file_step) if file_step else 1
        files_cols_number = len(file_cols) if file_cols else -1
        self.dbgl('loadInputFile: ' + str(inputFile) + ', slice[' + str(start_ind) + ',' + str(end_ind) + '], step: ' + str(file_step) +
            ', cols number: ' + str(files_cols_number))
        print(file_cols)
        resultPD = None

        inputFilePath = self.getInputPath().clone().add(inputFile)
        if inputFilePath.exists():   
            try:
                self.dbgl('Load CSV data from ' + inputFilePath.getPath())
                resultPD = pd.read_csv(inputFilePath.getPath())
                start_ind = int(start_ind) if start_ind else 0
                end_ind = int(end_ind) if end_ind else len(resultPD.index) - 1
                self.dbgl('Final slice after file load is [' + str(start_ind) + ',' + str(end_ind) + ']')
                items_from_slice = list(range(start_ind, end_ind + 1, file_step))
                if file_cols:
                    cols_number = len(file_cols)
                    data_cols_number = len(resultPD.columns)
                    if cols_number > 0 and len(file_cols) <= data_cols_number: 
                        self.dbgl('Limiting columns to ' + str(len(file_cols)))
                        resultPD = resultPD[file_cols]
                    else:
                        self.dbgl('WARNING: cannot limit cols as it not match columns in iput data: ' +  str(cols_number) + ' vs ' + str(data_cols_number))
                resultPD = resultPD.filter(items=items_from_slice, axis=0)
            except Exception as err:
                self.dbgl('ERROR: xception during CSV parse: ' + str(err))
        else:
            self.dbgl('File ' + inputFilePath.getPath() + ' not exists')
        return resultPD

    def saveFinalInputFile(self, finalDataFrame, setResultFileName, resultFileFormat):
        rows_count =  len(finalDataFrame.index) if finalDataFrame is not None else 0
        testExecDir = self.getCurrentTest().getTestExecDir()
        outputFilePath = PPath(testExecDir).clone().add(setResultFileName).getPath()

        self.dbgl('saveFinalInputFile: store ' + str(rows_count) + ' rows to ' + str(outputFilePath)
            + ', format: ' + str(resultFileFormat))
        finalDataFrame.to_csv(outputFilePath, index=False)
        return

    def resolveCols(self, trainColsfile, trainCols):
        result = None

        if trainCols and len(trainCols) > 0:
            result = trainCols
        elif trainColsfile: 
            self.dbgl('Reading columns from file ' + str(trainColsfile))
            colsFilePath = self.getInputPath().clone().add(trainColsfile)
            if colsFilePath.exists():
                colsFilePath.open()
                lines = colsFilePath.readLines()
                cols = []
                lines_number = len(lines)
                if lines_number > 0:
                    for line in lines:
                        line = line.replace(P_NEW_LINE,'')
                        cols_from_line = opplistvals(line)
                        if cols_from_line and len(cols_from_line) > 0:
                            cols.extend(cols_from_line)
                if len(cols) > 0:
                    self.dbgl('Columns read: ' + str(len(cols))) 
                    result = cols
                else:
                    self.dbgl('WARNING: no columns found in file. Columns limiting skipped')
                
                colsFilePath.close()
            else:
                self.dbgl('WARNING: no columns file found. Columns limiting skipped')

        return result


    def onFileProcess(self, fileToProcess, params,tokenData):
        # add your code for single data file here

        self.dbgopen()
        self.dbgl("SplitData::onFileProcess  " + str(fileToProcess) + " skipped.")
        self.dbgclose()

        return tokenData