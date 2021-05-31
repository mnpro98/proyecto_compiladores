# ScannerParser.py

# Codigo principal. Ejecutar este.

# DIRECCIONES DE MEMORIA

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
#Classes    27001-36000
#   int:        27001-30000
#   float:      30001-33000
#   char:       33001-36000

import ply.lex as lex
import ply.yacc as yacc
from pprint import PrettyPrinter
from enum import Enum
from VM.VirtualMachine import start_vm

# Contadores para address de variables
globalInt = 1
globalFloat = 3001
globalChar = 6001

localInt = 9001
localFloat = 12001
localChar = 15001

tempInt = 18001
tempFloat = 21001
tempChar = 24001

classVar = 27001


#Manejador de direcciones de memoria
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

class_func_call = False
function_bool = False
class_bool = False
function_temp = {
    "total": 0,
    "int": 0,
    "float": 0,
    "char": 0
}
rel_op = ""
curr_arr_id = ""
access_id = ""
arr_type = ""
curr_class = ""
class_func_call_type = ""
class_func_call_id = ""
dim = 0
r_array = 0
offset_arr = 0
size_arr = 0
arr_pointer = 0

avail = MemoryRegister()
pending_operators = []
pending_operands = []
corresponding_types = []
quad = [['GOTO', '_', '_', 'main']]
pila_fors = []
function_vars = {}
psaltos = []
pila_dim = []
pila_nodos = []


#funcion para saber si valor recibido es float
def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

#Cubo semantico para obtener que se tendria si se hace una operacion
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
            'or': 'int',
            'and': 'int'
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
#palabras reservadas
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
    'print': 'PRINT',
    'input': 'INPUT'
}

#Tokens
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
t_INPUT = r'input'
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

#funcion para ver si hay otra dimension en arreglos
def next_pointer(dimensions):
    if dim >= dimensions:
        return False
    return True

#funcion que agrega virtual address global de arreglos
def add_globalarrvaddr():
    global globalChar, globalInt, globalFloat
    if table['variables'][curr_arr_id]['tipo'] == "int":
        table['variables'][curr_arr_id]['vaddr'] = globalInt
        globalInt += size_arr
    elif table['variables'][curr_arr_id]['tipo'] == "float":
        table['variables'][curr_arr_id]['vaddr'] = globalFloat
        globalFloat += size_arr
    elif table['variables'][curr_arr_id]['tipo'] == "char":
        table['variables'][curr_arr_id]['vaddr'] = globalChar
        globalChar += size_arr

#funcion que agrega virtual address local de arreglos
def add_localarrvaddr():
    global localChar, localFloat, localInt
    if function_vars[curr_arr_id]['tipo'] == "int":
        function_vars[curr_arr_id]['vaddr'] = localInt
        localInt += size_arr
    elif function_vars[curr_arr_id]['tipo'] == "float":
        function_vars[curr_arr_id]['vaddr'] = localFloat
        localFloat += size_arr
    elif function_vars[curr_arr_id]['tipo'] == "char":
        function_vars[curr_arr_id]['vaddr'] = localChar
        localChar += size_arr

#funcion que agrega virtual address local ademas de agregar global a las clases
def add_localvaddr():
    global localChar, localFloat, localInt, globalInt, globalFloat, globalChar, classVar
    if function_bool:
        if function_vars[token_dic['id']]['tipo'] == "int":
            function_vars[token_dic['id']]['vaddr'] = localInt
            localInt += 1
        elif function_vars[token_dic['id']]['tipo'] == "float":
            function_vars[token_dic['id']]['vaddr'] = localFloat
            localFloat += 1
        elif function_vars[token_dic['id']]['tipo'] == "char":
            function_vars[token_dic['id']]['vaddr'] = localChar
            localChar += 1
        else:
            function_vars[token_dic['id']]['vaddr'] = classVar
            classVar += len(table['clases'][token_dic['tipo']]['variables'])
    elif class_bool:
        if table['clases'][curr_class]['variables'][token_dic['id']]['tipo'] == "int":
            table['clases'][curr_class]['variables'][token_dic['id']]['vaddr'] = globalInt
            globalInt += 1
        elif table['clases'][curr_class]['variables'][token_dic['id']]['tipo'] == "float":
            table['clases'][curr_class]['variables'][token_dic['id']]['vaddr'] = globalFloat
            globalFloat += 1
        elif table['clases'][curr_class]['variables'][token_dic['id']]['tipo'] == "char":
            table['clases'][curr_class]['variables'][token_dic['id']]['vaddr'] = globalChar
            globalChar += 1    

#funcion que agrega virtual address global
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

#funcion que agrega virtual address a los parametros
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

#funcion que hace un reset a direcciones de variables locales
def reset_local():
    global localChar, localFloat, localInt
    localInt = 9001
    localFloat = 12001
    localChar = 15001

#funcion que hace un reset a direcciones de variables temporales
def reset_temp():
    global tempChar, tempInt, tempFloat
    tempInt = 18001
    tempFloat = 21001
    tempChar = 24001

#Funcion para el punto neuralgico uno de la declaracion de arreglos
#agrega a tabla de variables
def array_declaration_1(id, tipo):
    global curr_arr_id
    if function_bool:
        function_vars[id] = {"tipo": tipo}
    else:
        table['variables'][id] = {"tipo": tipo}
    curr_arr_id = id

#Funcion para el punto neuralgico dos de la declaracion de arreglos
#agrega is Array a tabla de variables
def array_declaration_2():
    if function_bool:
        function_vars[curr_arr_id]['isArray'] = True
    else:
        table['variables'][curr_arr_id]['isArray'] = True

#Funcion para el punto neuralgico tres de la declaracion de arreglos
#agrega tabla de dimensiones
def array_declaration_3():
    global dim
    global r_array

    dim = 1
    r_array = 1
    if function_bool:
        function_vars[curr_arr_id]['dimensions'] = []
    else:
        table['variables'][curr_arr_id]['dimensions'] = []

#Funcion para el punto neuralgico cinco de la declaracion de arreglos
#agrega el limite superior y hace calculo de R
def array_declaration_5(ls):
    global r_array
    if function_bool:
        function_vars[curr_arr_id]['dimensions'].append({"ls": ls})
    else:
        table['variables'][curr_arr_id]['dimensions'].append({"ls": ls})
    r_array = (int(ls) + 1) * r_array

#Funcion para el punto neuralgico seis de la declaracion de arreglos
#cambia de dimension
def array_declaration_6(ls):
    global dim
    dim += 1

#Funcion para el punto neuralgico siete de la declaracion de arreglos
#hace el recorrido por la tabla de dimensiones y agrega informacion correspondiente de m dim
def array_declaration_7():
    global dim, offset_arr, size_arr, r_array
    dim = 1
    offset_arr = 0
    size_arr = r_array

    if function_bool:
        nodes = function_vars[curr_arr_id]['dimensions']
    else:
        nodes = table['variables'][curr_arr_id]['dimensions']

    for node in nodes:
        node['m_dim'] = r_array // (node['ls'] + 1)
        r_array = node['m_dim']
        dim += 1

#Funcion para el punto neuralgico ocho de la declaracion de arreglos
#agrega la direccion correspondiente
def array_declaration_8():
    if function_bool:
        add_localarrvaddr()
    else:
        add_globalarrvaddr()

#Funcion para el punto neuralgico uno de accesso a arreglos
#hace variable con el nombre del array y mete a tabla de tipos el tipo
def array_access_1(id):
    global access_id

    pending_operands.append(id)
    if id in function_vars:
        corresponding_types.append(function_vars[id]['tipo'])
        access_id = function_vars[id]
    elif id in table['variables']:
        corresponding_types.append(table['variables'][id]['tipo'])
        access_id = table['variables'][id]


#Funcion para el punto neuralgico dos de accesso a arreglos
#revisa que si sea un arreglo y pone fondo falso en pila de operandos ademas de poner info en pila dim y piila nodos
def array_access_2():
    global arr_type, dim
    id = pending_operands.pop()
    arr_type = corresponding_types.pop()
    if id in function_vars:  # Local
        if 'dimensions' in function_vars[id]:
            dim = 1
            pila_dim.append([id, dim])
            pila_nodos.append(function_vars[id]['dimensions'])
            pending_operators.append('(')
        else:
            print("ERROR: 'dimensions' no existe en el id.")
            exit(-1)
    elif id in table['variables']:
        if 'dimensions' in table['variables'][id]:
            dim = 1
            pila_dim.append([id, dim])
            pila_nodos.append(table['variables'][id]['dimensions'])
            pending_operators.append('(')
        else:
            print("ERROR: 'dimensions' no existe en el id.")
            exit(-1)

#Funcion para el punto neuralgico tres de accesso a arreglos
#hace el cuadruplo de la verificacion del arreglo
#y revisa si es matriz o arreglo para ver que cuadruplo sigue
def array_access_3():
    global dim
    dimensions = pila_nodos[0]
    quad.append(["VER", pending_operands[-1], 0, dimensions[dim - 1]['ls']])
    if next_pointer(len(dimensions)):
        tj = avail.next(arr_type)
        aux = pending_operands.pop()
        quad.append(['*', aux, str(dimensions[dim - 1]['m_dim']), tj])
        pending_operands.append(tj)
    if dim > 1:
        tk = avail.next(arr_type)
        aux2 = pending_operands.pop()
        aux1 = pending_operands.pop()
        quad.append(['+', aux1, aux2, tk])
        pending_operands.append(tk)

#Funcion para el punto neuralgico cuatro de accesso a arreglos
#suma 1 al dim y se updatea el dim en pila de dim
def array_access_4():
    global dim
    dim += 1
    pila_dim[-1][1] = dim

#Funcion para el punto neuralgico cinco de accesso a arreglos
#crea el cuadruplo y agrega a pila de operandos el apuntador ademas de quitar el fake bottom
def array_access_5():
    global access_id
    aux1 = pending_operands.pop()
    tn = avail.next(arr_type)
    quad.append(['+', aux1, str(access_id['vaddr']), tn])
    pending_operands.append('(' + str(tn) + ')')
    pending_operators.pop()

#funcion para generar cuadruplo de return y endfunc despues del return
def return_1():
    quad.append(["RET", "_", "_", pending_operands.pop()])
    quad.append(["ENDFUNC", '_', '_', '_'])

#Funcion para el punto neuralgico uno para declarar una funcion
#mete la funcion y el tipo en la tabla de funciones
def module_def_1(proc_name):
    global function_bool
    function_bool = True
    funciones_dic["id"] = proc_name
    if class_bool:
        table['clases'][curr_class]['funciones'][funciones_dic['id']] = {
            "tipo": funciones_dic['tipo'],
            "parametros": [],
            "variables": {},
        }
    else:
        table["funciones"][funciones_dic['id']] = {
            "tipo": funciones_dic['tipo'],
            "parametros": [],
            "variables": {},
        }
    if not class_bool:
        reset_local()
        reset_temp()

#Funcion para el punto neuralgico dos para declarar una funcion
#inserta los parametros a la tabla actual
def module_def_2(param):
    global temporal_dic
    temporal_dic = {
            "tipo": param["tipo"],
            "vaddr": ""
        }
    add_paramvaddr()
    if class_bool:
        table['clases'][curr_class]['funciones'][funciones_dic['id']]["variables"][param["id"]] = temporal_dic
    else:
        table["funciones"][funciones_dic['id']]["variables"][param["id"]] = temporal_dic

#Funcion para el punto neuralgico tres para declarar una funcion
#le agrega a la tabla actual todos los tipos de los parametros
def module_def_3(param):
    if class_bool:
        table['clases'][curr_class]['funciones'][funciones_dic['id']]["parametros"].append(param['tipo'])
        try:
            table['clases'][curr_class]['funciones'][funciones_dic['id']]["parametros_vaddr"].append(temporal_dic['vaddr'])
        except KeyError:
            table['clases'][curr_class]['funciones'][funciones_dic['id']]["parametros_vaddr"] = [temporal_dic['vaddr']]
    else:
        table["funciones"][funciones_dic['id']]["parametros"].append(param['tipo'])
        try:
            table["funciones"][funciones_dic['id']]["parametros_vaddr"].append(temporal_dic['vaddr'])
        except KeyError:
            table["funciones"][funciones_dic['id']]["parametros_vaddr"] = [temporal_dic['vaddr']]


#Funcion para el punto neuralgico cuatro para declarar una funcion
#inserta el numero de parametros
def module_def_4():
    if class_bool:
        table['clases'][curr_class]['funciones'][funciones_dic['id']]["param_cont"] = len(
            table['clases'][curr_class]['funciones'][funciones_dic['id']]["parametros"])
    else:
        table["funciones"][funciones_dic['id']]["param_cont"] = len(
            table["funciones"][funciones_dic['id']]["parametros"])

#Funcion para el punto neuralgico cinco para declarar una funcion
#inserta el numero de variables locales
def module_def_5():
    if class_bool:
        function_vars.update(table['clases'][curr_class]["funciones"][funciones_dic['id']]["variables"])
        table['clases'][curr_class]["funciones"][funciones_dic['id']]["variables"] = function_vars
        table['clases'][curr_class]["funciones"][funciones_dic['id']]["var_cont"] = len(table['clases'][curr_class]["funciones"][funciones_dic['id']]["variables"])
    else:
        function_vars.update(table["funciones"][funciones_dic['id']]["variables"])
        table["funciones"][funciones_dic['id']]["variables"] = function_vars
        table["funciones"][funciones_dic['id']]["var_cont"] = len(table["funciones"][funciones_dic['id']]["variables"])

#Funcion para el punto neuralgico seis para declarar una funcion
#inserta la linea o en que quadruplo empieza la funcion
def module_def_6():
    if class_bool:
        table['clases'][curr_class]["funciones"][funciones_dic['id']]["linea"] = len(quad)
    else:
        table["funciones"][funciones_dic['id']]["linea"] = len(quad)

#Funcion para el punto neuralgico siete para declarar una funcion
#resetea la tabla local de variables genera un endfunc inserta el numero de variables temporales que se usaron
#si la funcion es el main se agrega la linea en el primer cuadruplo y un endprog
def module_def_7():
    global function_bool
    global function_temp
    global quad

    if class_bool:
        table['clases'][curr_class]["funciones"][funciones_dic['id']]["variables"] = {}
        function_vars.clear()
        if funciones_dic['id'] != 'main' and quad[-1] != ["ENDFUNC", "_", "_", "_"]:
            quad.append(["ENDFUNC", "_", "_", "_"])
        if funciones_dic['id'] == 'main':
            quad[0] = ['GOTO', '_', '_', table['clases'][curr_class]["funciones"][funciones_dic['id']]["linea"]]
            quad.append(["ENDPROG", "_", "_", "_"])
        table['clases'][curr_class]["funciones"][funciones_dic['id']]["variables_temporales"] = function_temp
        table['funciones'][funciones_dic['id']] = table['clases'][curr_class]["funciones"][funciones_dic['id']]
    else:
        table["funciones"][funciones_dic['id']]["variables"] = {}
        function_vars.clear()
        if funciones_dic['id'] != 'main' and quad[-1] != ["ENDFUNC", "_", "_", "_"]:
            quad.append(["ENDFUNC", "_", "_", "_"])
        if funciones_dic['id'] == 'main':
            quad[0] = ['GOTO', '_', '_', table["funciones"][funciones_dic['id']]["linea"]]
            quad.append(["ENDPROG", "_", "_", "_"])
        table["funciones"][funciones_dic['id']]["variables_temporales"] = function_temp
    funciones_dic_clear()
    function_bool = False
    function_temp = {
        "total": 0,
        "int": 0,
        "float": 0,
        "char": 0
    }
    avail.clear_avail()

#Funcion para el punto neuralgico uno para llamar una funcion
#verifica que la funcion existe en el dir de funciones
def module_call_1(_id):
    global func_call_id
    func_call_id = _id
    if _id not in table["funciones"] and _id not in table['clases'][class_func_call_type]['funciones']:
        print("ERROR: funcion no existe")
        exit(-1)

#Funcion para el punto neuralgico dos para llamar una funcion
#genera el era pone un piso falso y inicializa la k
def module_call_2():
    global k, pending_operators
    pending_operators.append("(")
    quad.append(["ERA", func_call_id, "_", "_"])
    k = 1

#Funcion para el punto neuralgico tres para llamar una funcion
#saca el tipo y argumento para ver que sean correctos de acuerdo con los parametros
def module_call_3():
    argument = pending_operands.pop()
    arg_type = corresponding_types.pop()
    if class_func_call:
        if table['clases'][class_func_call_type]['funciones'][func_call_id]["parametros"][k - 1] != arg_type:
            print("ERROR: el argumento " + str(k) + " de la funcion " + func_call_id + " es del tipo incorrecto")
            exit(-1)
    else:
        if table["funciones"][func_call_id]["parametros"][k - 1] != arg_type:
            print("ERROR: el argumento " + str(k) + " de la funcion " + func_call_id + " es del tipo incorrecto")
            exit(-1)
    quad.append(["PARAM", argument, "_", "PARAM" + str(k)])

#Funcion para el punto neuralgico cuatro para llamar una funcion
#suma uno a k para pasar al siguiente parametro
def module_call_4():
    global k
    k = k + 1


#Funcion para el punto neuralgico cinco para llamar una funcion
#verificar que se hayan pasado los parametros exactos de la funcion
def module_call_5():
    if class_func_call:
        if k != len(table['clases'][class_func_call_type]['funciones'][func_call_id]["parametros"]) and len(table['clases'][class_func_call_type]['funciones'][func_call_id]["parametros"]) != 0:
            print("ERROR: se paso un numero incorrecto de argumentos en la llamada.")
            exit(-1)
    else:
        if k != len(table["funciones"][func_call_id]["parametros"]) and len(table["funciones"][func_call_id]["parametros"]) != 0:
            print("ERROR: se paso un numero incorrecto de argumentos en la llamada.")
            exit(-1)
    pending_operators.pop()

#Funcion para el punto neuralgico seis para llamar una funcion
#genera los cuadruplos del gosub y si el tipo no es void tambien se genera un cuadruplo para el recibir el return
def module_call_6():
    if class_func_call:
        result = avail.next(table['clases'][class_func_call_type]['funciones'][func_call_id]["tipo"])
        quad.append(["GOSUB", func_call_id, "_", table['clases'][class_func_call_type]['funciones'][func_call_id]["linea"]])
        if table['clases'][class_func_call_type]['funciones'][func_call_id]["tipo"] != 'void':
            quad.append(["=", func_call_id, "_", result])
        pending_operands.append(result)
    else:
        result = avail.next(table["funciones"][func_call_id]["tipo"])
        quad.append(["GOSUB", func_call_id, "_", table["funciones"][func_call_id]["linea"]])
        if table["funciones"][func_call_id]["tipo"] != 'void':
            quad.append(["=", func_call_id, "_", result])
        pending_operands.append(result)

#Funcion para el punto neuralgico uno para los for loops
#agrega un dicionario vacio a la pila_for
def for_1():
    pila_fors.append({})

#Funcion para el punto neuralgico dos para los for loops
#agrega a que linea tiene que regresar para regresar a la condicion
def for_2():
    pila_fors[-1]["condicion"] = len(quad)

#Funcion para el punto neuralgico tres para los for loops
#verifica que la condicion sea del tipo correcto y hace el append de los cuadruplos de goto, gotof
def for_3():
    cond = pending_operands.pop()
    t_cond_for = corresponding_types.pop()

    if t_cond_for != "int":
        print("Tcond ERROR")
        exit(-1)
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        pila_fors[-1]["GOTOF"] = len(quad) - 1
        quad.append(["GOTO", "_", "_", "_"])
        pila_fors[-1]["GOTO1"] = len(quad) - 1

#Funcion para el punto neuralgico cuatro para los for loops
#agrega goto2 al diccionario de fors
def for_4():
    pila_fors[-1]["GOTO2"] = len(quad)

#Funcion para el punto neuralgico cinco para los for loops
#hace el cuadruplo para regresar a la condicion y rellena el goto1 con la linea donde estamos
def for_5():
    quad.append(["GOTO", "_", "_", pila_fors[-1]["condicion"]])
    quad[pila_fors[-1]["GOTO1"]][3] = len(quad)

#Funcion para el punto neuralgico seis para los for loops
#hace el cuadruplo del goto2 y rellena el gotof con la linea donde estamos
def for_6():
    quad.append(["GOTO", "_", "_", pila_fors[-1]["GOTO2"]])
    quad[pila_fors[-1]["GOTOF"]][3] = len(quad)
    pila_fors.pop()

#Funcion para el punto neuralgico uno para los if's
#saca condicion y tipo y revisa que sea int hace el quadruplo de gotof agrega linea a pila de saltos
def if_1():
    cond = pending_operands.pop()
    t_cond_if = corresponding_types.pop()
    if t_cond_if != 'int':
        print("ERROR: la condicion no es entera.")
        exit(-1)
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        psaltos.append(len(quad) - 1)

#Funcion para el punto neuralgico dos para los if's
#saca de pila de saltos y regresa a llenar donde termina el if
def if_2():
    fin = psaltos.pop()
    quad[fin][3] = len(quad)

#Funcion para el punto neuralgico tres para los if's
#regresa a falso y llena con linea actual agrega aun goto y linea a pila de saltos
def if_3():
    falso = psaltos.pop()
    quad.append(["GOTO", "_", "_", "_"])
    psaltos.append(len(quad) - 1)
    quad[falso][3] = len(quad)

#Funcion para el punto neuralgico uno para el while loop
#agrega la linea a la pila de saltos para regresar
def while_1():
    psaltos.append(len(quad))

#Funcion para el punto neuralgico dos para el while loop
#checa que la condicion sea del tipo correcto genera el cuadruplo de gotof y agrega linea a pila de saltos
def while_2():
    cond = pending_operands.pop()
    t_cond = corresponding_types.pop()

    if t_cond != "int":
        print(t_cond)
        print("Tcond ")
        print("ERROR")
        exit(-1)
    else:
        quad.append(["GOTOF", "_", cond, "_"])
        psaltos.append(len(quad) - 1)

#Funcion para el punto neuralgico tres para el while loop
#rellena gotof con linea actual y genera cuadruplo para regresar a la condicion del while
def while_3():
    falso = psaltos.pop()
    ret = psaltos.pop()
    quad.append(["GOTO", "_", "_", ret])
    quad[falso][3] = len(quad)

#funcion para ver que tipo de variable es
def infer_type(id):
    try:
        int(id)
        corresponding_types.append('int')
    except ValueError:
        try:
            float(id)
            corresponding_types.append('float')
        except ValueError:
            corresponding_types.append('char')

#funcion para el punto neuralgico 1 de las expresiones
#hace push a la pila de operandos y a la de tipos
def math_expression_1(id):
    type_converter = {
        "<class 'str'>": "char"
    }

    if id not in table['funciones']:
        if id.isnumeric() or check_float(id) or id[0] == '\'':
            pending_operands.append(id)
        else:
            if not class_bool:
                try:  # Checar si existe el id en variables para meter el virtual address a la pila.
                    pending_operands.append(table['variables'][id]['vaddr'])
                except KeyError:  # Si no, checa el de funciones
                    pending_operands.append(function_vars[id]['vaddr'])
            else:
                if id in table['clases'][curr_class]['variables']:
                    pending_operands.append(table['clases'][curr_class]['variables'][id]['vaddr'])
                else:
                    pending_operands.append(function_vars[id]['vaddr'])

    # Sacar el tipo

    if id in function_vars:
        corresponding_types.append(function_vars[id]['tipo'])
    elif id in table['variables']:
        corresponding_types.append(table['variables'][id]['tipo'])
    elif id in table['funciones']:
        corresponding_types.append(table['funciones'][id]['tipo'])
    elif curr_class != '':
        if id in table['clases'][curr_class]['variables']:
            corresponding_types.append(table['clases'][curr_class]['variables'][id]['vaddr'])
        else:
            infer_type(id)
    else:
        infer_type(id)


#funcion para el punto neuralgico 2 de las expresiones
#revisa que los operadores sean + o -
def math_expression_2(operand):
    if operand == '+' or operand == '-':
        pending_operators.append(operand)
    else:
        print("ERROR: los operadores deberian de ser + or -")
        exit(-1)

#funcion para el punto neuralgico 3 de las expresiones
#revisa que los operadors sean * o /
def math_expression_3(operand):
    if operand == '*' or operand == '/':
        pending_operators.append(operand)
    else:
        print("ERROR: los operadores deberian de ser * or /")

#funcion para el punto neuralgico 4 de las expresiones
#genera el cuadruplo de la expresion matematica
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
                # If any operand were a temporal space, return it to AVAIL
                # if left_operand[0] == "t":
                #     avail.clear_space(left_operand[1])
                # if right_operand[0] == "t":
                #     avail.clear_space(right_operand[1])
            else:
                print("ERROR: Los tipos no coinciden")
                exit(-1)

#funcion para el punto neuralgico 5 de las expresiones
#checa si los siguientes operadores son ya sea * o /
def math_expression_5():
    if len(pending_operators) != 0:
        if pending_operators[-1] == '*' or pending_operators[-1] == '/':
            math_expression_4(['*', '/'])

#funcion para el punto neuralgico 6 de las expresiones
#agrega fondo falso a la pilo
def math_expression_6():
    pending_operators.append('|')

#funcion para el punto neuralgico 7 de las expresiones
#saca fondo falso
def math_expression_7():
    if pending_operators.pop() != '|':
        print("ERROR: Falta el fondo falso.")
        exit(-1)

#funcion para el punto neuralgico 8 de las expresiones
#agrega el relop a la pilop
def math_expression_8(rel_op):
    pending_operators.append(rel_op)

#funcion para el punto neuralgico 9 de las expresiones
#checa si los siguientes operadores son ya sea un relop o (
def math_expression_9(rel_op):
    if pending_operators[-1] == rel_op or '(':
        math_expression_4(['>', '<', '>=', '<=', '==', '!='])

#funcion para el punto neuralgico 10 de las expresiones
#agrega and o or a la pilop
def math_expression_10(operand):
    if operand == "and" or operand == "or":
        pending_operators.append(operand)
    else:
        print("ERROR: los operadores deberian de ser 'and' o 'or'")
        exit(-1)

#funcion para el punto neuralgico 11 de las expresiones
#manda llamar math expresion 4 con and
def math_expression_11(rel_op):
    if pending_operators[-1] == rel_op:
        math_expression_4(["and"])

#funcion para el punto neuralgico 12 de las expresiones
#manda llamar math expresion 4 con or
def math_expression_12(rel_op):
    if pending_operators[-1] == rel_op:
        math_expression_4(["or"])

#funcion para hacer clear al dic
def funciones_dic_clear():
    funciones_dic["id"] = ""
    funciones_dic["tipo"] = ""

#funcion para hacer clear al dic
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

#GRAMATICAS
def p_programa(p):
    '''programa : PROGRAM ID SC programa_a bloque'''


def p_programa_a(p):
    '''programa_a : programa_b
                | programa_b programa_a
                | empty'''


def p_programa_b(p):
    '''programa_b : vars
                | vars_vect_mat'''

#gramatica de vars
#revisa si es funcion y hace un diccionario temporal con las variables de esa funcion
#si no lo mete a la tabla
def p_vars(p):
    '''vars : tiposimple vars_a SC
            | tipocompuesto vars_a SC'''

    global function_vars

    if function_bool:
        function_vars[token_dic['id']]['tipo'] = token_dic['tipo']
        function_vars[token_dic['id']]['valor'] = token_dic['valor']
        try:
            function_vars[token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    elif class_bool:
        table['clases'][curr_class]['variables'][token_dic['id']]['tipo'] = token_dic['tipo']
        try:
            table['clases'][curr_class]['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    else:
        table['variables'][token_dic['id']]['tipo'] = token_dic['tipo']
        table['variables'][token_dic['id']]['valor'] = token_dic['valor']
        try:
            table['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_globalvaddr()
    token_dic_clear()


def p_vars_a(p):
    '''vars_a : vars_b
            | vars_c vars_a'''

#revisa si esta en funcion o clase y mete a lugar correspondiente
#si el length es mayor a dos genera cuadruplo de resultado
def p_vars_b(p):
    '''vars_b : ID
            | ID EQ expresion'''
    token_dic['id'] = p[1]
    if function_bool:
        function_vars[token_dic['id']] = {
            "tipo": token_dic['tipo'],
        }
        try:
            function_vars[token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    elif class_bool:
        table['clases'][curr_class]['variables'][token_dic['id']] = {
            "tipo": token_dic['tipo'],
            "valor": token_dic['valor'],
        }
        try:
            table['clases'][curr_class]['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()
    else:
        table['variables'][token_dic['id']] = {
            "tipo": token_dic['tipo'],
            "valor": token_dic['valor']
        }
        try:
            table['variables'][token_dic['id']]['vaddr']
        except KeyError:
            add_globalvaddr()

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
    '''vars_vect_mat : vars_vect_mat_b vars_vect_mat_a SC
                    | vars_vect_mat_b vars_vect_mat_a vars_vect_mat_d SC'''
    array_declaration_7()
    array_declaration_8()


def p_vars_vect_mat_a(p):
    '''vars_vect_mat_a : vars_vect_mat_c exp CSB'''
    array_declaration_5(int(pending_operands[-1]) - 1)


def p_vars_vect_mat_b(p):
    '''vars_vect_mat_b : tiposimple ID'''
    array_declaration_1(p[2], token_dic['tipo'])
    array_declaration_2()


def p_vars_vect_mat_c(p):
    '''vars_vect_mat_c : OSB'''
    array_declaration_3()


def p_vars_vect_mat_d(p):
    '''vars_vect_mat_d : OSB exp CSB'''
    array_declaration_6(int(pending_operands[-1]) - 1)
    array_declaration_5(int(pending_operands[-1]) - 1)


def p_m_exp(p):
    '''m_exp : m_exp_b
            | m_exp_b m_exp_a m_exp'''


def p_m_exp_a(p):
    '''m_exp_a : ADD
            | SUB'''
    math_expression_2(p[1])


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
                | print
                | input'''


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

#agrega operando a la pila
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
    '''exp : and_exp
            | exp_b exp'''
    if len(p) == 3:
        math_expression_12("or")


def p_exp_b(p):
    '''exp_b : and_exp OR'''
    math_expression_10("or")


def p_and_exp(p):
    '''and_exp : expresion
            | and_exp_b and_exp'''
    if len(p) == 3:
        math_expression_12("and")


def p_and_exp_b(p):
    '''and_exp_b : expresion AND'''
    math_expression_10("and")


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

#si es una llamada a una funcion de una clase se hace un quadruplo con una direccion
def p_llamada_c(p):
    '''llamada_c : ID'''
    if class_func_call:
        class_vars = table['clases'][token_dic['tipo']]['variables']
        cont = 0
        for i in class_vars.values():
            quad.append(["=", '_', '[' + str(function_vars[class_func_call_id]['vaddr'] + cont) + ']', i['vaddr']])
            cont += 1
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

#genera cuadruplo para el print
def p_print(p):
    '''print : PRINT OP expresion CP SC'''
    quad.append(["PRINT", "_", "_", pending_operands.pop()])

#genera cuadruplo para el input
def p_input(p):
    '''input : INPUT OP ID CP SC'''
    try:
        result = table['variables'][p[3]]['vaddr']
    except KeyError:
        try:
            result = function_vars[p[3]]['vaddr']
        except KeyError:
            print("ERROR: VARIABLE PUESTA EN INPUT NO EXISTE")
            exit()
    quad.append(["INPUT", "_", p[3], result])

def p_fact(p):
    '''fact : OP fact_a exp CP
            | CTE_I
            | CTE_F
            | CTE_CHAR
            | ID
            | llamada
            | llamadafuncionclase
            | array_access'''

    if p[1] == "(":
        math_expression_7()
    elif p[1] is None:  # 1
        # Llamar funcion en caso de que sea una llamada
        if func_call_id != "":
            math_expression_1(func_call_id)
    else:
        math_expression_1(p[1])


def p_fact_a(p):
    '''fact_a : empty'''
    math_expression_6()


def p_classcreate(p):
    '''classcreate : classcreate_e OB classcreate_a function classcreate_c CB'''
    global class_bool
    class_bool = False


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

#agrega clase a tabla de clases
def p_classcreate_e(p):
    '''classcreate_e : CLASS CLASS_ID'''
    global curr_class, class_bool
    class_bool = True
    curr_class = p[2]
    table['clases'][p[2]] = {'variables': {},
                             'funciones': {}}


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
    '''condicion_c : IF OP exp CP'''
    if_1()


def p_condicion_d(p):
    '''condicion_d : ELSE'''
    if_3()

#se agrega id ,tipo y virtual address a dicionario temporal
def p_classdeclare(p):
    '''classdeclare : CLASS_ID ID SC'''
    token_dic['tipo'] = p[1]
    token_dic['id'] = p[2]
    if function_bool:
        function_vars[token_dic['id']] = {
            "tipo": token_dic['tipo'],
        }
        try:
            function_vars[token_dic['id']]['vaddr']
        except KeyError:
            add_localvaddr()


def p_llamadafuncionclase(p):
    '''llamadafuncionclase : llamadafuncionclase_a POINT llamada
                            | llamadafuncionclase_a POINT llamada SC'''
    global class_func_call_type, class_func_call
    class_func_call_type = ''
    class_func_call = False


def p_llamadafuncionclase_a(p):
    '''llamadafuncionclase_a : ID'''
    print(p[1])
    global class_func_call, class_func_call_type, class_func_call_id
    class_func_call = True
    class_func_call_id = p[1]
    class_func_call_type = table['funciones'][funciones_dic['id']]['variables'][class_func_call_id]['tipo']

#se genera cuadruplo para la asignacion
#si p[1] es non es un arreglo y busca a donde se le tiene que asignar
def p_asignacion(p):
    '''asignacion : ID EQ expresion SC
                | array_access EQ expresion SC
                |  ID EQ expresion'''

    debug_num = 0

    operator = p[2]
    left_operand = '_'
    right_operand = pending_operands.pop()
    if p[1] is not None:
        if not class_bool:
            try:
                result = table['variables'][p[1]]['vaddr']
            except KeyError:
                try:
                    result = function_vars[p[1]]['vaddr']
                except KeyError:
                    print("ERROR: variable ", p[1], " no existe.")
                    exit(-1)
        else:
            result = table['clases'][curr_class]['variables'][p[1]]['vaddr']
    else:
        result = pending_operands.pop()

    _quad = [operator, left_operand, right_operand, result]
    quad.append(_quad)

#genera cuadruplo para la asignacion sencilla, y agrega su vaddr
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


def p_function(p):
    '''function : DEF function_e bloque'''
    module_def_7()

#agrega tipo a diccionario temporal de funciones
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
    '''function_e : function_c OP function_b CP function_f'''
    module_def_5()
    module_def_6()


def p_function_f(p):
    '''function_f : vars function_f
                | classdeclare function_f
                | empty'''


def p_array_access(p):
    '''array_access : array_access_c array_access_d exp CSB
                    | array_access_c'''
    if len(p) > 2:
        array_access_3()
    array_access_5()


def p_array_access_a(p):
    '''array_access_a : ID'''
    array_access_1(p[1])


def p_array_access_b(p):
    '''array_access_b : array_access_a OSB'''
    array_access_2()


def p_array_access_c(p):
    '''array_access_c : array_access_b exp CSB'''
    array_access_3()


def p_array_access_d(p):
    '''array_access_d : OSB'''
    array_access_4()


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()

try:
    f = open("test_string.txt", "r")
    s = f.read()

except EOFError:
    print("Sintax Error")

yacc.parse(s)

pp = PrettyPrinter(indent=4)
pp.pprint(quad)
#pp.pprint(table)


start_vm(quad, table['funciones'], table['clases'])
