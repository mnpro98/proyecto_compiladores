from typing import ValuesView


quad = []
memories = []

curr_quad = []
curr_quad_num = 0

GLOBAL_INT = 1
GLOBAL_FLOAT = 3001
GLOBAL_CHAR = 6001

LOCAL_INT = 9001
LOCAL_FLOAT = 12001
LOCAL_CHAR = 15001

TEMP_INT = 18001
TEMP_FLOAT = 21001
TEMP_CHAR = 24001

funciones = {}


class Memory:
    integers: list
    floats: list
    chars: list

    t_integers: list
    t_floats: list
    t_chars: list

    def __init__(self):
        self.integers = []
        self.floats = []
        self.chars = []
        self.t_integers = []
        self.t_floats = []
        self.t_chars = []

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

    def get_int(self, index):
        return self.integers[index]

    def get_float(self, index):
        return self.floats[index]

    def get_char(self, index):
        return self.chars[index]

    def get_t_int(self, index):
        return self.t_integers[index]

    def get_t_float(self, index):
        return self.t_floats[index]

    def get_t_char(self, index):
        return self.t_chars[index]
    
    def print_mem(self):
        print("int", self.integers)
        print("float", self.floats)
        print("char", self.chars)
        print("tint", self.t_integers)
        print("tfloat", self.t_floats)
        print("tchar", self.t_chars)


def insert(dir, value):
    global_max = LOCAL_INT - 1
    local_max = TEMP_INT - 1

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
    else:  # Temp
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


def get(dir):
    global_max = LOCAL_INT - 1
    local_max = TEMP_INT - 1

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
    else:  # Temp
        if dir < TEMP_FLOAT:  # int
            return memories[-1].get_t_int(dir - TEMP_INT)
        elif TEMP_FLOAT <= dir < TEMP_CHAR:  # float
            return memories[-1].get_t_float(dir - TEMP_FLOAT)
        else:  # char
            return memories[-1].get_t_char(dir - TEMP_CHAR)


def get_param(dir):
    if dir < LOCAL_FLOAT:  # int
        return memories[-2].get_int(dir - LOCAL_INT)
    elif LOCAL_FLOAT <= dir < LOCAL_CHAR:  # float
        return memories[-2].get_float(dir - LOCAL_FLOAT)
    else:  # char
        return memories[-2].get_char(dir - LOCAL_CHAR)


# Differentiates between a constant and an id.
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
            if curr_quad[1] > 9000 and curr_quad[1] <= 18000:
                return get_param(arg)
            else:
                return get(arg)



def exec_goto():
    global curr_quad_num
    curr_quad_num = curr_quad[3] - 1


def exec_gotof():
    if get(curr_quad[2]) == 0:
        exec_goto()

last_quad = []
# TODO
def exec_gosub():
    global last_quad
    last_quad.append(curr_quad_num)
    exec_goto()


def exec_print():
    try:
        print(get(curr_quad[3]))
    except TypeError:
        print(curr_quad[3])

def exec_input():
    if (curr_quad[3] > 9000 and curr_quad[3] <= 12000) or (curr_quad[3] > 0 and curr_quad[3] <= 3000):
        try:
            value = int(input("Enter the value of " + curr_quad[2] + ': '))
        except ValueError:
            print("ERROR: VALOR TIENE QUE SER INT")
            exit(-1)
    elif curr_quad[3] > 12000 and curr_quad[3] <= 15000 or (curr_quad[3] > 3000 and curr_quad[3] <= 6000):
        try:
            value = float(input("Enter the value of " + curr_quad[2] + ': '))
        except ValueError:
            print("ERROR: VALOR TIENE QUE SER FLOAT")
            exit(-1)
    elif curr_quad[3] > 15000 and curr_quad[3] <= 18000 or (curr_quad[3] > 6000 and curr_quad[3] <= 9000):
        #TODO: validar string en char
        try:
            value = input("Enter the value of " + curr_quad[2] + ': ')
        except ValueError:
            print("ERROR: VALOR TIENE QUE SER CHAR")
            exit(-1)
    insert(curr_quad[3], value)

funcion_actual = ""
getting_param = False
# TODO reserva espacio para variables locales
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
            pass

def check_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False


param_checker = []
# TODO pasas los parametros y validas mismo numero
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
        if curr_quad[1] > 9000 and curr_quad[1] <= 18000:
            insert(param_checker.pop(0), get_param(curr_quad[1]))
        else:
            insert(param_checker.pop(0), get(curr_quad[1]))
    getting_param = False


retornos = []


# TODO regresa valor si es que tiene return
def exec_ret():
    retornos.append(get(curr_quad[3]))

# libera la memoria
def exec_endfunc():
    global curr_quad_num
    memories.pop()
    curr_quad_num = last_quad.pop()


def exec_endprog():
    exit(0)


def exec_or():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand or right_operand)


def exec_and():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand and right_operand)


def exec_add():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand + right_operand)


def exec_subtract():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand - right_operand)


def exec_multiply():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])
    insert(curr_quad[3], left_operand * right_operand)


def exec_divide():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    insert(curr_quad[3], left_operand / right_operand)


def exec_assign():
    if curr_quad[1] != '_':  # if it is a function
        insert(curr_quad[3], retornos.pop(0))
    else:
        insert(curr_quad[3], operand(curr_quad[2]))


def exec_gt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand > right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_lt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand < right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_ge():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand >= right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_le():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand <= right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_ne():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand != right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_eq():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand == right_operand:
        result = 1
    else:
        result = 0

    insert(curr_quad[3], result)


def exec_quad(quads):
    global curr_quad
    global curr_quad_num
    while quads[curr_quad_num][0] != 'ENDPROG':
        func = switch.get(quads[curr_quad_num][0], lambda: "Invalid action")
        curr_quad = quads[curr_quad_num]
        func()
        curr_quad_num += 1
        #print(curr_quad)


switch = {
    'GOTO': exec_goto,
    'GOTOF': exec_gotof,
    'GOSUB': exec_gosub,
    'PRINT': exec_print,
    'INPUT': exec_input,
    'ERA': exec_era,
    'PARAM': exec_param,
    'RET': exec_ret,
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


def start_vm(_quad, functions):
    global funciones
    funciones = functions
    print("VM")
    global quad
    quad = _quad
    global_mem = Memory()
    local_mem = Memory()

    memories.append(global_mem)
    memories.append(local_mem)

    exec_quad(quad)
