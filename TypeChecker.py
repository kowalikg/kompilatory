#!/usr/bin/python
import AST
from OperationsTypes import result_types, Matrix as M
from SymbolTable import SymbolTable, VariableSymbol

from AST import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)



    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.loop_nest = 0
        self.function = False
        self.curr_type = ""

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BinaryExpression(self, node):
        type_left = self.visit(node.expression_left)
        type_right = self.visit(node.expression_right)
        operator = node.operator

        expected_type = result_types[operator][type_left][type_right]
        if not expected_type:
            print("Error in line: " + str(node.line) + ": illegal operation")
        return expected_type

    def visit_NegUnaryExpression(self, node):
        type = self.visit(node.expression)
        type = result_types['-'][type]
        if not type:
            print("Error in line: " + str(node.line) + ": invalid unary negation type: " + type)
        return type

    def visit_TransUnaryExpression(self, node):
        t = self.visit(node.expression)
        type = result_types['\''][t.__class__.__name__]
        if not type:
            print("Error in line: " + str(node.line) + ": invalid transposition type: " + t)
        return type

    def visit_Variable(self, node):
        definition = self.symbol_table.getGlobal(node.name)
        if definition is None:
            print("Error in line: " + str(node.line) + ": unknown variable")
        else:
            return definition

    def visit_Constant(self, node):
        return node.type

    def visit_Assignment(self, node):
        type = self.visit(node.expression)
        var = self.symbol_table.getGlobal(node.variable.name)
        if var is not None:
            print("reassigning variable: " + str(var) + "with type: " + str(type))

        self.symbol_table.put(node.variable.name, type)
        self.visit(node.variable)

    def visit_MatrixElement(self, node):

        x = self.visit(node.row)
        y = self.visit(node.column)

        if x == 'int' and y == 'int':
            id = node.variable
            row = node.row
            column = node.column
            t = self.symbol_table.getGlobal(id)
            if row.value >= t.dim_Y or column.value >= t.dim_X:
                print("Error in line: " + str(node.line) + ": index out of bound")
        else: print("Error in line: " + str(node.line) + ": index is not int")

    def visit_ListsOfExpressions(self, node):
        size = -1
        for expression_list in node.expression_lists:
            next_size = self.visit(expression_list)
            if size == -1:
                size = next_size
            if size != next_size:
                print("Error in line: " + str(node.line) + ": Different rows size " + str(size) + " and " + str(next_size))
        return M(size, len(node.expression_lists))

    def visit_MatrixAssignment(self, node):
        var = self.symbol_table.getGlobal(node.variable.name)
        if var is not None:
            print("reassigning variable: " + str(var) + "with type: " + str(M.__name__))

        self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, M.__name__))
        self.visit(node.expression_list)

    def visit_PrintExpression(self, node):
        for expression in node.expression_list:
            self.visit(expression)

    def visit_ListOfExpressions(self, node):
        for expression in node.expression_list:
            self.visit(expression)
        return len(node.expression_list)

    def visit_PrintInstructions(self, node):
        self.visit(node.expressions_list)

    def visit_ZerosInitialization(self, node):
        type = self.visit(node.expression)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": cannot initialize zeros with " + type)
        dim = self.get_dim(node.expression)
        return M(dim, dim)

    def visit_OnesInitialization(self, node):
        type = self.visit(node.expression)
        if type != "int":
            print("Error in line: " + str(node.line) + ": cannot initialize ones with " + type)
        dim = self.get_dim(node.expression)
        return M(dim, dim)

    def visit_EyeInitialization(self, node):
        type = self.visit(node.expression)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": cannot initialize eye with " + type)
        dim = self.get_dim(node.expression)
        return M(dim, dim)


    def visit_BreakInstruction(self, node):
        if self.loop_nest <= 0:
            print("Error in line: " + str(node.line) + ": break outside the loop")
        return None

    def visit_ContinueInstruction(self, node):
        if self.loop_nest <= 0:
            print("Error in line: " + str(node.line) + ": continue outside the loop")
        return None

    def visit_IfInstruction(self, node):
        self.visit(node.condition)
        inner_scope = SymbolTable(self.symbol_table, "if")
        self.symbol_table = inner_scope
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.getParentScope()

    def visit_IfElseInstruction(self, node):
        self.visit(node.condition)
        inner_scope = SymbolTable(self.symbol_table, "if")
        self.symbol_table = inner_scope
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.getParentScope()
        inner_scope = SymbolTable(self.symbol_table, "else")
        self.symbol_table = inner_scope
        self.visit(node.else_instruction)
        self.symbol_table = self.symbol_table.getParentScope()
        return None

    def visit_WhileInstruction(self, node):
        inner_scope = SymbolTable(self.symbol_table, 'while')
        self.symbol_table = inner_scope
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.getParentScope()
        return None

    def visit_ForInstruction(self, node):
        inner_scope = SymbolTable(self.symbol_table, 'while')
        self.symbol_table = inner_scope

        type = self.visit(node.start)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": invalid range type: " + str(type))
        type = self.visit(node.end)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": invalid range type: " + str(type))

        self.symbol_table.put(node.variable.name, type)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.getParentScope()
        return None

    def visit_ReturnInstruction(self, node):
        if (function):
            self.visit(node.expression)
        else:
            print("Error in line: " + str(node.line) + ": return outside the function")

    def get_dim(self, val):
        if isinstance(val, Constant):
            return val.value
        elif isinstance(val, Variable):
            return val.name
        elif isinstance(val, int):
            return val