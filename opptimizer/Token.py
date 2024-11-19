from .PObject import *

class Token(PObject):
    ''' Wrapper class for tokenData to pass betwen modules during execution'''
    def __init__(self, name = ''):
        PObject.__init__(self, name)
        pass