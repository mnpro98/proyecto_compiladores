import numpy as np

virtual_memory = {
    "mem_stack": [],
    "quad": [],
}

curr_quad = []


# Differentiates between a constant and an id.
def operand(arg):
    if type(arg) == str:
        try:
            return int(arg)
        except ValueError:
            return float(arg)
    else:
        return virtual_memory['mem_stack'][arg]


def exec_goto():
    new_quad = np.array(virtual_memory['quad'])
    exec_quad(new_quad[curr_quad[3]:])


def exec_gotof():
    if virtual_memory['mem_stack'][curr_quad[2]] == 0:
        exec_goto()


# TODO
def exec_gosub():
    exec_goto()


def exec_print():
    print(virtual_memory['mem_stack'][curr_quad[3]])


# TODO
def exec_era():
    print("era")


# TODO
def exec_param():
    print("param")


# TODO
def exec_ret():
    pass


def exec_endfunc():
    print("endfunc")


def exec_endprog():
    exit(0)


def exec_add():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    virtual_memory['mem_stack'][curr_quad[3]] = left_operand + right_operand


def exec_subtract():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    virtual_memory['mem_stack'][curr_quad[3]] = left_operand - right_operand


def exec_multiply():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    virtual_memory['mem_stack'][curr_quad[3]] = left_operand * right_operand


def exec_divide():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    virtual_memory['mem_stack'][curr_quad[3]] = left_operand / right_operand


def exec_assign():
    if curr_quad[1] != '_':  # if it is a function
        virtual_memory['mem_stack'][curr_quad[3]] = operand(curr_quad[1])
    else:
        virtual_memory['mem_stack'][curr_quad[3]] = operand(curr_quad[2])


def exec_gt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand > right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_lt():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand < right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_ge():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand >= right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_le():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand <= right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_ne():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand != right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_eq():
    left_operand = operand(curr_quad[1])
    right_operand = operand(curr_quad[2])

    if left_operand == right_operand:
        result = 1
    else:
        result = 0

    virtual_memory['mem_stack'][curr_quad[3]] = result


def exec_quad(quads):
    global curr_quad
    for _quad in quads:
        func = switch.get(_quad[0], lambda: "Invalid action")
        curr_quad = _quad
        func()
        if _quad[0] == "GOTO":
            break


switch = {
    'GOTO': exec_goto,
    'GOTOF': exec_gotof,
    'GOSUB': exec_gosub,
    'PRINT': exec_print,
    'ERA': exec_era,
    'PARAM': exec_param,
    'RET': exec_ret,
    'ENDFUNC': exec_endfunc,
    'ENDPROG': exec_endprog,
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


def start_vm(quad, functions):
    print("VM")
    virtual_memory['mem_stack'] = [None]*27000
    virtual_memory['quad'] = quad
    exec_quad(quad)
