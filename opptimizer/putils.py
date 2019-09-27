#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

MEDBASE_VER = 1

def medbaseversion():
    return 'b' + str(MEDBASE_VER)
                     
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