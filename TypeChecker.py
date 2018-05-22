#!/usr/bin/python
import AST
from OperationsTypes import result_types, Matrix as M, getMatrixResult, Matrix
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

        if not isinstance(type_left, Matrix):
            if isinstance(type_left, VariableSymbol):
                if isinstance(type_right, VariableSymbol):
                    expected_type = result_types[operator][type_left.type][type_right.type]
                else:
                    expected_type = result_types[operator][type_left.type][type_right]
            else:
                if isinstance(type_right, VariableSymbol):
                    expected_type = result_types[operator][type_left][type_right.type]
                else:
                    expected_type = result_types[operator][type_left][type_right]

            if not expected_type:
                print("Error in line: " + str(node.line) + ": illegal operation")
                return None
            return expected_type
        else:
            matrix_left = self.symbol_table.getGlobal(type_left.name)
            if not isinstance(type_right, Matrix):
                print("Error in line: " + str(node.line) + ": illegal operation")
            else:
                if type_right.dim_X != matrix_left.dim_X or type_right.dim_Y != matrix_left.dim_Y:
                    print("Error in line: " + str(node.line) + ": illegal operation on different matrix size")
                return M(type_right.dim_X, type_right.dim_Y)

    def visit_NegUnaryExpression(self, node):
        t = self.visit(node.expression)
        if isinstance(t, VariableSymbol):
            type = result_types['-'][t.type.__class__.__name__]
        else:
            type = result_types['-'][t]
        if not type:
            print("Error in line: " + str(node.line) + ": invalid unary negation type")
        return type

    def visit_TransUnaryExpression(self, node):
        t = self.visit(node.expression)
        type = result_types['\''][t.type.__class__.__name__]
        if not type:
            print("Error in line: " + str(node.line) + ": invalid transposition type")
        return type

    def visit_Variable(self, node):
        definition = self.symbol_table.getGlobal(node.name)
        if definition is None:
            print("Error in line: " + str(node.line) + ": unknown variable")
        else:
            return definition

    def visit_Constant(self, node):
        return node.type

    def visit_CompoundInstruction(self, node):
        self.visit(node.instructions)

    def visit_Assignment(self, node):
        type = self.visit(node.expression)

        if isinstance(node.variable, MatrixElement):
            var = self.symbol_table.getGlobal(node.variable.variable)
            if var is None:
                print("Error in line " + str(
                    node.line) + ": no matrix with that name")
            else:
                self.visit(node.variable)

        else:
            var = self.symbol_table.getGlobal(node.variable.name)
            if var is not None:
                print("Warning in line " + str(node.line) + ": previously declared variable, now reassigning with type: " + str(
                type))

            self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, type))

            self.visit(node.variable)

    def visit_CompoundAssignment(self, node):
        variable = self.symbol_table.getGlobal(node.variable.name)
        expression = self.visit(node.expression)
        operator = node.operator
        if not isinstance(variable, Matrix):
            expected_type = result_types[operator][variable.type][expression.type]
            if not expected_type:
                print("Error in line: " + str(node.line) + ": illegal operation")
                return None
            return expected_type
        else:
            matrix_left = self.symbol_table.getGlobal(node.variable.name)
            if not isinstance(expression, Matrix):
                print("Error in line: " + str(node.line) + ": illegal operation")
                return None
            else:
                if expression.dim_X != matrix_left.dim_X or expression.dim_Y != matrix_left.dim_Y:
                    print("Error in line: " + str(node.line) + ": illegal operation on different matrix size")
                    return None
                return M(matrix_left.dim_X, matrix_left.dim_Y)


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
            print("Warning in line " + str(
                node.line) + ": previously declared variable, now reassigning with type: " + str(
                M.__name__))
        matrix = self.visit(node.expression_list)
        matrix.set_name(node.variable.name)
        self.symbol_table.put(node.variable.name, matrix)

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
        #print('type')

        type = self.visit(node.expression)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": cannot initialize zeros with " + type)
            return None
        dim = self.get_dim(node.expression)
        return M(dim, dim)

    def visit_OnesInitialization(self, node):
        type = self.visit(node.expression)
        if type != "int":
            print("Error in line: " + str(node.line) + ": cannot initialize ones with " + type)
            return None
        dim = self.get_dim(node.expression)
        return M(dim, dim)

    def visit_EyeInitialization(self, node):
        type = self.visit(node.expression)
        if type != 'int':
            print("Error in line: " + str(node.line) + ": cannot initialize eye with " + type)
            return None
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
        self.loop_nest = self.loop_nest + 1
        inner_scope = SymbolTable(self.symbol_table, 'while' + str(self.loop_nest))
        self.symbol_table = inner_scope
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.getParentScope()
        self.loop_nest = self.loop_nest - 1
        return None

    def visit_ForInstruction(self, node):
        self.loop_nest = self.loop_nest + 1
        inner_scope = SymbolTable(self.symbol_table, 'for' + str(self.loop_nest))
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
        self.loop_nest = self.loop_nest - 1
        return None

    def visit_ReturnInstruction(self, node):
        self.visit(node.expression)
        if self.symbol_table.getParentScope() is None:
            print("Error in line: " + str(node.line) + ": return in outer of scope")
        return None

    def get_dim(self, val):
        if isinstance(val, Constant):
            return val.value
        elif isinstance(val, Variable):
            return val.name
        elif isinstance(val, int):
            return val