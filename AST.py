class Node(object):
    pass

class Expression(Node):
    pass

#DONE
class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions

#DONE
class Instructions(Node):
    def __init__(self):
        self.instructions = []


class Error(Node):
    def __init__(self):
        pass

#DONE
class BreakInstruction(Node):
    def __init__(self, line):
        self.line = line

#DONE
class ContinueInstruction(Node):
    def __init__(self, line):
        self.line = line

#DONE
class ReturnInstruction(Node):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

#DONE
class PrintInstructions(Node): #DONE
    def __init__(self, expressions_list, line):
        self.expressions_list = expressions_list
        self.line = line

#DONE
class Assignment(Node):
    def __init__(self, variable, expression, line):
        self.variable = variable
        self.expression = expression
        self.line = line

#DONE
class BinaryExpression(Expression):
    def __init__(self, expression_left, operator, expression_right, line):
        self.expression_left = expression_left
        self.expression_right = expression_right
        self.operator = operator
        self.line = line

#DONE
class ZerosInitialization(Expression):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

#DONE
class OnesInitialization(Expression):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

#DONE
class EyeInitialization(Expression):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

#DONE
class MatrixAssignment(Node):
    def __init__(self, variable, expression_list, line):
        self.variable = variable
        self.expression_list = expression_list
        self.line = line


class CompoundAssignment(Node):
    def __init__(self, variable, operator, expression, line):
        self.variable = variable
        self.operator = operator
        self.expression = expression
        self.line = line


class IfInstruction(Node):
    def __init__(self, condition, instruction, line):
        self.condition = condition
        self.instruction = instruction
        self.line = line


class IfElseInstruction(Node):
    def __init__(self, condition, instruction, else_instruction, line):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction
        self.line = line


class WhileInstruction(Node):
    def __init__(self, condition, instruction, line):
        self.condition = condition
        self.instruction = instruction
        self.line = line


class ForInstruction(Node):
    def __init__(self, variable, start, end, instruction, line):
        self.variable = variable
        self.start = start
        self.end = end
        self.instruction = instruction
        self.line = line


class CompoundInstruction(Node):
    def __init__(self, instructions, line):
        self.instructions = instructions
        self.line = line

#DONE
class Constant(Expression):
    def __init__(self, value, type, line):
        self.value = value
        self.type = type
        self.line = line

#DONE
class Variable(Expression):
    def __init__(self, name, line):
        self.name = name
        self.line = line

#DONE
class ListOfExpressions(Expression):
    def __init__(self, line):
        self.expression_list = []
        self.line = line

    def append_expression(self, e):
        self.expression_list.append(e)

    def flat_expressions(self, expression_list, e):
        self.expression_list = list(expression_list)
        self.expression_list.append(e)

#DONE
class ListsOfExpressions(Expression):
    def __init__(self, line):
        self.expression_lists = []
        self.line = line

    def append_expression(self, e):
        self.expression_lists.append(e)

    def flat_expressions(self, expression_lists, e):
        self.expression_lists = list(expression_lists)
        self.expression_lists.append(e)

#DONE
class NegUnaryExpression(Expression):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line


class TransUnaryExpression(Expression):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

#DONE
class MatrixElement(Node):
    def __init__(self, variable, row, column, line):
        self.variable = variable
        self.row = row
        self.column = column
        self.line = line
