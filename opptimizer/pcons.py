#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

from opp import *

MED_VER = 5

def medversion():
    return 'm' + str(MED_VER)

P_DIR_SEP = '/'
P_UP_DIR = '..' + P_DIR_SEP

P_DEFAULT_ROOTDIR = '.'
P_DEFAULT_INPUTDIR = 'output'
P_DEFAULT_OUTPUTDIR = 'output'
P_DEFAULT_TRAININGDIR = 'training'
P_DEFAULT_RAWDIR = 'raw'


P_SUMMARY_FILENAME = 'summary-log.txt'
P_EXEC_FILENAME = 'exec-log.txt'
P_RESULT_FILENAME = 'result.txt'
P_TESTLIST_FILENAME = 'testlist.txt'
P_TESTCHAIN_FILENAME = 'testchain-log.txt'

PSERVICE_MAX_PARAMS_MSG_LEN = 1024 * 5
PSERVICE_MAX_REPLY_MSG_LEN = 1024 * 1

P_KEY = 'key'
P_KEY_TESTNAME = 'testName'
P_KEY_TEST = 'test'
P_KEY_ROOTDIR = 'rootDir'
P_KEY_DATADIR = 'dataDir'
P_KEY_TRAINDIR = 'trainDir'
P_KEY_RAWDATADIR = 'rawDataDir'
P_KEY_INPUTDIR = 'inputDir'
P_KEY_OUTPUTDIR = 'outputDir'
P_KEY_MODELDIR = 'modelDir'
P_KEY_IN = 'in'
P_KEY_OUT = 'out'

P_KEY_FILTER = 'filter'

KEY_PREPAREDATA = 'PrepareData'


KEY_PLOT = 'plot'
KEY_PRECISION = 'precision'
KEY_RECALL = 'recall'
KEY_FALLOUT = 'fallout'
KEY_ACCURACY = 'accuracy'
KEY_CLASSIFIER = 'cl'
KEY_RESULTFILE = 'ResultFile'
KEY_DESCRIPTION = 'description'

KEY_COLOR = 'color'
KEY_INVERSE = 'inverse'
VAL_CL_SVM = 'svm' 
VAL_CL_NN = 'nn'
VAL_CL_DT = 'dt'
VAL_CL_GAUSSNB = 'gaussnb'
VAL_CL_RANDFOREST = 'rforest'
VAL_CL_ADABOOST = 'adaboost'
VAL_BEST = 10.0
VAL_BLUE = 'blue'
VAL_RED = 'red'

def oppKey(val):
    return P_KEY + '=' + str(val)

def oppIn(fileName):
    return P_KEY_IN + '=' + str(fileName)

def oppOut(val):
    return P_KEY_OUT + '=' + val
#returns output dir with standard name in given path

def oppStdOutputDir(path):
    return opp(P_KEY_OUTPUTDIR,path + '/' + P_DEFAULT_OUTPUTDIR)

def oppCommand(val):
    return 'command=' + val

def oppRange(val):
    return 'range=' + val

def oppRoot(rootPath):
    return 'RootDir=' + rootPath

#def oppList(key, valList):
#    resultList = [key]
#    resultList.extend(valList) 
#    return resultList
    
def oppThreshold(key, th):
    return 'key=' + key + ';threshold=' + str(th)

def oppPlot(key,params):
    opp = 'key=' + key
    for par in params:
        opp = oppsum(opp, par)
    return opp
    
def oppLabel(label):
    return 'label=' + label

def oppColor(col):
    return 'color=' + col

def oppPrepareData(val):
    return KEY_PREPAREDATA + '=' + val

def oppTrainDir(val):
    return P_KEY_TRAINDIR + '=' + val

def oppInputDir(val):
    return P_KEY_INPUTDIR + '=' + val

def oppOutputDir(val):
    return P_KEY_OUTPUTDIR + '=' + val

def oppModelDir(val):
    return P_KEY_MODELDIR + '=' + val

def oppRawDataDir(val):
    return P_KEY_RAWDATADIR + '=' + val

def oppResultFile(val):
    return KEY_RESULTFILE + '=' + val

def oppDescription(val):
    return KEY_DESCRIPTION + '=' + val
