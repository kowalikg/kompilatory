#!/usr/bin/python
import AST
from OperationsTypes import result_types
from SymbolTable import SymbolTable


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

    def visit_Program(self, node):
        self.visit(node.instructions)

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
        variable_status = self.symbol_table.getGlobal(node.variable)



