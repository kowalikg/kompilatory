#!/usr/bin/python
from Exceptions import DuplicationError
from enum import Enum

class Symbol():
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #
    def __str__(self):
        return str(self.type)


class Matrix(object):
    def __init__(self, dim_X, dim_Y):
        self.dim_X = dim_X
        self.dim_Y = dim_Y

    def __str__(self):
        return "Matrix"


class BadType(object):
    def __str__(self):
        return "bad type"


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def getParentScope(self):
        return self.parent

    def get(self, name):
        try:
            symbol = self.symbols[name]
            return symbol
        except:
            if self.parent is not None:
                return self.getParentScope().getGlobal(name)
            return None


