# IAWT

import scanner


# VARIABLES
PB = None

semantic_stack = []
break_stack = []
last_temp = scanner.TEMP_OFFSET
PB = []


# FUNCTIONS
def next_temp():
    global last_temp
    last_temp += 4
    return last_temp - 4

def generate_code(operation : str, *components):
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

def ptoken():
    t = next_temp()
    last_type, last_lexeme = scanner.get_last_token()
    if last_type == 'NUM':
        generate_code('ASSIGN', '#' + last_lexeme, t)
    elif last_type == 'ID':
        sym_index = scanner.symbol_table_lookup(last_lexeme)
        if sym_index == -1:
            raise Exception("code maker : cannot find symbol with lexeme " + last_lexeme)
        sym_address = scanner.symbol_list[sym_index].address
        generate_code('ASSIGN', sym_address, t)
    else:
        raise Exception("code maker : token to be pushed is not either of type NUM nor ID")
    semantic_stack.append(t)


def temp_exch():
    a = semantic_stack.pop()
    if a == 'function':
        return
    t = next_temp()
    generate_code('ASSIGN', a, t)
    semantic_stack.append(t)

def pid():
    last_type, last_lexeme = scanner.get_last_token()
    if last_type != 'ID':
        raise Exception("code maker : last token type expected to be ID, but was " + last_type)
    sym_index = scanner.symbol_table_lookup(last_lexeme)
    if sym_index == -1:
        raise Exception("code maker : cannot find symbol with lexeme " + last_lexeme)
    if scanner.symbol_list[sym_index].is_function:
        semantic_stack.append('function')
    else:
        semantic_stack.append(scanner.symbol_list[sym_index].address)

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
    t = semantic_stack.pop()
    a = semantic_stack.pop()
    generate_code('ASSIGN', t, a)

def assign_arr():
    val = semantic_stack.pop()
    ind = semantic_stack.pop()
    a  = semantic_stack.pop()
    generate_code('MULT', ind, '#4', ind)
    generate_code('ADD', '#' + str(a), ind, ind)
    generate_code('ASSIGN', val, '@' + str(ind))

def do_op():
    t2 = semantic_stack.pop()
    op = semantic_stack.pop()
    t1 = semantic_stack.pop()
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
    t = semantic_stack.pop()
    a = semantic_stack.pop()
    generate_code('MULT', t, '#4', t)
    generate_code('ADD', '#' + str(a), t, t)
    generate_code('ASSIGN', '@' + str(t), t)
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
    n = break_stack.pop()
    break_stack.append(len(PB))
    break_stack.append(n + 1)
    PB.append('')


def end_repeat():
    t = semantic_stack.pop()
    a = semantic_stack.pop()
    generate_code('JPF', t, a)
    break_cnt = break_stack.pop()
    for _ in range(break_cnt):
        break_addr = break_stack.pop()
        PB[break_addr] = f'{break_addr}\t(JP, {len(PB)},  ,   )'

def call_output():
    a = semantic_stack.pop()
    generate_code('PRINT', a)

def start_declaration():
    scanner.start_declaration()

def start_params():
    scanner.start_params()

def end_declaration():
    scanner.set_declaration_mode(scanner.DeclarationMode.Disabled)

def end_scope():
    scanner.end_scope()

def do_action(action_symbol : str):
    eval(action_symbol[1:].replace('-', '_') + '()')