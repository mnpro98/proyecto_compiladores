import ply.lex as lex
import ply.yacc as yacc


reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char' : 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'or' : 'OR',
    'and' : 'AND',
    'program': 'PROGRAM',
    'class' : 'CLASS',
    'void' : 'VOID',
    'for' : 'FOR',
    'while' : 'WHILE',
    'dataframe' : 'DATAFRAME',
    'file' : 'FILE'
}


tokens = [
    'DIGIT', 'DIGITS', 'LETTER',
    'CAPT', 'ID', 'CLASSID',
    'OB', 'CB', 'OP', 'CP',
    'OSB', 'CSB', 'GT', 
    'LT', 'GE', 'LE',
    'NE', 'EQ', 'EQEQ',
    'ADD', 'SUB', 'DIV'
    'MULT', 'SC', 'COL',
    'POINT', 'COMMA', 'CTE_I',
    'CTE_F', 'CTE_CHAR', 'CTE.STRING'
] + list(reserved.values())

# Tokens

t_INT = r'int'
t_FLOAT = r'float'
t_CHAR = r'char'
t_IF = r'if'
t_ELSE = r'else'
t_OR = r'or'
t_AND = r'and'
t_PROGRAM = r'program'
t_CLASS = r'class'
t_VOID = r'void'
t_FOR = r'for'
t_WHILE = r'while'
t_DATAFRAME = r'dataframe'
t_FILE= r'file'
t_DIGIT = r'[0-9]'
t_DIGITS = r'[0-9]+'
t_LETTER = r'[A-Za-z]'
t_CAPT =  r'[A-Z]'
t_OB = r'\{'
t_CB = r'\}'
t_OP = r'\('
t_CP = r'\)'
t_OSB = r'\['
t_CSB = r'\]'
t_GT = r'\>'
t_LT = r'\<'
t_GE = r'>='
t_LE = r'<='
t_NE = r'!='
t_EQ = r'\='
t_EQEQ = r'=='
t_ADD = r'\+'
t_SUB = r'\-'
t_DIV = r'\/'
t_MULT = r'\*'
t_SC = r'\;'
t_COL = r'\:'
t_POINT = r'\.'
t_COMMA = r'\,'
t_CTE_I = r'-?[0-9]+'
t_CTE_F = r'-?[0-9]+.[0-9]+'
t_CTE_CHAR = r'\'.\''
t_CTE_STRING = r'\".*\"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
def t_CLASSID(t):
    r'[A-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()
names = {}


def p_program(p):
    '''program : PROGRAM ID DOTCOMMA a'''
    print("apropiado")


def p_a(p):
    '''a : vars bloque
        | bloque'''


def p_b(p):
    '''b : ID TWODOTS tipo DOTCOMMA
        | ID COMMA b
        | ID TWODOTS tipo DOTCOMMA b'''
#
#
def p_c(p):
    '''c : estatuto
        | estatuto c'''


def p_d(p):
    '''d : expresion
        | expresion COMMA d
        | CTESTRING
        | CTESTRING COMMA d'''


def p_e(p):
    '''e : GT exp
        | LT exp
        | NOTEQUAL exp'''


def p_f(p):
    '''f : bloque
        | bloque ELSE bloque'''


def p_vars(p):
    '''vars : VAR b'''


def p_tipo(p):
    '''tipo : INT
        | FLOAT'''


def p_bloque(p):
    '''bloque : LKEY RKEY
        | LKEY c RKEY'''


def p_estatuto(p):
    '''estatuto : asignacion
        | condicion
        | escritura'''


def p_asignacion(p):
    '''asignacion : ID EQUALS expresion DOTCOMMA'''


def p_escritura(p):
    '''escritura : PRINT LPAREN d RPAREN DOTCOMMA'''


def p_expresion(p):
    '''expresion : exp
        | exp e'''


def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN f DOTCOMMA'''


def p_exp(p):
    '''exp : termino
        | termino PLUS exp
        | termino MINUS exp'''


def p_termino(p):
    '''termino : factor
        | factor TIMES exp
        | factor DIVIDE exp'''


def p_factor(p):
    '''factor : LPAREN expresion RPAREN
        | PLUS varcte
        | MINUS varcte
        | varcte'''


def p_varcte(p):
    '''varcte : ID
        | CTEI
        | CTEF'''


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()


try:
    f = open("correct.txt", "r")
    s = f.read()

except EOFError:
    print("ERROR")
yacc.parse(s)
