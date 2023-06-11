# IAWT

import scanner
from scanner import IdentifierType as Type
from typing import TextIO

# VARIABLES


PB = []
SEM_ERROR_FILE : TextIO
semantic_correctness = True
semantic_stack = []
break_stack = []
last_temp = scanner.TEMP_OFFSET
last_sem_error_line = 0



# FUNCTIONS
def report_semantic_error(lineno, prompt):
    global semantic_correctness, last_sem_error_line
    if lineno <= last_sem_error_line:
        pass # I AM REALLY NOT HAPPY TO WRITE THIS :(
    last_sem_error_line = lineno
    semantic_correctness = False
    SEM_ERROR_FILE.write(f'#{lineno}: Semantic Error! {prompt}.\n')

def next_temp():
    global last_temp
    last_temp += 4
    return last_temp - 4

def generate_code(operation : str, *components):
    if semantic_correctness is False:
        return
    new_code = str(len(PB))
    new_code += '\t(' + operation
    for j in range(3):
        if j < len(components):
            new_code += ', ' + str(components[j])
        elif j < 2:
            new_code += (',  ')
        else:
            new_code += ',   '
    new_code += ')'
    PB.append(new_code)

def pnum():
    t = next_temp()
    last_type, last_lexeme = scanner.get_last_token()
    if last_type != 'NUM':
        raise Exception(f'code maker : improper type : {last_type} instead of NUM')
    generate_code('ASSIGN', '#' + last_lexeme, t)
    semantic_stack.append(t)


def temp_exch():
    a_index = semantic_stack.pop()
    a_line = semantic_stack.pop()
    a_entry = scanner.symbol_list[a_index]
    if a_entry.is_function:
        report_semantic_error(a_line, "Type mismatch in operands, Got function instead of int")
    if a_entry.id_type == Type.array:
        semantic_stack.append(a_line)
        semantic_stack.append('array')
        return
    a = a_entry.address
    t = next_temp()
    generate_code('ASSIGN', a, t)
    semantic_stack.append(t)


def pid():
    last_type, last_lexeme = scanner.get_last_token()
    if last_type != 'ID':
        raise Exception("code maker : last token type expected to be ID, but was " + last_type)
    sym_index = scanner.symbol_table_lookup(last_lexeme)
    if sym_index == -1:
        report_semantic_error(scanner.line_number, f"'{last_lexeme}' is not defined")
        sym_index = 0
    semantic_stack.append(scanner.line_number)
    semantic_stack.append(sym_index)


def pplus():
    semantic_stack.append('ADD')


def pminus():
    semantic_stack.append('SUB')


def pless():
    semantic_stack.append('LT')


def peq():
    semantic_stack.append('EQ')

def ptimes():
    semantic_stack.append('MULT')

def assign():
    t_line = 0
    t = semantic_stack.pop()
    if t == 'array':
        t_line = semantic_stack.pop()
    a_index = semantic_stack.pop()
    a_line = semantic_stack.pop()
    a_entry = scanner.symbol_list[a_index]
    if a_entry.id_type != Type.int:
        report_semantic_error(a_line,
                              f"Type mismatch in operands, Got {a_entry.id_type.name} instead of int")
    if a_entry.is_function:
        report_semantic_error(a_line,
                              "Type mismatch in operands, Got function instead of int")
    if t == 'array':
        report_semantic_error(t_line, "Type mismatch in operands, Got array instead of int")
        t = 0
    a = a_entry.address
    generate_code('ASSIGN', t, a)
    semantic_stack.append(t)

def assign_arr():
    val_line, ind_line = 0, 0
    val = semantic_stack.pop()
    if val == 'array':
        val_line = semantic_stack.pop()
    ind = semantic_stack.pop()
    if ind == 'array':
        ind_line = semantic_stack.pop()
    a_index = semantic_stack.pop()
    a_line = semantic_stack.pop()
    a_entry = scanner.symbol_list[a_index]
    if a_entry.id_type != Type.array:
        report_semantic_error(a_line,
                              f"Type mismatch in operands, Got {a_entry.id_type.name} instead of array")
    if a_entry.is_function:
        report_semantic_error(a_line,
                              "Type mismatch in operands, Got function instead of array")
    if ind == 'array':
        report_semantic_error(ind_line, "Type mismatch in operands, Got array instead of int")
    if val == 'array':
        report_semantic_error(val_line, "Type mismatch in operands, Got array instead of int")
        val = 0
    a = a_entry.address
    generate_code('MULT', ind, '#4', ind)
    generate_code('ADD', '#' + str(a), ind, ind)
    generate_code('ASSIGN', val, '@' + str(ind))
    semantic_stack.append(val)

def end_expression():
    exp = semantic_stack.pop()
    if exp == 'array':
        semantic_stack.pop()

def do_op():
    t1_line, t2_line = 0, 0
    t2 = semantic_stack.pop()
    if t2 == 'array':
        t2_line = semantic_stack.pop()
    op = semantic_stack.pop()
    t1 = semantic_stack.pop()
    if t1 == 'array':
        t1_line = semantic_stack.pop()
        report_semantic_error(t1_line, f'Type mismatch in operands, Got array instead of int')
        t1 = 0
    if t2 == 'array':
        report_semantic_error(t2_line, f'Type mismatch in operands, Got array instead of int')
    generate_code(op, t1, t2, t1)
    semantic_stack.append(t1)


def do_mult():
    t2 = semantic_stack.pop()
    t1 = semantic_stack.pop()
    generate_code('MULT', t1, t2, t1)
    semantic_stack.append(t1)


def eval_ind():
    ind = semantic_stack.pop()
    t = semantic_stack[-1]
    generate_code('MULT', ind, '#4', ind)
    generate_code('ADD', t, ind, t)
    generate_code('ASSIGN', '@' + str(t), t)


def eval_ind_orig():
    t_line = 0
    t = semantic_stack.pop()
    if t == 'array':
        t_line = semantic_stack.pop()
    a_index = semantic_stack.pop()
    a_line = semantic_stack.pop()
    a_entry = scanner.symbol_list[a_index]
    if a_entry.id_type != Type.array:
        report_semantic_error(a_line, 
                              f"Type mismatch in operands, Got {a_entry.id_type.name} instead of array")
    if a_entry.is_function:
        report_semantic_error(a_line, 
                              "Type mismatch in operands, Got function instead of array")
    if t == 'array':
        report_semantic_error(t_line, "Type mismatch in operands, Got array instead of int")
        t = 0
    a = a_entry.address
    generate_code('MULT', t, '#4', t)
    generate_code('ADD', '#' + str(a), t, t)
    generate_code('ASSIGN', '@' + str(t), t)
    semantic_stack.append(t)

def expect_temp():
    t = semantic_stack.pop()
    if t == 'array':
        t_line = semantic_stack.pop()
        report_semantic_error(t_line, f'Type mismatch in operands, Got array instead of int')
        t = 0
    semantic_stack.append(t)

def make_patch():
    semantic_stack.append(len(PB))
    PB.append('')


def end_if():
    a2 = semantic_stack.pop()
    a1 = semantic_stack.pop()
    t = semantic_stack.pop()
    PB[a2] = f'{a2}\t(JP, {len(PB)},  ,   )'
    PB[a1] = f'{a1}\t(JPF, {t}, {a2 + 1},   )'


def start_repeat():
    semantic_stack.append(len(PB))
    break_stack.append(0)


def brk():
    if not break_stack:
        report_semantic_error(scanner.line_number, "No 'repeat ... until' found for 'break'")
        return
    n = break_stack.pop()
    break_stack.append(len(PB))
    break_stack.append(n + 1)
    PB.append('')


def end_repeat():
    expect_temp()
    t = semantic_stack.pop()
    a = semantic_stack.pop()
    generate_code('JPF', t, a)
    break_cnt = break_stack.pop()
    for _ in range(break_cnt):
        break_addr = break_stack.pop()
        PB[break_addr] = f'{break_addr}\t(JP, {len(PB)},  ,   )'

def start_args():
    semantic_stack.append(0)

def new_arg():
    last_arg_line = -1
    last_arg = semantic_stack.pop()
    if last_arg == 'array':
        last_arg_line = semantic_stack.pop()
    n = semantic_stack.pop()
    if last_arg == 'array':
        semantic_stack.append(last_arg_line)
    semantic_stack.append(last_arg)
    semantic_stack.append(n + 1)

def call():
    n = semantic_stack.pop()
    parameters = []
    for _ in range(n):
        arg = semantic_stack.pop()
        if arg == 'array':
            semantic_stack.pop()
            parameters.append((Type.array, 'array'))
        else:
            parameters.append((Type.int, arg))
    f_index = semantic_stack.pop()
    _ = semantic_stack.pop() # f_line
    f = scanner.symbol_list[f_index]
    if f.is_function is False:
        raise Exception(f'code maker : expected {f.lexeme} to be function but it was not')
    if len(f.parameter_list) != n:
        report_semantic_error(scanner.line_number, f"Mismatch in numbers of arguments of '{f.lexeme}'")
    elif f.lexeme == 'output':
        generate_code('PRINT', parameters[0][1])
    if f.id_type == Type.array:
        semantic_stack.append(scanner.line_number)
    semantic_stack.append(f.id_type.name)

def check_void():
    if scanner.symbol_list[-1].id_type == Type.void and not scanner.symbol_list[-1].is_function:
        report_semantic_error(scanner.last_type_line_number, 
                              f"Illegal type of void for '{scanner.symbol_list[-1].lexeme}'")

def start_declaration():
    scanner.start_declaration()

def start_params():
    scanner.start_params()

def end_declaration():
    scanner.set_declaration_mode(scanner.DeclarationMode.Disabled)
    check_void()

def end_scope():
    scanner.end_scope()

def do_action(action_symbol : str):
    eval(action_symbol[1:].replace('-', '_') + '()')