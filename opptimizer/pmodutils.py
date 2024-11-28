from .Mod import *

def clean_mod_onprocess(self, fileToProcess, params, tokenData):
    tokenData = None
    return tokenData

def clean_mod_exec(self, params, tokenData):
    tokenData = None
    return tokenData

def m_clean(name='clean'):
    return Mod(name=name, func_exec=clean_mod_exec, func_onprocess=clean_mod_onprocess)

def mclean_func(self, fileToProcess, params, tokenData):
    tokenData = None
    return tokenData

mclean = Mod(name='mclean',func_onprocess=mclean_func)

###  INLINE MODULE for putting \n to result file
def newline_action(self):
    self.resultFileOpen()
    self.writeToResultFile('', semicolon=False, new_line = True)
    self.resultFileClose()

def newline_mod_onprocess(self, fileToProcess, params, tokenData):
    newline_action(self)
    return tokenData

def newline_mod_exec(self, params, tokenData):
    newline_action(self)
    return tokenData

def m_newline(name='newline'):
    return Mod(name=name, func_exec=newline_mod_exec, func_onprocess=newline_mod_onprocess)