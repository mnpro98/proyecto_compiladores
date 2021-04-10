import ply.lex as lex
import ply.yacc as yacc

amount = 0

reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'or': 'OR',
    'and': 'AND',
    'program': 'PROGRAM',
    'class': 'CLASS',
    'void': 'VOID',
    'for': 'FOR',
    'while': 'WHILE',
    'dataframe': 'DATAFRAME',
    'file': 'FILE'
}


tokens = [
    'DIGIT', 'DIGITS', 'LETTER',
    'CAPT', 'ID', 'CLASS_ID',
    'OB', 'CB', 'OP', 'CP',
    'OSB', 'CSB', 'GT', 
    'LT', 'GE', 'LE',
    'NE', 'EQ', 'EQEQ',
    'ADD', 'SUB', 'DIV',
    'MULT', 'SC', 'COL',
    'POINT', 'COMMA', 'CTE_I',
    'CTE_F', 'CTE_CHAR', 'CTE_STRING'
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
t_FILE = r'file'
t_DIGIT = r'[0-9]'
t_DIGITS = r'[0-9]+'
t_LETTER = r'[A-Za-z]'
t_CAPT = r'[A-Z]'
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
t_EQEQ = r'\=\='
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
    r'[a-z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_CLASS_ID(t):
    r'[A-Z_][a-z_0-9]*'
    t.type = reserved.get(t.value, 'CLASS_ID')    # Check for reserved words
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


def p_programa(p):
    '''programa : PROGRAM ID SC programa_a bloque'''
    print("apropiado")


def p_programa_a(p):
    '''programa_a : programa_b
                | programa_b programa_a'''


def p_programa_b(p):
    '''programa_b : vars
                | vars_vect_mat'''
#
#
def p_vars(p):
    '''vars : tiposimple vars_a SC
            | tipocompuesto vars_a SC'''


def p_vars_a(p):
    '''vars_a : vars_b
            | vars_b COMMA vars_a'''

def p_vars_b(p):
    '''vars_b : ID
            | ID EQ varcte'''


def p_vars_vect_mat(p):
    '''vars_vect_mat : tiposimple ID vars_vect_mat_a SC
                    | tiposimple ID vars_vect_mat_a vars_vect_mat_a SC'''


def p_vars_vect_mat_a(p):
    '''vars_vect_mat_a : OSB exp CSB'''


def p_m_exp(p):
    '''m_exp : term
            | term m_exp_a m_exp'''


def p_m_exp_a(p):
    '''m_exp_a : ADD
            | SUB'''


def p_term(p):
    '''term : fact
            | fact term_a term'''


def p_term_a(p):
    '''term_a : MULT
            | DIV'''


def p_tiposimple(p):
    '''tiposimple : INT
                | FLOAT
                | CHAR'''


def p_tipocompuesto(p):
    '''tipocompuesto : DATAFRAME
                    | ID
                    | FILE'''


def p_bloque(p):
    '''bloque : OB bloque_a CB'''
    print("bloque")


def p_bloque_a(p):
    '''bloque_a : estatuto bloque_a
                | estatuto
                | empty'''


def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | llamada
                | while
                | for
                | classcreate
                | vars
                | classdeclare
                | llamadafuncionclase
                | function'''


def p_expresion(p):
    '''expresion : m_exp
                | m_exp expresion_a m_exp'''
    print("expresion")


def p_expresion_a(p):
    '''expresion_a : LT
                | GT
                | NE
                | EQEQ
                | LE
                | GE'''


def p_varcte(p):
    '''varcte : ID
            | CTE_I
            | CTE_F'''


def p_while(p):
    '''while : WHILE OB expresion CB bloque'''


def p_exp(p):
    '''exp : and_exp exp_a'''


def p_exp_a(p):
    '''exp_a : OR
            | empty'''


def p_and_exp(p):
    '''and_exp : expresion and_exp_a'''


def p_and_exp_a(p):
    '''and_exp_a : AND
                | empty'''


def p_for(p):
    '''for : FOR OP asignacionsencilla SC expresion SC asignacionsencilla CP bloque'''


def p_llamada(p):
    '''llamada : ID OP llamada_a CP SC'''


def p_llamada_a(p):
    '''llamada_a : expresion llamada_b
                | CTE_STRING llamada_b
                | llamada_b'''


def p_llamada_b(p):
    '''llamada_b : COMMA llamada_a
                | empty'''


def p_fact(p):
    '''fact : OP exp CP
            | CTE_I
            | CTE_F
            | CTE_CHAR
            | ID
            | llamada'''


def p_classcreate(p):
    '''classcreate : CLASS CLASS_ID OB classcreate_a function classcreate_c CB'''
    print("classcreate")


def p_classcreate_a(p):
    '''classcreate_a : vars classcreate_a
                    | vars_vect_mat classcreate_a
                    | empty'''


def p_classcreate_c(p):
    '''classcreate_c : function classcreate_d
                    | classcreate_d'''


def p_classcreate_d(p):
    '''classcreate_d : classcreate_c
                    | empty'''


def p_condicion(p):
    '''condicion : IF OP expresion CP bloque condicion_a'''


def p_condicion_a(p):
    '''condicion_a : ELSE condicion_b bloque'''


def p_condicion_b(p):
    '''condicion_b : condicion
                | empty'''

def p_classdeclare(p):
    '''classdeclare : CLASS_ID ID SC'''


def p_llamadafuncionclase(p):
    '''llamadafuncionclase : ID POINT llamada'''


def p_asignacion(p):
    '''asignacion : ID asignacion_a asignacion_a EQ expresion SC'''
    print("asignacion")


def p_asignacion_a(p):
    '''asignacion_a : OSB exp CSB
                    | empty'''


def p_asignacionsencilla(p):
    '''asignacionsencilla : ID EQ expresion'''
    global amount
    amount += 1
    print(str(amount) + ".- asignacion sencilla")


def p_function(p):
    '''function : function_a ID OP function_b CP bloque'''


def p_function_a(p):
    '''function_a : VOID
                | tiposimple'''


def p_function_b(p):
    '''function_b : tiposimple ID
                | tiposimple ID COMMA function_b
                | empty'''


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()


try:
    f = open("./Tests/test_1", "r")
    s = f.read()

except EOFError:
    print("Sintax Error")
yacc.parse(s)
