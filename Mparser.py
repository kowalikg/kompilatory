#!/usr/bin/python
import re

import scanner
import AST


class MParser:
    def __init__(self, scanner):
        self.scanner = scanner

    tokens = scanner.Scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("nonassoc", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
        ("nonassoc", 'LESS', 'GREATER', "LESSEQ", "GREATEREQ", "EQ", "NOTEQ"),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left",  '*', '/', "DOTMUL", "DOTDIV"),
        ("right", 'NEGATION'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : instructions"""
        program = AST.Program(p[1])
        p[0] = program

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[1].instructions.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Instructions()
            p[0].instructions.append(p[1])

    def p_instruction(self, p):
        """instruction :  return_instruction
                    | break_instruction
                    | continue_instruction
                    | print_instruction
                    | while_instruction
                    | for_instruction
                    | if_instruction
                    | assignment_instruction
                    | compound_assignment_instruction
                    | compound_instruction

        """
        #instrukcja = ktoras z tych
        p[0] = p[1]

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p[2], p.lineno(1)) # bez return

    def p_break_instruction(self, p):
        """break_instruction : BREAK ';' """
        p[0] = AST.BreakInstruction(p.lineno(1))


    def p_continue_instr(self,p):
        """continue_instruction : CONTINUE ';' """
        p[0] = AST.ContinueInstruction(p.lineno(1))

    def p_print_instruction(self, p):
        """print_instruction :    PRINT expression_list ';'
                                | PRINT '"' expression_list '"' ';'
        """
        if len(p) == 6:
            p[0] = AST.PrintInstructions(p[3], p.lineno(1))
        else:
            p[0] = AST.PrintInstructions(p[2], p.lineno(1))


    def p_assignment_instruction(self, p):
        """assignment_instruction : variable_expression '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[3], p.lineno(1))

    def p_matrix_assignment(self, p):
        """assignment_instruction : variable_expression '=' '[' expression_lists ']' ';'"""
        p[0] = AST.MatrixAssignment(p[1], p[4], p.lineno(1))

    def p_binary_expression(self, p):
        """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression EQ expression
                  | expression NOTEQ expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression LESSEQ expression
                  | expression GREATEREQ expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression

        """
        p[0] = AST.BinaryExpression(p[1], p[2], p[3], p.lineno(1))

    def p_neg_unary_expression(self, p):
        """expression : '-' expression %prec NEGATION """
        p[0] = AST.NegUnaryExpression(p[2], p.lineno(1))


    def p_trans_unary_expression(self, p):
        """expression : expression "'" """
        p[0] = AST.TransUnaryExpression(p[1], p.lineno(1))


    def p_matrix_initialization_zeros(self, p):
        """expression : ZEROS '(' expression ')'"""
        p[0] = AST.ZerosInitialization(p[3], p.lineno(1))


    def p_matrix_initialization_ones(self, p):
        """expression : ONES '(' expression ')'"""
        p[0] = AST.OnesInitialization(p[3], p.lineno(1))


    def p_matrix_initialization_eye(self, p):
        """expression : EYE '(' expression ')'"""
        p[0] = AST.EyeInitialization(p[3], p.lineno(1))


    def p_compound_assignment(self, p):
        """compound_assignment_instruction : variable_expression ADDASSIGN expression ';'
                            | variable_expression SUBASSIGN expression ';'
                            | variable_expression MULASSIGN expression ';'
                            | variable_expression DIVASSIGN expression ';'
                            """
        p[0] = AST.CompoundAssignment(p[1], p[2], p[3], p.lineno(1))

    def p_if_instruction(self, p):
        """if_instruction : IF '(' condition ')' instruction %prec IF
                          | IF '(' condition ')' instruction ELSE instruction"""
        if len(p) == 8:
            p[0] = AST.IfElseInstruction(p[3], p[5], p[7], p.lineno(1))
        else:
            p[0] = AST.IfInstruction(p[3], p[5], p.lineno(1))

    def p_while_instruction(self, p):
        """while_instruction : WHILE '(' condition ')' instruction"""
        p[0] = AST.WhileInstruction(p[3], p[5], p.lineno(1))

    def p_for_instruction(self, p):
        """for_instruction : FOR variable_expression '=' expression ':' expression  instruction """
        p[0] = AST.ForInstruction(p[2], p[4], p[6], p[7], p.lineno(1))

    def p_compound_instruction(self, p):
        """compound_instruction : '{' instructions '}' """
        p[0] = AST.CompoundInstruction(p[2], p.lineno(1))

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_constant(self, p):
        """expression : FLOATNUM
                      | INTNUM
                      | STRING
        """
        if re.match(r"\d*\.\d+", str(p[1])):
            type = 'float'
        elif re.match(r"\d+", str(p[1])):
            type = 'int'
        else:
            type = 'string'
        p[0] = AST.Constant(p[1], type, p.lineno(1))


    def p_variable_expression(self, p):
        """expression : variable_expression"""
        p[0] = p[1]

    def p_ID(self, p):
        """variable_expression : ID
                                | ID '[' expression ',' expression ']'"""
        if len(p) == 2:
            p[0] = AST.Variable(p[1], p.lineno(1))
        else:
            p[0] = AST.MatrixElement(p[1], p[3], p[5], p.lineno(1))

    def p_paren_expression(self, p):
        """expression : '(' expression ')'"""
        p[0] = p[2]

    def p_expression_lists(self, p):
        """expression_lists : expression_lists ';' expression_list
                            | expression_list """
        p[0] = AST.ListsOfExpressions(p.lineno(1))
        if len(p) == 4:
            p[0].flat_expressions(p[1].expression_lists, p[3])
        else:
            p[0].append_expression(p[1])

    def p_expression_list(self, p):
        """expression_list : expression_list ',' expression
                           | expression """
        p[0] = AST.ListOfExpressions(p.lineno(1))
        if len(p) == 4:
            p[0].flat_expressions(p[1].expression_list, p[3])
        else:
            p[0].append_expression(p[1])





