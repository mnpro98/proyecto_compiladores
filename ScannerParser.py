import ply.lex as lex
import ply.yacc as yacc


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT'
}


tokens = [
    'ID', 'DOTCOMMA', 'COMMA',
    'TWODOTS', 'LKEY', 'RKEY',
    'EQUALS', 'LPAREN', 'RPAREN',
    'GT', 'LT', 'NOTEQUAL',
    'PLUS', 'MINUS', 'TIMES',
    'DIVIDE', 'CTEI', 'CTEF', 'CTESTRING'
] + list(reserved.values())

# Tokens

t_PROGRAM = r'program'
t_DOTCOMMA = r'\;'
t_VAR = r'var'
t_COMMA = r'\,'
t_TWODOTS = r'\:'
t_INT = r'int'
t_FLOAT = r'float'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_PRINT = r'print'
t_CTESTRING = r'\".*\"'
t_GT = r'\>'
t_LT = r'\<'
t_NOTEQUAL = r'<>'
t_IF = r'if'
t_ELSE = r'else'
t_CTEI = r'-?[0-9]+'
t_CTEF = r'-?[0-9]+.[0-9]+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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
