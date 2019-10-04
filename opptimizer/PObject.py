#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

# Base class for optimizer objects


class PObject():
    def __init__(self, name = ""):
        self.name = name
    
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    