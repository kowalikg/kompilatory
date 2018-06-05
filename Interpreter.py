import numpy
from numpy.linalg import LinAlgError

import AST
from Memory import *
from Exceptions import *
from visit import *
import sys


def multiply(x, y):
    return [[elem * x for elem in row] for row in y]


def divide(x, y):
    return [[elem / x for elem in row] for row in y]


def add_matrices(x, y):
    A = numpy.matrix(x)
    B = numpy.matrix(y)
    return A + B


def sub_matrices(x, y):
    A = numpy.matrix(x)
    B = numpy.matrix(y)
    return A - B


def mul_matrices(x, y):
    A = numpy.matrix(x)
    C = []
    rows = int(A.shape[0])
    columns = int(A.shape[1])
    for i in range(0, rows):
        inner = []
        for j in range(0, columns):
            result = x[i][j] * y[i][j]
            inner.append(result)
        C.append(inner)
    return C


def div_matrices(x, y):
    A = numpy.matrix(x)
    C = []
    rows = int(A.shape[0])
    columns = int(A.shape[1])
    for i in range(0, rows):
        inner = []
        for j in range(0, columns):
            if y[i][j] == 0: return [[]]
            result = x[i][j] / y[i][j]
            inner.append(result)
        C.append(inner)
    return C

def mul_invert(x, y):
    A = numpy.matrix(x)
    try:
        B = numpy.linalg.inv(y)
        return numpy.array(numpy.matmul(A, B)).tolist()
    except LinAlgError:
        return [[]]


sys.setrecursionlimit(10000)

result = {
       "+": (lambda x, y: x + y),
       "+=": (lambda x, y: x + y),
       "-": (lambda x, y: x - y),
       "-=": (lambda x, y: x - y),
       "*": (lambda x, y: x * y),
       "*=": (lambda x, y: x * y),
       "/": (lambda x, y: x / y),
       "/=": (lambda x, y: x / y),
       "^": (lambda x, y: x ^ y),
       "==": (lambda x, y: x == y),
       "!=": (lambda x, y: x != y),
       ">": (lambda x, y: x > y),
       "<": (lambda x, y: x < y),
       "<=": (lambda x, y: x <= y),
       ">=": (lambda x, y: x >= y)}

matrix_result = {
    "*": (lambda x, y: multiply(x,y)),
    '/': (lambda x, y: divide(x,y))
}

matrix_matrix_result = {
    '*': (lambda x, y: numpy.array(numpy.matmul(x,y)).tolist()),
    '*=': (lambda x, y: numpy.array(numpy.matmul(x,y)).tolist()),
    '/': (lambda x, y: mul_invert(x,y)),
    '/=': (lambda x, y: mul_invert(x,y)),
    '+': (lambda x, y: add_matrices(x,y).tolist()),
    '+=': (lambda x, y: add_matrices(x,y).tolist()),
    '.+': (lambda x, y: add_matrices(x,y).tolist()),
    '-': (lambda x, y: sub_matrices(x,y).tolist()),
    '-=': (lambda x, y: sub_matrices(x,y).tolist()),
    '.-': (lambda x, y: sub_matrices(x,y).tolist()),
    '.*': (lambda x, y: mul_matrices(x,y)),
    './': (lambda x, y: div_matrices(x,y)),

}

class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.MatrixElement)
    def visit(self, node):
        row = node.row.accept(self)
        column = node.column.accept(self)
        return row, column

    @when(AST.Assignment)
    def visit(self, node):
        expression = node.expression.accept(self)
        variable = node.variable.accept(self)

        if type(variable) is tuple:
            M = self.memory_stack.get(node.variable.variable)
            M[variable[0]][variable[1]] = expression
            self.memory_stack.set(node.variable.variable, M)
        else:
            if self.memory_stack.get(node.variable.name) is None:
                self.memory_stack.insert(node.variable.name, expression)
            else:
                self.memory_stack.set(node.variable.name, expression)

    @when(AST.MatrixAssignment)
    def visit(self, node):
        expression_list = node.expression_list.accept(self)
        if self.memory_stack.get(node.variable.name) is None:
            self.memory_stack.insert(node.variable.name, expression_list)
        else:
            self.memory_stack.set(node.variable.name, expression_list)

    @when(AST.CompoundAssignment)
    def visit(self, node):
        expression = node.expression.accept(self)
        variable = node.variable.accept(self)

        if type(variable) is tuple:
            M = self.memory_stack.get(node.variable.variable)
            element = M[variable[0]][variable[1]]
            M[variable[0]][variable[1]] = result[node.operator](element,expression)
            self.memory_stack.set(node.variable.variable, M)
        elif type(variable) is list:
            self.memory_stack.set(node.variable.name, matrix_matrix_result[node.operator](variable, expression))
        else:
            self.memory_stack.set(node.variable.name, result[node.operator](variable, expression))

    @when(AST.ZerosInitialization)
    def visit(self, node):
        expression = node.expression.accept(self)
        zeros = [[0 for column in range(expression)] for row in range(expression)]
        return zeros

    @when(AST.OnesInitialization)
    def visit(self, node):
        expression = node.expression.accept(self)
        ones = [[1 for column in range(expression)] for row in range(expression)]
        return ones

    @when(AST.EyeInitialization)
    def visit(self, node):
        expression = node.expression.accept(self)
        eye = [[0 for column in range(expression)] for row in range(expression)]
        for i in range(0, expression - 1):
            eye[i][i] = 1
        return eye

    @when(AST.BinaryExpression)
    def visit(self, node):
        r1 = node.expression_left.accept(self)
        r2 = node.expression_right.accept(self)
        if type(r1) is not list and type(r2) is not list:
            return result[node.operator](r1, r2)
        else:
            if type(r1) is not list and type(r2) is list:
                return matrix_result[node.operator](r1,r2)
            elif type(r1) is list and type(r2) is not list:
                return matrix_result[node.operator](r2, r1)
            else:
                return matrix_matrix_result[node.operator](r1, r2)

    @when(AST.NegUnaryExpression)
    def visit(self, node):
        expression = node.expression.accept(self)
        if type(expression) is list: #czyli tak naprawde macierz
            negated = []
            for row in expression:
                inner = []
                for element in row:
                    inner.append(-element)
                negated.append(inner)
            return negated
        return - expression

    @when(AST.TransUnaryExpression)
    def visit(self, node):
        expression = node.expression.accept(self)
        return [list(i) for i in zip(*expression)]


    @when(AST.Constant)
    def visit(self, node):

        if node.type == 'int':
            return int(node.value)
        elif node.type == 'float':
            return float(node.value)
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ForInstruction)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)

        if self.memory_stack.get(node.variable.name) is None:
            self.memory_stack.insert(node.variable.name, start)
        else:
            self.memory_stack.set(node.variable.name, start)

        while self.memory_stack.get(node.variable.name) < end:
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

            iterated = self.memory_stack.get(node.variable.name)
            iterated = iterated + 1
            self.memory_stack.set(node.variable.name, iterated)

    @when(AST.CompoundInstruction)
    def visit(self, node):
        compound_memory = Memory("compound")
        self.memory_stack.push(compound_memory)
        try:
            node.instructions.accept(self)
        finally:
            self.memory_stack.pop()

    @when(AST.PrintInstructions)
    def visit(self, node):
        expressions = node.expressions_list.accept(self)
        printed = []
        for expression in expressions:
            if expression is not None:
                printed.append(str(expression))
        print(', '.join(printed))

    @when(AST.ListOfExpressions)
    def visit(self, node):
        list = []
        for expression in node.expression_list:
            list.append(expression.accept(self))

        return list

    @when(AST.ListsOfExpressions)
    def visit(self, node):
        list = []
        for expression_list in node.expression_lists:
            list.append(expression_list.accept(self))

        return list

    @when(AST.ReturnInstruction)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.IfInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)

    @when(AST.IfElseInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        else:
            return node.else_instruction.accept(self)