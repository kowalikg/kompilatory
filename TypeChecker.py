#!/usr/bin/python
import AST
from OperationsTypes import result_types
from SymbolTable import SymbolTable, VariableSymbol


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
            print("Error in line: " + node.line + ": illegal operation")
        return expected_type

    def visit_Variable(self, node):
        definition = self.symbol_table.getGlobal(node.name)
        if definition is None:
            print("Error in line: " + node.line + ": unknown variable")
        else:
            return definition.type

    def visit_Constant(self, node):
        return node.type

    def visit_Assignment(self, node):

        type1 = self.visit(node.expression)
        if (isinstance(node.variable, AST.Variable)):
            self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, type1))
            self.visit(node.variable)
        # else:
        #     self.symbol_table.put(node.variable.variable, VariableSymbol(node.variable.variable, type1))
        #     self.visit(node.variable.variable)

    def visit_PrintExpression(self, node):
        for expression in node.expression_list:
            self.visit(expression)

    def visit_ListOfExpressions(self, node):
        for expression in node.expression_list:
            self.visit(expression)

    def visit_Break(self, node):
        if self.loop_nest <= 0:
            print("Error in line: " + node.line + ": break outside the loop")
        return None

    def visit_Continue(self, node):
        if self.loop_nest <= 0:
            print("Error in line: " + node.line + ": continue outside the loop")
        return None

    def visit_IfInstruction(self, node):
        inner_scope = SymbolTable("if", self.symbol_table)
        self.symbol_table = inner_scope

        self.visit(node.condition)
        self.visit(node.instruction)

        self.symbol_table = self.symbol_table.parent

    def visit_IfElseInstruction(self, node):
        inner_scope = SymbolTable("ifelse", self.symbol_table)
        self.symbol_table = inner_scope

        self.visit(node.condition)
        self.visit(node.instruction)
        self.visit(node.else_instruction)

        self.symbol_table = self.symbol_table.parent

    def visit_ReturnInstruction(self, node):
        if (function):
            self.visit(node.expression)
        else:
            print("Error in line: " + node.line + ": return outside the function")

