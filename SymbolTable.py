#!/usr/bin/python
from Exceptions import DuplicationError
from enum import Enum

class ScopeType(Enum):
    GLOBAL = 'globalScp'
    NESTED = 'nestedScp'
    LOOP = 'loopScp'
    FUNCTION = 'functionScp'

class Symbol():
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #

class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
        print(self.symbols[name].type)

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            symbol = self.symbols[name]
            return symbol
        except:
            return None
    #

    def getParentScope(self):
        return self.parent

    #

    def getGlobal(self, name):
        symbol = self.get(name)
        if symbol is None:
            if self.parent is not None:
                return self.parent.getGlobal(name)
            else:
                return None
        else:
            return symbol


