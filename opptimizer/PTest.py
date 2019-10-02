#!/usr/bin/env python

# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

import sys
from socket import *
import time
import os
from .opp import *
from .pcons import *
from .PLog import *
import imp

MEDTEST_VER = 1

class PTest:
	def __init__(self, testName = None, context = None, params = None):
		self.name = testName
		self.context = context
		self.params = params
		self.modules = []
		self.execDir = None
		self.log = None
		return

	def version(self):
		return 't' + str(MEDTEST_VER)
	
	def addModule(self, module):
		self.modules.append(module)
		
	def getModules(self):
		return self.modules
	
	def setExecDir(self, directory):
		self.execDir = directory
	
	def getExecDir(self):
		return self.execDir
		



def connectToServiceITK(self):
	print('connectToServiceITK')
	itkServiceSocket = socket(AF_INET, SOCK_STREAM)
	itkServiceSocket.connect(('localhost', 3355))
	return itkServiceSocket
	
	

		