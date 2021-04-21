import ply.lex as lex
import ply.yacc as yacc
from pprint import PrettyPrinter
from enum import Enum


class State(Enum):
    CLASS_CREATE = 1


curr_state = 0

pending_operators = []
pending_operands = []
corresponding_types = []
quad = []

semantics = {
    'int': {
        'int': {
            '+': 'int',
            '-': 'int'
        },
        'float': {},
        'char': {},
    },
    'float': {
        'int': {},
        'float': {},
        'char': {},
    },
    'char': {
        'int': {},
        'float': {},
        'char': {},
    },
}

expresion_helper = ""

token_dic = {
    "id": "",
    "tipo": "",
    "valor": "null"
}  # 0 - Tipo, 1 - id, 2 - valor

#llamada_dic = {}

funciones_dic = {
    "id": "",
    "tipo": ""
}

table = {
    "clases": {},
    "variables": {},
    "funciones": {}
}

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


def math_expression_1(id):
    pending_operands.append(id)
    corresponding_types.append(table['variables'][id]['tipo'])


def math_expression_2(operand):
    if operand == '+' or operand == '-':
        pending_operators.append(operand)
    else:
        print("ERROR: operands should be either + or -")


def math_expression_3(operand)
    if operand == '*' or operand == '/':
        pending_operators.append(operand)
    else:
        print("ERROR: operands should be either + or -")


def math_expression_4():
    if pending_operators[-1] == '+' or pending_operators[-1] == '-':
        right_operand = pending_operands.pop()
        right_type = corresponding_types.pop()
        left_operand = pending_operands.pop()
        left_type = corresponding_types.pop()
        operator = pending_operators.pop()
        result_type = semantics[left_type][right_type][operator]
        if result_type != 'ERROR':
            result = avail.next()
            _quad = [operator, left_operand, right_operand, result]
            quad.append(_quad)
            pending_operands.append(result)
            corresponding_types.append(result_type)
            # If any operand were a temporal space, return it to AVAIL
        else:
            print("ERROR: Type mismatch")


def math_expression_5():
    if pending_operators[-1] == '*' or pending_operators[-1] == '/':
        pass
        # = to #4 with *,/


def math_expression_6():
    pending_operators.append('|')


def math_expression_7():
    if pending_operators.pop() != '|':
        print("ERROR: False bottom mark missing.")


def math_expression_8(rel_op):
    pending_operators.append(rel_op)


def math_expression_9(rel_op):
    if pending_operators[-1] == rel_op:
        pass
        # = to #4 with *,/


def create_class_variable():
    pass


def state_switcher(arg):
    switcher = {
        State.CLASS_CREATE: create_class_variable
    }
    func = switcher.get(arg, "Invalid state")
    func()

#def llamada_dic_clear():
#    llamada_dic["id"] = ""
#    llamada_dic["parametros"] = ""

def funciones_dic_clear():
    funciones_dic["id"] = ""
    funciones_dic["tipo"] = ""

def token_dic_clear():
    token_dic["tipo"] = ""
    token_dic["id"] = ""
    token_dic["valor"] = "null"


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


    table['variables'][token_dic['id']] = {
        "tipo": token_dic['tipo'],
        "valor": token_dic['valor']
    }

    token_dic_clear()


def p_vars_a(p):
    '''vars_a : vars_b
            | vars_b COMMA vars_a'''

def p_vars_b(p):
    '''vars_b : ID
            | ID EQ varcte'''
    token_dic['id'] = p[1]


def p_vars_vect_mat(p):
    '''vars_vect_mat : tiposimple ID vars_vect_mat_a SC
                    | tiposimple ID vars_vect_mat_a vars_vect_mat_a SC'''


def p_vars_vect_mat_a(p):
    '''vars_vect_mat_a : OSB exp CSB'''


def p_m_exp(p):
    '''m_exp : term
            | term m_exp_a m_exp'''
    if len(p) < 3:
        math_expression_4()


def p_m_exp_a(p):
    '''m_exp_a : ADD
            | SUB'''
    math_expression_4()
#    global expresion_helper
#    expresion_helper = expresion_helper + p[1]


def p_term(p):
    '''term : fact
            | fact term_a term'''


def p_term_a(p):
    '''term_a : MULT
            | DIV'''
#    global expresion_helper
#    expresion_helper = expresion_helper + p[1]


def p_tiposimple(p):
    '''tiposimple : INT
                | FLOAT
                | CHAR'''
    token_dic['tipo'] = p[1]


def p_tipocompuesto(p):
    '''tipocompuesto : DATAFRAME
                    | ID
                    | FILE'''


def p_bloque(p):
    '''bloque : OB bloque_a CB'''


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


def p_expresion_a(p):
    '''expresion_a : LT
                | GT
                | NE
                | EQEQ
                | LE
                | GE'''
#    global expresion_helper
#    expresion_helper = expresion_helper + p[1]


def p_varcte(p):
    '''varcte : ID
            | CTE_I
            | CTE_F'''
    try:
        token_dic['valor'] = p[1]
    except IndexError:
        token_dic['valor'] = "Null"


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
#    llamada_dic[p[1]] = ""
#    print(llamada_dic)


def p_llamada_a(p):
    '''llamada_a : expresion llamada_b
                | CTE_STRING llamada_b
                | llamada_b'''
#    if p[1] != None:
#        llamada_dic["parametros"] = p[1]


def p_llamada_b(p):
    '''llamada_b : COMMA llamada_a
                | empty'''
#    if p[1] == ',':
#        llamada_dic["parametros"] = llamada_dic["parametros"] + p[1]


def p_fact(p):
    '''fact : OP exp CP
            | CTE_I
            | CTE_F
            | CTE_CHAR
            | ID
            | llamada'''

    if p[1] is not '(': #1
        math_expression_1(p[1])
    else: #7
        math_expression_7()

#    global expresion_helper
#    if p[1] == '(':
#        expresion_helper = expresion_helper + p[1]
#    elif type(p[1]) == float or type(p[1]) == int:
#        expresion_helper = expresion_helper + str(p[1])
#    else:
#        expresion_helper = expresion_helper + p[1]


def p_classcreate(p):
    '''classcreate : CLASS CLASS_ID OB classcreate_a function classcreate_c CB'''
    global curr_state
    curr_state = 0

    table['clases'][p[2]] = {}


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


def p_asignacion_a(p):
    '''asignacion_a : OSB exp CSB
                    | empty'''


def p_asignacionsencilla(p):
    '''asignacionsencilla : ID EQ expresion'''

#falta guardar los parametros de las funciones en la tabla
def p_function(p):
    '''function : function_a ID OP function_b CP bloque'''
    funciones_dic["id"] = p[2]
    table["funciones"][funciones_dic['id']] = {
        "tipo": funciones_dic['tipo']
    }
    funciones_dic_clear()


def p_function_a(p):
    '''function_a : VOID
                | tiposimple'''
    if p[1] == "void":
        funciones_dic["tipo"] = "void"
    else:
        funciones_dic["tipo"] = token_dic["tipo"]



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
    f = open("test_1.txt", "r")
    s = f.read()

except EOFError:
    print("Sintax Error")

yacc.parse(s)

pp = PrettyPrinter(indent=4)
pp.pprint(table)
