# Global:   1 - 9000
#   int:        1 - 3000
#   float:      3001 - 6000
#   char:       6001 - 9000
# Local:    9001 - 18000
#   int:        9001 - 12000
#   float:      12001 - 15000
#   char:       15001 - 18000
# Temp:     18001 - 27000
#   int:        18001 - 21000
#   float:      21001 - 24000
#   char:       24001 - 27000

import ply.lex as lex
import ply.yacc as yacc
from pprint import PrettyPrinter
from enum import Enum
from VM.VirtualMachine import start_vm

#Contadores para address de variables
globalInt = 1
globalFloat = 3001
globalChar = 6001

localInt = 9001
localFloat = 12001
localChar = 15001

tempInt = 18001
tempFloat = 21001
tempChar = 24001


class MemoryRegister:
    array: list
    index: int

    def __init__(self):
        self.array = [None]*1000
        self.index = 0

    def next(self, type):
        global tempInt, tempChar, tempFloat
        if type == "int":
            temp = tempInt
            tempInt += 1
            return temp
        elif type == "float":
            temp = tempFloat
            tempFloat += 1
            return temp
        elif type == "char":
            temp = tempChar
            tempChar += 1
            return temp

    def clear_space(self, space_num):
        space_num = int(space_num)
        self.array[space_num] = None

    def clear_avail(self):
        self.array.clear()
        self.index = 0


class State(Enum):
    CLASS_CREATE = 1

tabla_constantes = {}

curr_state = 0
function_bool = False
function_temp = {
    "total": 0,
    "int": 0,
    "float": 0,
    "char": 0
}
rel_op = ""

avail = MemoryRegister()
pending_operators = []
pending_operands = []
corresponding_types = []
quad = [['GOTO', '_', '_', 'main']]
pila_fors = []
function_vars = {}

psaltos = []

def check_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False

semantics = {
    'int': {
        'int': {
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'float',
            '>': 'int',
            '<': 'int',
            '>=': 'int',
            '<=': 'int',
            '==': 'int',
            '!=': 'int',
            'or': 'error',
            'and': 'error'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '>': 'int',
            '<': 'int',
            '>=': 'int',
            '<=': 'int',
            '==': 'int',
            '!=': 'int',
            'or': 'error',
            'and': 'error'
        },
        'char': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '>': 'error',
            '<': 'error',
            '>=': 'error',
            '<=': 'error',
            '==': 'error',
            '!=': 'error',
            'or': 'error',
            'and': 'error'
        },
    },
    'float': {
        'int': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '>': 'int',
            '<': 'int',
            '>=': 'int',
            '<=': 'int',
            '==': 'int',
            '!=': 'int',
            'or': 'error',
            'and': 'error'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '>': 'int',
            '<': 'int',
            '>=': 'int',
            '<=': 'int',
            '==': 'int',
            '!=': 'int',
            'or': 'error',
            'and': 'error'
        },
        'char': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '>': 'error',
            '<': 'error',
            '>=': 'error',
            '<=': 'error',
            '==': 'error',
            '!=': 'error',
            'or': 'error',
            'and': 'error'
        },
    },
    'char': {
        'int': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '>': 'error',
            '<': 'error',
            '>=': 'error',
            '<=': 'error',
            '==': 'error',
            '!=': 'error',
            'or': 'error',
            'and': 'error'
        },
        'float': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '>': 'error',
            '<': 'error',
            '>=': 'error',
            '<=': 'error',
            '==': 'error',
            '!=': 'error',
            'or': 'error',
            'and': 'error'
        },
        'char': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '>': 'int',
            '<': 'int',
            '>=': 'int',
            '<=': 'int',
            '==': 'int',
            '!=': 'int',
            'or': 'error',
            'and': 'error'
        },
    },
}

expresion_helper = ""
k = -1

token_dic = {
    "id": "",
    "tipo": "",
    "valor": "null"
}  # 0 - Tipo, 1 - id, 2 - valor

funciones_dic = {
    "id": "",
    "tipo": ""
}

func_call_id = ""

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
    'file': 'FILE',
    'return': 'RETURN',
    'def': 'DEF',
    'print': 'PRINT'
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
t_RETURN = r'return'
t_VOID = r'void'
t_FOR = r'for'
t_DEF = r'def'
t_PRINT = r'print'
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


def add_localvaddr():
    global localChar, localFloat, localInt
    if function_vars[token_dic['id']]['tipo'] == "int":
        function_vars[token_dic['id']]['vaddr'] = localInt
        localInt += 1
    elif function_vars[token_dic['id']]['tipo'] == "float":
        function_vars[token_dic['id']]['vaddr'] = localFloat
        localFloat += 1
    elif function_vars[token_dic['id']]['tipo'] == "char":
        function_vars[token_dic['id']]['vaddr'] = localChar
        localChar += 1
    

def add_globalvaddr():
    global globalChar
    global globalInt
    global globalFloat

    if table['variables'][token_dic['id']]['tipo'] == "int":
        table['variables'][token_dic['id']]['vaddr'] = globalInt
        globalInt += 1
    elif table['variables'][token_dic['id']]['tipo'] == "float":
        table['variables'][token_dic['id']]['vaddr'] = globalFloat
        globalFloat += 1
    elif table['variables'][token_dic['id']]['tipo'] == "char":
        table['variables'][token_dic['id']]['vaddr'] = globalChar
        globalChar += 1

temporal_dic = {}

def add_paramvaddr():
    global localChar, localFloat, localInt
    if temporal_dic['tipo'] == "int":
        temporal_dic['vaddr'] = localInt
        localInt += 1
    elif temporal_dic['tipo'] == "float":
        temporal_dic['vaddr'] = localFloat
        localFloat += 1
    elif temporal_dic['tipo'] == "char":
        temporal_dic['vaddr'] = localChar
        localChar += 1

def return_1():
    quad.append(["RET", "_", "_", pending_operands.pop()])


def module_def_1(proc_name):
    global function_bool
    function_bool = True
    funciones_dic["id"] = proc_name
    table["funciones"][funciones_dic['id']] = {
        "tipo": funciones_dic['tipo'],
        "parametros": [],
        "variables": {},
    }


def module_def_2(param):
    global temporal_dic
    temporal_dic = {
            "tipo": param["tipo"],
            "vaddr": ""
        }
    add_paramvaddr()
    table["funciones"][funciones_dic['id']]["variables"][param["id"]] = temporal_dic


def module_def_3(param):
    table["funciones"][funciones_dic['id']]["parametros"].append(param['tipo'])
    try:
        table["funciones"][funciones_dic['id']]["parametros_vaddr"].append(temporal_dic['vaddr'])
    except KeyError:
        table["funciones"][funciones_dic['id']]["parametros_vaddr"] = [temporal_dic['vaddr']]


# Insert the number of parameters.
def module_def_4():
    table["funciones"][funciones_dic['id']]["param_cont"] = len(table["funciones"][funciones_dic['id']]["parametros"])


def module_def_5():
    function_vars.update(table["funciones"][funciones_dic['id']]["variables"])
    table["funciones"][funciones_dic['id']]["variables"] = function_vars
    table["funciones"][funciones_dic['id']]["var_cont"] = len(table["funciones"][funciones_dic['id']]["variables"])
    #print(str(table["funciones"][funciones_dic['id']]["variables"]))


def module_def_6():
    table["funciones"][funciones_dic['id']]["linea"] = len(quad)


def module_def_7():
    global function_bool
    global function_temp
    global quad
    table["funciones"][funciones_dic['id']]["variables"] = {}
    function_vars.clear()
    if funciones_dic['id'] != 'main':
        quad.append(["ENDFUNC", "_", "_", "_"])
    if funciones_dic['id'] == 'main':
        quad[0] = ['GOTO', '_', '_', table["funciones"][funciones_dic['id']]["linea"]]
        quad.append(["ENDPROG", "_", "_", "_"])
    table["funciones"][funciones_dic['id']]["variables_temporales"] = function_temp
    funciones_dic_clear()
    function_bool = False
    # TODO: NOS FALTO EL ULTIMO PASO
    function_temp = {
        "total": 0,
        "int": 0,
        "float": 0,
        "char": 0
    }
    avail.clear_avail()


def module_call_1(_id):
    global func_call_id
    func_call_id = _id
    if _id not in table["funciones"]:
        print("ERROR: funcion no existe")
        exit(-1)


def module_call_2():
    global k, pending_operators
    pending_operators.append("(")
    quad.append(["ERA", func_call_id, "_", "_"])
    k = 1


def module_call_3():
    argument = pending_operands.pop()
    arg_type = corresponding_types.pop()
    if table["funciones"][func_call_id]["parametros"][k - 1] != arg_type:
        print("ERROR: el argumento " + str(k) + " de la funcion " + func_call_id + " es del tipo incorrecto")
        exit(-1)
    quad.append(["PARAM", argument, "_", "PARAM" + str(k)])

def module_call_4():
    global k
    k = k + 1


def module_call_5():
    if k != len(table["funciones"][func_call_id]["parametros"]) and len(table["funciones"][func_call_id]["parametros"]) != 0:
        print("ERROR: se paso un numero incorrecto de argumentos en la llamada.")
        exit(-1)
    pending_operators.pop()


def module_call_6():
    result = avail.next(table["funciones"][func_call_id]["tipo"])
    quad.append(["GOSUB", func_call_id, "_", table["funciones"][func_call_id]["linea"]])
    if table["funciones"][func_call_id]["tipo"] != 'void':
        quad.append(["=", func_call_id, "_", result])
    pending_operands.append(result)


def for_1():
    pila_fors.append({})


def for_2():
    pila_fors[-1]["condicion"] = len(quad)


def for_3():
    cond = pending_operands.pop()
    t_cond_for = corresponding_types.pop()

    if t_cond_for != "int":
        print("Tcond ERROR")
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        pila_fors[-1]["GOTOF"] = len(quad) - 1
        quad.append(["GOTO", "_", "_", "_"])
        pila_fors[-1]["GOTO1"] = len(quad) - 1


def for_4():
    pila_fors[-1]["GOTO2"] = len(quad)


def for_5():
    quad.append(["GOTO", "_", "_", pila_fors[-1]["condicion"]])
    quad[pila_fors[-1]["GOTO1"]][3] = len(quad)


def for_6():
    quad.append(["GOTO", "_", "_", pila_fors[-1]["GOTO2"]])
    quad[pila_fors[-1]["GOTOF"]][3] = len(quad)
    pila_fors.pop()


def if_1():
    cond = pending_operands.pop()
    t_cond_if = corresponding_types.pop()
    if t_cond_if != 'int':
        print("ERROR: Cond is not int")
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        psaltos.append(len(quad) - 1)


def if_2():
    fin = psaltos.pop()
    quad[fin][3] = len(quad)


def if_3():
    falso = psaltos.pop()
    quad.append(["GOTO", "_", "_", "_"])
    psaltos.append(len(quad) - 1)
    quad[falso][3] = len(quad)


def while_1():
    psaltos.append(len(quad))


def while_2():
    cond = pending_operands.pop()
    t_cond = corresponding_types.pop()

    if t_cond != "int":
        print(t_cond)
        print("Tcond ")
        print("ERROR")
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        psaltos.append(len(quad) - 1)


def while_3():
    falso = psaltos.pop()
    ret = psaltos.pop()
    quad.append(["GOTO", "_", "_", ret])
    quad[falso][3] = len(quad)


def infer_type(id):
    try:  # TODO Detectar cuando es float
        int(id)
        corresponding_types.append('int')
    except ValueError:
        corresponding_types.append('char')


def math_expression_1(id):
    type_converter = {
        "<class 'str'>": "char"
    }

    if id not in table['funciones']:
        if id.isnumeric() or check_float(id) or id[0] == '\'':
            pending_operands.append(id)
        else:
            try:
                pending_operands.append(table['variables'][id]['vaddr'])
            except KeyError:
                pending_operands.append(function_vars[id]['vaddr'])

    if id in function_vars:
        corresponding_types.append(function_vars[id]['tipo'])
    elif id in table['variables']:
        corresponding_types.append(table['variables'][id]['tipo'])
    elif id in table['funciones']:
        corresponding_types.append(table['funciones'][id]['tipo'])
    else:
        infer_type(id)


def math_expression_2(operand):
    if operand == '+' or operand == '-':
        pending_operators.append(operand)
    else:
        print("ERROR: operands should be either + or -")


def math_expression_3(operand):
    if operand == '*' or operand == '/':
        pending_operators.append(operand)
    else:
        print("ERROR: operands should be either + or -")


def math_expression_4(symbols):
    global avail
    global function_temp
    if len(pending_operators) != 0:
        if pending_operators[-1] in symbols:
            right_operand = pending_operands.pop()
            right_type = corresponding_types.pop()
            left_operand = pending_operands.pop()
            left_type = corresponding_types.pop()
            operator = pending_operators.pop()

            result_type = semantics[left_type][right_type][operator]
            if result_type != 'error' and result_type != 'ERROR':
                if function_bool:
                    function_temp["total"] = function_temp["total"] + 1
                    if result_type == 'int':
                        function_temp["int"] = function_temp["int"] + 1
                    elif result_type == 'float':
                        function_temp["float"] = function_temp["float"] + 1
                    elif result_type == 'char':
                        function_temp["char"] = function_temp["char"] + 1
                result = avail.next(result_type)  # Avail continene registros temporales, direcciones disponibles
                _quad = [operator, left_operand, right_operand, result]
                quad.append(_quad)
                pending_operands.append(result)
                corresponding_types.append(result_type)
                #TODO: revisar esto (da out of bounds cuando reseteas el avail)
                # If any operand were a temporal space, return it to AVAIL
                # if left_operand[0] == "t":
                #     avail.clear_space(left_operand[1])
                # if right_operand[0] == "t":
                #     avail.clear_space(right_operand[1])
            else:
                print("ERROR: Type mismatch")
                exit(-1)


def math_expression_5():
    if len(pending_operators) != 0:
        if pending_operators[-1] == '*' or pending_operators[-1] == '/':
            math_expression_4(['*', '/'])


def math_expression_6():
    pending_operators.append('|')


def math_expression_7():
    if pending_operators.pop() != '|':
        print("ERROR: False bottom mark missing.")


def math_expression_8(rel_op):
    pending_operators.append(rel_op)


def math_expression_9(rel_op):
    if pending_operators[-1] == rel_op:
        math_expression_4(['>', '<', '>=', '<=', '==', '!='])


def create_class_variable():
    pass


def state_switcher(arg):
    switcher = {
        State.CLASS_CREATE: create_class_variable
    }
    func = switcher.get(arg, "Invalid state")
    func()


def funciones_dic_clear():
    funciones_dic["id"] = ""
    funciones_dic["tipo"] = ""


def token_dic_clear():
    token_dic["tipo"] = ""
    token_dic["id"] = ""
    token_dic["valor"] = ""


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
                | programa_b programa_a
                | empty'''


def p_programa_b(p):
    '''programa_b : vars
                | vars_vect_mat'''


def p_vars(p):
    '''vars : tiposimple vars_a SC
            | tipocompuesto vars_a SC'''

    global function_vars

    if not function_bool:
        table['variables'][token_dic['id']]['tipo'] = token_dic['tipo']
        table['variables'][token_dic['id']]['valor'] = token_dic['valor']
        try:
            table['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_globalvaddr()
    else:
        function_vars[token_dic['id']]['tipo'] = token_dic['tipo']
        function_vars[token_dic['id']]['valor'] = token_dic['valor']
        try:
            function_vars[token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    token_dic_clear()


def p_vars_a(p):
    '''vars_a : vars_b
            | vars_c vars_a'''


def p_vars_b(p):
    '''vars_b : ID
            | ID EQ expresion'''
    token_dic['id'] = p[1]
    if not function_bool:
        table['variables'][token_dic['id']] = {
            "tipo": token_dic['tipo'],
            "valor": token_dic['valor']
        }
        try:
            table['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_globalvaddr()
    else:
        function_vars[token_dic['id']] = {
            "tipo": token_dic['tipo'],
            "valor": token_dic['valor'],
        }
        try:
            function_vars[token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    if len(p) > 2:
        operator = p[2]
        left_operand = '_'
        right_operand = pending_operands.pop()
        try:
            result = table['variables'][p[1]]['vaddr']
        except KeyError:
            result = function_vars[p[1]]['vaddr']
        _quad = [operator, left_operand, right_operand, result]
        quad.append(_quad)


def p_vars_c(p):
    '''vars_c : vars_b COMMA'''

def p_vars_vect_mat(p):
    '''vars_vect_mat : tiposimple ID vars_vect_mat_a SC
                    | tiposimple ID vars_vect_mat_a vars_vect_mat_a SC'''


def p_vars_vect_mat_a(p):
    '''vars_vect_mat_a : OSB exp CSB'''


def p_m_exp(p):
    '''m_exp : m_exp_b
            | m_exp_b m_exp_a m_exp'''


def p_m_exp_a(p):
    '''m_exp_a : ADD
            | SUB'''
    math_expression_2(p[1])
#    global expresion_helper
#    expresion_helper = expresion_helper + p[1]


def p_m_exp_b(p):
    '''m_exp_b : term '''
    math_expression_4(['+', '-'])


def p_term(p):
    '''term : term_b
            | term_b term_a term'''


def p_term_a(p):
    '''term_a : MULT
            | DIV'''
    math_expression_3(p[1])
#    global expresion_helper
#    expresion_helper = expresion_helper + p[1]


def p_term_b(p):
    '''term_b : fact'''
    math_expression_5()


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
                | llamada SC
                | while
                | for
                | classcreate
                | vars
                | classdeclare
                | llamadafuncionclase
                | function
                | return
                | print'''


def p_return(p):
    '''return : RETURN expresion SC'''
    return_1()


def p_expresion(p):
    '''expresion : m_exp
                | m_exp expresion_a m_exp'''
    global rel_op
    if len(p) == 4:
        math_expression_9(rel_op)
    rel_op = ""


def p_expresion_a(p):
    '''expresion_a : LT
                | GT
                | NE
                | EQEQ
                | LE
                | GE'''
    global rel_op
    math_expression_8(p[1])
    rel_op = p[1]
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
    pending_operands.append(p[1])


def p_while(p):
    '''while : while_b bloque'''
    while_3()


def p_while_a(p):
    '''while_a : WHILE'''
    while_1()


def p_while_b(p):
    '''while_b : while_a OP expresion CP'''
    while_2()


def p_exp(p):
    '''exp : and_exp exp_a'''
    math_expression_6()


def p_exp_a(p):
    '''exp_a : OR
            | empty'''


def p_and_exp(p):
    '''and_exp : expresion and_exp_a'''


def p_and_exp_a(p):
    '''and_exp_a : AND
                | empty'''


def p_for(p):
    '''for : for_a for_b bloque'''
    for_6()


def p_for_a(p):
    '''for_a : FOR'''
    for_1()


def p_for_b(p):
    '''for_b : for_e asignacionsencilla CP'''
    for_5()


def p_for_c(p):
    '''for_c : OP asignacionsencilla SC'''
    for_2()


def p_for_d(p):
    '''for_d : for_c expresion'''
    for_3()


def p_for_e(p):
    '''for_e : for_d SC'''
    for_4()


def p_llamada(p):
    '''llamada : llamada_d llamada_a CP'''
    module_call_5()
    module_call_6()


def p_llamada_a(p):
    '''llamada_a : llamada_e llamada_b
                | llamada_b'''


def p_llamada_b(p):
    '''llamada_b : llamada_f llamada_a
                | empty'''


def p_llamada_c(p):
    '''llamada_c : ID'''
    module_call_1(p[1])


def p_llamada_d(p):
    '''llamada_d : llamada_c OP'''
    module_call_2()


def p_llamada_e(p):
    '''llamada_e : expresion
                | CTE_STRING'''
    module_call_3()


def p_llamada_f(p):
    '''llamada_f : COMMA'''
    module_call_4()

def p_print(p):
    '''print : PRINT OP expresion CP SC'''
    quad.append(["PRINT", "_", "_", pending_operands.pop()])


def p_fact(p):
    '''fact : OP fact_a exp CP
            | CTE_I
            | CTE_F
            | CTE_CHAR
            | ID
            | llamada'''

    if p[1] == "(":
        math_expression_7()
    elif p[1] is None:  # 1
        # Llamar funcion en caso de que sea una llamada
        math_expression_1(func_call_id)
    else:
        math_expression_1(p[1])


def p_fact_a(p):
    '''fact_a : empty'''
    math_expression_6()


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
    '''condicion : condicion_c bloque condicion_a'''
    if_2()


def p_condicion_a(p):
    '''condicion_a : condicion_d condicion_b bloque
                | empty'''


def p_condicion_b(p):
    '''condicion_b : condicion
                | empty'''


def p_condicion_c(p):
    '''condicion_c : IF OP expresion CP'''
    if_1()


def p_condicion_d(p):
    '''condicion_d : ELSE'''
    if_3()


def p_classdeclare(p):
    '''classdeclare : CLASS_ID ID SC'''


def p_llamadafuncionclase(p):
    '''llamadafuncionclase : ID POINT llamada'''


def p_asignacion(p):
    '''asignacion : ID asignacion_a asignacion_a EQ expresion SC'''

    operator = p[4]
    left_operand = '_'
    right_operand = pending_operands.pop()
    try:
        result = table['variables'][p[1]]['vaddr']
    except KeyError:
        result = function_vars[p[1]]['vaddr']

    _quad = [operator, left_operand, right_operand, result]
    quad.append(_quad)


def p_asignacion_a(p):
    '''asignacion_a : OSB exp CSB
                    | empty'''


def p_asignacionsencilla(p):
    '''asignacionsencilla : ID EQ expresion'''

    operator = p[2]
    left_operand = '_'
    right_operand = pending_operands.pop()
    try:
        result = table['variables'][p[1]]['vaddr']
    except KeyError:
        result = function_vars[p[1]]['vaddr']
    _quad = [operator, left_operand, right_operand, result]
    quad.append(_quad)


#TODO falta guardar los parametros de las funciones en la tabla
def p_function(p):
    '''function : DEF function_e bloque'''
    module_def_7()


def p_function_a(p):
    '''function_a : VOID
                | tiposimple'''
    if p[1] == "void":
        funciones_dic["tipo"] = "void"
    else:
        funciones_dic["tipo"] = token_dic["tipo"]


def p_function_b(p):
    '''function_b : function_d
                | function_d COMMA function_b
                | empty'''


def p_function_c(p):
    '''function_c : function_a ID'''
    module_def_1(p[2])


def p_function_d(p):
    '''function_d : tiposimple ID'''
    _dic = {
        "tipo": token_dic['tipo'],
        "id": p[2],
        "vaddr": ""
    }
    module_def_2(_dic)
    module_def_3(_dic)


def p_function_e(p):
    '''function_e : function_c OP function_b CP vars
                | function_c OP function_b CP empty'''
    module_def_5()
    module_def_6()


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()


try:
    f = open("test_10.txt", "r")
    s = f.read()

except EOFError:
    print("Sintax Error")

yacc.parse(s)

pp = PrettyPrinter(indent=4)
pp.pprint(quad)
#pp.pprint(table)

start_vm(quad, table['funciones'])
