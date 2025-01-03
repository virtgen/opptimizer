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


from .PModule import *
from .PLog import *
from .opp import *
from .pcons import *

class PModulePy(PModule):
    def __init__(self, name="", func_exec=None, func_init=None, func_onprocess=None):
        PModule.__init__(self,name, func_exec, func_init, func_onprocess)
        self.setSkipExe(True)
        
        return
        
 #   @override(PModule)
    def execute(self, params, tokenData = None):

        self.dbgopen()
        tokenData = PModule.execute(self, params, tokenData)

  
        context = self.getContext()
        paramsUnion = oppmodify(context, params)
        dataloop = oppval('dataloop', paramsUnion)

        data_pattern = oppval('datapattern', paramsUnion)
        data_prefix = oppval('dataprefix', paramsUnion)
        data_postfix = oppval('datapostfix', paramsUnion)

        if dataloop == '1':
            inputPath = self.getInputPath()
            
            if inputPath and inputPath.getPath():
                if inputPath.exists():
                    files = inputPath.getDirFiles(pattern = data_pattern,
                        prefix = data_prefix, postfix = data_postfix, key = PPath.sortByPaths)
                    if len(files) > 0:
                        for f in files:
                            onprocess_func = self.get_func_onprocess()
                            if onprocess_func is not None:
                                #self.dbgl("Call module onprocess_func by handler. Type of token {0}".format(type(tokenData)))
                                tokenData = onprocess_func(self, f, params, tokenData)
                            else:
                                #self.dbgl("Call module onprocess_func by module method. Type of token {0}".format(type(tokenData)))
                                tokenData = self.onFileProcess(f, params, tokenData)
                    else:
                        self.dbgl(f"No input files found in {inputPath.getPath()}")
                else:
                    self.errl('PModulePy::exceute: Input path not exists: ' + str(inputPath.getPath()))
            else:
                self.errl('PModulePy::exceute: Input path not defined')

        self.dbgclose()

        return tokenData

    # to override in child class
    def onFileProcess(self, fileToProcess,  params, tokenData):
            
        return tokenData
    
