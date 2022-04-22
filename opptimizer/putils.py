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

from .pcons import *



MEDBASE_VER = 1

_PRINT_LOG_ENABLED = True

def medbaseversion():
    return 'b' + str(MEDBASE_VER)

#Get relative path (from execution directory) to file realted to test
# @testName  name of test
#
#
def getDecorFileName(fileName, prefix= None, postfix = None):
 
    decoratedFileName = ''

    if prefix:
        decoratedFileName += prefix
    
    decoratedFileName += fileName
     
    if postfix:
        decoratedFileName += postfix
        
    return decoratedFileName


def getFileLines(file):
    f = open(file,'r')
    lines = f.readlines()
    lines = [l.split('\n')[0] for l in lines]
    return lines
    
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

# prints the object on standard output
def oppdbg(object_to_write):
    if _PRINT_LOG_ENABLED:
        print(object_to_write)
