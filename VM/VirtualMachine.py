from typing import ValuesView
#variables globales
quad = []
memories = []

curr_quad = []
curr_quad_num = 0
#rangos de vaddr's
GLOBAL_INT = 1
GLOBAL_FLOAT = 3001
GLOBAL_CHAR = 6001

LOCAL_INT = 9001
LOCAL_FLOAT = 12001
LOCAL_CHAR = 15001

TEMP_INT = 18001
TEMP_FLOAT = 21001
TEMP_CHAR = 24001

CLASS_VAR = 27001

funciones = {}
tclases = {}
class_attr_dic = {}

#clase de la memoria que utiliza la virtual machine
class Memory:
    integers: list
    floats: list
    chars: list

    t_integers: list
    t_floats: list
    t_chars: list

    c_vars: list

    def __init__(self):
        self.integers = []
        self.floats = []
        self.chars = []
        self.t_integers = []
        self.t_floats = []
        self.t_chars = []
        self.c_vars = []

    def push_int(self, value):
        self.integers.append(value)

    def push_float(self, value):
        self.floats.append(value)

    def push_char(self, value):
        self.chars.append(value)

    def push_t_int(self, value):
        self.t_integers.append(value)

    def push_t_float(self, value):
        self.t_floats.append(value)

    def push_t_char(self, value):
        self.t_chars.append(value)

    def push_c_vars(self, value):
        self.c_vars.append(value)

    def change_int(self, index, value):
        self.integers[index] = value

    def change_float(self, index, value):
        self.floats[index] = value

    def change_char(self, index, value):
        self.chars[index] = value

    def change_t_int(self, index, value):
        self.t_integers[index] = value

    def change_t_float(self, index, value):
        self.t_floats[index] = value

    def change_t_char(self, index, value):
        self.t_chars[index] = value

    def change_c_vars(self, index, value):
        self.c_vars[index] = value

    def get_int(self, index):
        try:
            return self.integers[index]
        except IndexError:
            return None

    def get_float(self, index):
        try:
            return self.floats[index]
        except IndexError:
            return None

    def get_char(self, index):
        try:
            return self.chars[index]
        except IndexError:
            return None

    def get_t_int(self, index):
        try:
            return self.t_integers[index]
        except IndexError:
            return None

    def get_t_float(self, index):
        try:
            return self.t_floats[index]
        except IndexError:
            return None

    def get_t_char(self, index):
        try:
            return self.t_chars[index]
        except IndexError:
            return None

    def get_c_vars(self, index):
        try:
            return self.c_vars[index]
        except IndexError:
            return None

    def print_mem(self):
        print("int", self.integers)
        print("float", self.floats)
        print("char", self.chars)
        print("tint", self.t_integers)
        print("tfloat", self.t_floats)
        print("tchar", self.t_chars)
        print("cvars", self.c_vars)

#regresa la direccion de un arreglo
def array_dir(dir):
    return get(int(dir))

#funcion para insertar valores a las direcciones vrituales en memoria
#checa que sean globales para insertar en la memoria global
#o locales para insertar en la memoria local actual
def insert(dir, value):
    global_max = LOCAL_INT - 1
    local_max = TEMP_INT - 1
    temp_max = CLASS_VAR - 1

    if dir <= global_max:  # Global
        if dir < GLOBAL_FLOAT:  # int
            index = dir - 1
            if len(memories[0].integers) <= index:
                while len(memories[0].integers) < index:
                    memories[0].push_int(None)
                memories[0].push_int(value)
            else:
                memories[0].change_int(index, value)
        elif GLOBAL_FLOAT <= dir < GLOBAL_CHAR:  # float
            index = dir - GLOBAL_FLOAT
            if len(memories[0].floats) <= index:
                while len(memories[0].floats) < index:
                    memories[0].push_float(None)
                memories[0].push_float(value)
            else:
                memories[0].change_float(index, value)
        else:  # char
            index = dir - GLOBAL_CHAR
            if len(memories[0].chars) <= index:
                while len(memories[0].chars) < index:
                    memories[0].push_char(None)
                memories[0].push_char(value)
            else:
                memories[0].change_char(index, value)
    elif global_max < dir <= local_max:  # Local
        if dir < LOCAL_FLOAT:  # int
            index = dir - LOCAL_INT
            if len(memories[-1].integers) <= index:
                while len(memories[-1].integers) < index:
                    memories[-1].push_int(None)
                memories[-1].push_int(value)
            else:
                memories[-1].change_int(index, value)
        elif LOCAL_FLOAT <= dir < LOCAL_CHAR:  # float
            index = dir - LOCAL_FLOAT
            if len(memories[-1].floats) <= index:
                while len(memories[-1].floats) < index:
                    memories[-1].push_float(None)
                memories[-1].push_float(value)
            else:
                memories[-1].change_float(index, value)
        else:  # char
            index = dir - LOCAL_CHAR
            if len(memories[-1].chars) <= index:
                while len(memories[-1].chars) < index:
                    memories[-1].push_char(None)
                memories[-1].push_char(value)
            else:
                memories[-1].change_char(index, value)
    elif local_max < dir <= temp_max:  # Temp
        if dir < TEMP_FLOAT:  # int
            index = dir - TEMP_INT
            if len(memories[-1].t_integers) <= index:
                while len(memories[-1].t_integers) < index:
                    memories[-1].push_t_int(None)
                memories[-1].push_t_int(value)
            else:
                memories[-1].change_t_int(index, value)
        elif TEMP_FLOAT <= dir < TEMP_CHAR:  # float
            index = dir - TEMP_FLOAT
            if len(memories[-1].t_floats) <= index:
                while len(memories[-1].t_floats) < index:
                    memories[-1].push_t_float(None)
                memories[-1].push_t_float(value)
            else:
                memories[-1].change_t_float(index, value)
        else:  # char
            index = dir - TEMP_CHAR
            if len(memories[-1].t_chars) <= index:
                while len(memories[-1].chars) < index:
                    memories[-1].push_t_char(None)
                memories[-1].push_t_char(value)
            else:
                memories[-1].change_t_char(index, value)
    else:
        index = dir - CLASS_VAR
        if len(memories[-2].c_vars) <= index:
            while len(memories[-2].c_vars) < index:
                memories[-2].push_c_vars(None)
            memories[-2].push_c_vars(value)
        else:
            memories[-2].change_c_vars(index, value)

#funcion para regresar el valor de las direcciones virtuales en memoria
def get(dir):
    global_max = LOCAL_INT - 1
    local_max = TEMP_INT - 1
    temp_max = CLASS_VAR - 1

    if dir <= global_max:  # Global
        if dir < GLOBAL_FLOAT:  # int
            return memories[0].get_int(dir - 1)
        elif GLOBAL_FLOAT <= dir < GLOBAL_CHAR:  # float
            return memories[0].get_float(dir - GLOBAL_FLOAT)
        else:  # char
            return memories[0].get_char(dir - GLOBAL_CHAR)
    elif global_max < dir <= local_max:  # Local
        if dir < LOCAL_FLOAT:  # int
            return memories[-1].get_int(dir - LOCAL_INT)
        elif LOCAL_FLOAT <= dir < LOCAL_CHAR:  # float
            return memories[-1].get_float(dir - LOCAL_FLOAT)
        else:  # char
            return memories[-1].get_char(dir - LOCAL_CHAR)
    elif local_max < dir <= temp_max:  # Temp
        if dir < TEMP_FLOAT:  # int
            return memories[-1].get_t_int(dir - TEMP_INT)
        elif TEMP_FLOAT <= dir < TEMP_CHAR:  # float
            return memories[-1].get_t_float(dir - TEMP_FLOAT)
        else:  # char
            return memories[-1].get_t_char(dir - TEMP_CHAR)
    else:  # Class vars
        return memories[-2].get_c_vars(dir - CLASS_VAR)

#funcion que ayuda para obtener los valores de los parametros, busca no en la memoria actual local sino en la pasada
def get_param(dir):
    if dir < LOCAL_FLOAT:  # int
        return memories[-2].get_int(dir - LOCAL_INT)
    elif LOCAL_FLOAT <= dir < LOCAL_CHAR:  # float
        return memories[-2].get_float(dir - LOCAL_FLOAT)
    else:  # char
        return memories[-2].get_char(dir - LOCAL_CHAR)


# diferencia entre una constante y un id.
def operand(arg):
    if type(arg) == str:
        try:
            return int(arg)
        except ValueError:
            try:
                return float(arg)
            except ValueError:
                return arg
    else:
        if not getting_param:
            return get(arg)
        else:
            if 9000 < curr_quad[1] <= 18000:
                return get_param(arg)
            else:
                return get(arg)

#funcion que ejecuta el cuadruplo de goto
#cambia currquad a el numero que viene en el quadruplo
def exec_goto():
    global curr_quad_num
    curr_quad_num = curr_quad[3] - 1

#funcion que ejecuta el cuadruplo de gotof
#si es falso ejecuta el goto
def exec_gotof():
    if get(curr_quad[2]) == 0:
        exec_goto()


last_quad = []


#funcion que ejecuta el cuadruplo de gosub
#guarda linea actual de cuadruplo y se va a goto
def exec_gosub():
    global last_quad
    last_quad.append(curr_quad_num)
    exec_goto()

#funcion que ejecuta el cuadruplo de print
def exec_print():
    try:
        print(get(curr_quad[3]))
    except TypeError:
        print(curr_quad[3])


#funcion que ejecuta el cuadruplo de input
#revisa que el valor sea de un tipo correcto
def exec_input():
    if (9000 < curr_quad[3] <= 12000) or (0 < curr_quad[3] <= 3000):
        try:
            value = int(input("Enter the value of " + curr_quad[2] + ': '))
        except ValueError:
            print("ERROR: VALOR DE ENTRADA TIENE QUE SER INT")
            exit(-1)
    elif 12000 < curr_quad[3] <= 15000 or (3000 < curr_quad[3] <= 6000):
        try:
            value = float(input("Enter the value of " + curr_quad[2] + ': '))
        except ValueError:
            print("ERROR: VALOR DE ENTRADA TIENE QUE SER FLOAT")
            exit(-1)
    elif 15000 < curr_quad[3] <= 18000 or (6000 < curr_quad[3] <= 9000):
        # TODO: validar string en char
        try:
            value = input("Enter the value of " + curr_quad[2] + ': ')
        except ValueError:
            print("ERROR: VALOR DE ENTRADA TIENE QUE SER CHAR")
            exit(-1)
    insert(curr_quad[3], value)


funcion_actual = ""
getting_param = False


# funcion que ejecuta el cuadruplo de era
#revisa si necesita parametros, agrega una nueva memoria local y la pone en la pila de memorias
def exec_era():
    global funcion_actual, getting_param
    local_mem = Memory()
    memories.append(local_mem)
    funcion_actual = curr_quad[1]
    global param_checker
    if param_checker == []:
        try:
            param_checker = [] + funciones[funcion_actual]['parametros_vaddr']
            getting_param = True
        except KeyError:
            for clase in tclases:
                if funcion_actual in tclases[clase]['funciones']:
                    try:
                        param_checker = [] + tclases[clase]['funciones'][funcion_actual]['parametros_vaddr']
                        getting_param = True
                    except KeyError:
                        pass

#funcion que revisa si una variable es float
def check_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False


param_checker = []


# funcion que ejecuta el cuadruplo de param
#saca los valores de la pila de parametros
def exec_param():
    global param_checker, getting_param
    if isinstance(curr_quad[1], str):
        if curr_quad[1].isnumeric():
            insert(param_checker.pop(0), int(curr_quad[1]))
        elif check_float(curr_quad[1]):
            insert(param_checker.pop(0), float(curr_quad[1]))
        else:
            insert(param_checker.pop(0), curr_quad[1])
    else:
        if 9000 < curr_quad[1] <= 18000:
            insert(param_checker.pop(0), get_param(curr_quad[1]))
        else:
            insert(param_checker.pop(0), get(curr_quad[1]))
    getting_param = False


retornos = []


# funcion que ejecuta el cuadruplo de return si la funcion tiene retornos agrega valor a la pila de retornos
def exec_ret():
    val = get(curr_quad[3])
    if type(val) is str and val[0] == '[':
        retornos.append(get(int(val[1:-1])))
    else:
        retornos.append(get(curr_quad[3]))

#funcion que ejecuta el cuadruplo de verifica para los arreglos
#checa si esta dentro de los limites
def exec_ver():
    if type(curr_quad[1]) is str:
        if 0 <= int(curr_quad[1]) <= int(curr_quad[3]):
            pass
        else:
            print("ERROR: Fuera de limite.")
            exit(-1)
    else:
        value = get(curr_quad[1])
        if 0 <= value <= int(curr_quad[3]):
            pass
        else:
            print("ERROR: Fuera de limite.")
            exit(-1)

#funcion que ejecuta el cuadruplo de endfunc
# libera la memoria activa local y regresa al cudruplo donde se quedo
def exec_endfunc():
    global curr_quad_num
    memories.pop()
    curr_quad_num = last_quad.pop()
    for key in class_attr_dic.keys():
        class_attr_dic[key] = False
        insert(key, None)

#funcion que ejecuta el cuadruplo de endprog
def exec_endprog():
    exit(0)

#funcion que ejecuta el cuadruplo de or
def exec_or():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand or right_operand)

#funcion que ejecuta el cuadruplo de and
def exec_and():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand and right_operand)

#funcion que ejecuta el cuadruplo de suma +
def exec_add():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand + right_operand)

#funcion que ejecuta el cuadruplo de resta -
def exec_subtract():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand - right_operand)

#funcion que ejecuta el cuadruplo de multiplicacion *
def exec_multiply():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])
    insert(curr_quad[3], left_operand * right_operand)

#funcion que ejecuta el cuadruplo de division /
def exec_divide():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand / right_operand)

#funcion que ejecuta el cuadruplo de assign =
#si el operando empieza con ( o [ es una direccion primero saca esa direccion
#si no es direccion saca el valor e inserta
def exec_assign():
    if type(curr_quad[3]) is str and curr_quad[3][0] == '(':
        curr_quad[3] = get(int(curr_quad[3][1:-1]))

    if type(curr_quad[2]) is str and curr_quad[2][0] == '[':
        class_attr_dic[curr_quad[3]] = True

    val = get(curr_quad[3])
    if type(val) is not str:
        if curr_quad[1] != '_':  # if it is a function
            insert(curr_quad[3], retornos.pop(0))
        else:
            insert(curr_quad[3], operand(curr_quad[2]))
    else:
        if val[0] == '[' and class_attr_dic[curr_quad[3]] is True:
            insert(int(val[1:-1]), operand(curr_quad[2]))
        else:
            if curr_quad[1] != '_':  # if it is a function
                insert(curr_quad[3], retornos.pop(0))
            else:
                insert(curr_quad[3], operand(curr_quad[2]))

#funcion que ejecuta el cuadruplo de >
def exec_gt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand > right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que ejecuta el cuadruplo de <
def exec_lt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand < right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que ejecuta el cuadruplo de >=
def exec_ge():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand >= right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que ejecuta el cuadruplo de <=
def exec_le():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand <= right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que ejecuta el cuadruplo de !=
#revisa que los dos operandos no sean iguales
def exec_ne():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand != right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que ejecuta el cuadruplo de ==
#revisa que los dos operandos sean iguales
def exec_eq():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand == right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)

#funcion que recorre cada cuadruplo hasta ver el de endprog
def exec_quad(quads):
    global curr_quad
    global curr_quad_num
    curr_quad = quads[curr_quad_num].copy()
    while curr_quad[0] != 'ENDPROG':
        for i in range(3):
            slot = curr_quad[i + 1]
            if type(slot) is str and slot[0] == '(':
                # Obtener la direccion guardada en esa direccion
                curr_quad[i + 1] = array_dir(slot[1:-1])
        func = switch.get(curr_quad[0], lambda: "Invalid action")
        func()
        curr_quad_num += 1
        curr_quad = quads[curr_quad_num].copy()
        # memories[-1].print_mem()
        #print(curr_quad)
        #print(get(3001))

#switch para ver que funcion ejecutar en cada cuadruplo
switch = {
    'GOTO': exec_goto,
    'GOTOF': exec_gotof,
    'GOSUB': exec_gosub,
    'PRINT': exec_print,
    'INPUT': exec_input,
    'ERA': exec_era,
    'PARAM': exec_param,
    'RET': exec_ret,
    'VER': exec_ver,
    'ENDFUNC': exec_endfunc,
    'ENDPROG': exec_endprog,
    'or': exec_or,
    'and': exec_and,
    '+': exec_add,
    '-': exec_subtract,
    '*': exec_multiply,
    '/': exec_divide,
    '=': exec_assign,
    '>': exec_gt,
    '<': exec_lt,
    '>=': exec_ge,
    '<=': exec_le,
    '!=': exec_ne,
    '==': exec_eq,
}

#funcion para empezar la vm recibe los quadruplos, dir de funciones, y dir de clases, crea una memoria global y local(main)
def start_vm(_quad, functions, clases):
    global funciones, tclases
    funciones = functions
    for clase in clases.values():
        for variable in clase['variables'].values():
            class_attr_dic[variable['vaddr']] = False
    tclases = clases
    print(" __      ___      _               _   __  __            _     _            ")
    print(" \ \    / (_)    | |             | | |  \/  |          | |   (_)           ")
    print("  \ \  / / _ _ __| |_ _   _  __ _| | | \  / | __ _  ___| |__  _ _ __   ___ ")
    print("   \ \/ / | | '__| __| | | |/ _` | | | |\/| |/ _` |/ __| '_ \| | '_ \ / _ \ ")
    print("    \  /  | | |  | |_| |_| | (_| | | | |  | | (_| | (__| | | | | | | |  __/")
    print("     \/   |_|_|   \__|\__,_|\__,_|_| |_|  |_|\__,_|\___|_| |_|_|_| |_|\___|")
    print("\nOutput:")

    global quad
    quad = _quad
    global_mem = Memory()
    local_mem = Memory()

    memories.append(global_mem)
    memories.append(local_mem)

    exec_quad(quad)

    #print(tclases)
