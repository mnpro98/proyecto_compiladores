import ply.lex as lex
import ply.yacc as yacc


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'program': 'PROGRAM',
    'int': 'INT',
    'float': 'FLOAT',
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
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
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
    '''vars : tipo vars_a SC'''


def p_vars_a(p):
    '''vars_a : vars_b
            | vars_b COMMA vars_a'''

def p_vars_b(p):
    '''vars_b : ID
            | ID EQ var_cte'''


def p_vars_vect_mat(p):
    '''vars_vect_mat : tipo ID vars_vect_mat_a SC
                    | tipo ID vars_vect_mat_a vars_vect_mat_a SC'''


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
    '''bloque : OB bloquea CB'''


def p_bloque_a(p):
    '''bloque_a : estatuto
                | bloque_b'''


def p_bloque_b(p):
    '''bloque_b : bloque_a
                | empty'''


def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | llamada
                | while
                | for'''


def p_expresion(p):
    '''expresion : m_exp
                | m_exp expresion_a m_exp'''


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
    '''for : OB asignacionsencilla SC expresion asignacionsencilla CP bloque'''


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
            | vars
            | vars_vect_mat
            | llamada'''


def p_classcreate(p):
    '''classcreate : CLASS CLASS_ID OB classcreate_a function classcreate_c CB'''


def p_classcreate_a(p):
    '''classcreate_a : vars
                    | vars_vect_mat
                    | classcreate_b'''


def p_classcreate_b(p):
    '''classcreate_b : classcreate_a
                    | empty'''


def p_classcreate_c(p):
    '''classcreate_c : function classcreate_d
                    | classcreate_d'''


def p_classcreate_d(p):
    '''classcreate_d : classcreate_c
                    | empty'''


def p_condicion(p):
    '''condicion : IF OP expresion CP bloque condiciona SC'''


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


def p_asignacion_a(p):
    '''asignacion_a : OSB exp CSB
                    | empty'''


def p_asignacionsencilla(p):
    '''asignacionsencilla : ID EQ expresion'''


def p_function(p):
    '''function : function_a ID OP function_b CP bloque'''


def p_function_a(p):
    '''function_a : VOID
                | tipo_simple'''


def p_function_b(p):
    '''function_b : tipo_simple ID
                | tipo_simple ID COMMA function_b
                | empty'''


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()


try:
    f = open("correct.txt", "r")
    s = f.read()

except EOFError:
    print("Sintax Error")
yacc.parse(s)
