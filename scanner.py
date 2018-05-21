import sys
import ply.lex as lex


class Scanner:
    def __init__(self, text):
        self.input = text
        self.lexer = lex.lex(object=self)
        self.lexer.input(text)

    # te które rozpoznajemy za pomocą jednego znaku
    literals = "+-*/=()[]{}:\',;\""

    # wyrażenia zarezerwowane
    reserved = {
        'if': 'IF', 'else': 'ELSE', 'for': 'FOR', 'while': 'WHILE',
        'break': 'BREAK', 'continue': 'CONTINUE', 'return': 'RETURN',
        'eye': 'EYE', 'zeros': 'ZEROS', 'ones': 'ONES',
        'print': 'PRINT'
    }

    # tokeny

    tokens = (
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
    'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
    'LESS', 'GREATER', "LESSEQ", "GREATEREQ", "NOTEQ", 'EQ',
    'IF', 'ELSE', 'FOR', 'WHILE',
    'BREAK', 'CONTINUE', 'RETURN',
    'EYE', 'ZEROS', 'ONES',
    'PRINT',
    'INTNUM', 'FLOATNUM', 'STRING',
    'ID'
    )

    # tokeny związane z operacjami arytmetycznymi na macierzach

    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\./'

    # tokeny do operatorow przypisania

    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='

    # tokeny do operatorow porownania

    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESSEQ = r'<='
    t_GREATEREQ = r'>='
    t_NOTEQ = r'\!='
    t_EQ = r'=='

    # ignorowanie bialych znakow i komenatrzy

    t_ignore = r' \t'
    t_ignore_COMMENT = r'\#.*' # koniec linii

    def find_tok_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        return token.lexpos - last_cr

    # oznaczanie wyrażenia zarezerwowanego lub domyślnie jako ID

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID') # któreś z rozpoznanych słów zastrzeżonych, domyslnie jako id
        return t

    # oznaczanie jako int

    def t_FLOATNUM(self, t):
        r'\d*\.\d+'
        t.value = float(t.value)
        return t

    # oznaczanie jako float
    def t_INTNUM(self, t):
        r'\d+' # te które nie zawierają kropki
        t.value = int(t.value)
        return t

# numerowanie linii

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

# sygnalizacja błędu


    def t_error(self, t):
        print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
        t.lexer.skip(1)

