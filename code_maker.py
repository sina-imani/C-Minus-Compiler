# TODO change the if array

from config import STACK_OFFSET, CALL_FRAME_OFFSET
import scanner
from run_frame import Run_Frame
from scanner import IdentifierType as Type
from typing import TextIO, List

PB: List[str] = []  # program block | each block of program block contains a 3 address command
SEM_ERROR_FILE: TextIO  # file which the semantic errors is written in to it

semantic_correctness = True  # flag to check if program is correct semantically

semantic_stack = []  # semantic stack | use for saving temps and creating PB commands
break_stack = []  # separate break for relop to resolve PB fraction
last_temp = STACK_OFFSET  # start address of heap and stack
last_sem_error_line = 0  # Sina can explain this :)

frame_stack = []


def report_semantic_error(lineno, prompt):
    global semantic_correctness, last_sem_error_line
    if lineno <= last_sem_error_line:
        pass  # I AM REALLY NOT HAPPY TO WRITE THIS :(
    last_sem_error_line = lineno
    semantic_correctness = False
    SEM_ERROR_FILE.write(f'#{lineno}: Semantic Error! {prompt}.\n')


def next_temp():
    """
    Returns: get next temp address
    """
    global last_temp
    last_temp += 4
    return last_temp - 4


def generate_code(operation: str, *components):
    """
    Generates code for a 3-address operation and its associated components.

    This function takes an operation and a variable number of components as inputs, and generates code for a
    3-address operation using these inputs. It first checks the semantic correctness of the code, and if it is not
    correct, it returns without generating code. It then creates a new code string, appends the operation and
    components to it, and appends the code string to the PB (program block) list.

    Args:
        operation (str): The 3-address operation to perform.
        *components: The addresses of the components to be used in the operation.

    Returns:
        None
    """
    if semantic_correctness is False:
        return
    new_code = str(len(PB))
    new_code += '\t(' + operation
    for j in range(3):
        if j < len(components):
            new_code += ', ' + str(components[j])
        elif j < 2:
            new_code += ',  '
        else:
            new_code += ',   '
    new_code += ')'
    PB.append(new_code)

    for c in PB:
        print(c)
    print('*' * 10)


def pnum():
    """
    Assigns a numerical constant to a temporary variable and generates code for it.

    This function gets the next available temporary variable and assigns the value of the last numerical constant to it.
    It then appends the temporary variable to the semantic stack.

    Returns:
        None
    """
    t = next_temp()
    last_type, last_lexeme = scanner.get_last_token()
    if last_type != 'NUM':
        raise Exception(f'code maker : improper type : {last_type} instead of NUM')
    generate_code('ASSIGN', '#' + last_lexeme, t)
    semantic_stack.append(t)


def temp_exch():
    """
    Exchange an array or function symbol on the semantic stack with a temporary variable.

    This function pops the address and line number of a symbol from the semantic stack, and checks if it is an array
    or function. If the symbol is an array, it pushes its address, line number, and the string 'array' onto the
    semantic stack. If the symbol is a function, it reports a semantic error indicating a type mismatch. Otherwise,
    it generates code to assign the symbol's address to a new temporary variable, and pushes the temporary variable
    onto the semantic stack.

    Returns:
        None
    """
    a_index = semantic_stack.pop()
    a_line = semantic_stack.pop()
    a_entry = scanner.symbol_list[a_index]
    if a_entry.is_function:
        report_semantic_error(a_line, "Type mismatch in operands, Got function instead of int")
    if a_entry.id_type == Type.array:
        semantic_stack.append(a_index)
        semantic_stack.append(a_line)
        semantic_stack.append('array')
        return
    a = a_entry.address
    t = next_temp()
    generate_code('ASSIGN', a, t)
    semantic_stack.append(t)


def pid():
    """
    Processes an identifier and adds its symbol to the semantic stack.

    This function gets the last processed token from the scanner, which should be an identifier. It then looks up the
    identifier in the symbol table, and if it is found, it appends its line number and index to the semantic stack.
    If it is not found, it reports a semantic error and appends a default symbol index of 0 to the semantic stack.

    Returns:
        None
    """
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
    """
    Adds an 'ADD' operation to the semantic stack.

    This function is called when the parser encounters a + operation in the input.
    It appends the 'ADD' operation to the semantic stack.

    Returns:
        None
    """
    semantic_stack.append('ADD')


def pminus():
    """
    Adds a 'SUB' operation to the semantic stack.

    This function is called when the parser encounters a - operation in the input.
    It appends the 'SUB' operation to the semantic stack.

    Returns:
        None
    """
    semantic_stack.append('SUB')


def pless():
    """
    Adds an 'LT' operation to the semantic stack.

    This function is called when the parser encounters a < operation in the input.
    It appends the 'LT' operation to the semantic stack.

    Returns:
        None
    """
    semantic_stack.append('LT')


def peq():
    """
    Adds an 'EQ' operation to the semantic stack.

    This function is called when the parser encounters a = operation in the input.
    It appends the 'EQ' operation to the semantic stack.

    Returns:
        None
    """
    semantic_stack.append('EQ')


def ptimes():
    """
    Adds a 'MULT' operation to the semantic stack.

    This function is called when the parser encounters a * operation in the input.
    It appends the 'MULT' operation to the semantic stack.

    Returns:
        None
    """
    semantic_stack.append('MULT')


def assign():
    """
    Handles assignment statements.

    This function pops the value to be assigned from the semantic stack, as well as the symbol to which the value
    will be assigned. It checks that the symbol is an integer variable and not a function, and that the value to be
    assigned is also an integer. If either of these conditions is not met, it reports a semantic error. If the symbol
    is an array, it pops the line number and a useless symbol table entry from the semantic stack. It then generates
    code to assign the value to the symbol's address, and pushes the value back onto the semantic stack.

    Returns:
        None
    """
    t_line = 0
    t = semantic_stack.pop()

    if t == 'array':
        t_line = semantic_stack.pop()
        semantic_stack.pop()  # pop the useless symbol table entry

    if t == 'int':
        t = semantic_stack.pop()

    # check type
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
    """
        Handles assignment statements for arrays.

        This function pops the index and value to be assigned from the semantic stack, as well as the symbol
        representing the array. It checks that the array symbol is actually an array and not a function, and that the
        index is an integer and the value is an integer or an integer array. If any of these conditions is not met,
        it reports a semantic error. It then generates code to compute the address of the element to be assigned,
        and to assign the value to that address. Finally, it pushes the value back onto the semantic stack.

        Returns:
            None
    """
    val_line, ind_line = 0, 0
    val = semantic_stack.pop()

    if val == 'array':
        val_line = semantic_stack.pop()
        semantic_stack.pop()

    ind = semantic_stack.pop()

    if ind == 'array':
        ind_line = semantic_stack.pop()
        semantic_stack.pop()

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
    """
      Handles the end of an expression.

      This function pops the top element from the semantic stack, which should be the value of the expression.
      If the value is an array, it also pops a useless symbol table entry from the semantic stack.

      Returns:
          None
      """
    exp = semantic_stack.pop()
    if exp == 'array':
        semantic_stack.pop()
        semantic_stack.pop()


def do_op():
    """
    Handles operations.

    This function pops the top two elements from the semantic stack, which should be the second operand and the first
    operand. If either operand is an array, it also pops a useless symbol table entry from the semantic stack. It
    checks that the operands are integers and not arrays, and reports a semantic error if either of these conditions
    is not met. It generates code to perform the operation on the operands, and pushes the result back onto the
    semantic stack.

    Returns:
        None
    """

    t1_line, t2_line = 0, 0
    t2 = semantic_stack.pop()
    if t2 == 'array':
        t2_line = semantic_stack.pop()
        semantic_stack.pop()

    op = semantic_stack.pop()
    t1 = semantic_stack.pop()
    if t1 == 'array':
        t1_line = semantic_stack.pop()
        semantic_stack.pop()
        report_semantic_error(t1_line, f'Type mismatch in operands, Got array instead of int')
        t1 = 0
    if t2 == 'array':
        report_semantic_error(t2_line, f'Type mismatch in operands, Got array instead of int')
    generate_code(op, t1, t2, t1)
    semantic_stack.append(t1)


def eval_ind():
    """
    Evaluates an array index.

    This function pops the top element from the semantic stack, which should be the index of the array element to be
    accessed. It then looks at the second-to-top element of the stack, which should be the symbol table index for the
    array symbol. It generates code to compute the address of the element to be accessed, and to assign that address
    to the second-to-top element of the stack.

    Returns:
        None
    """
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
        semantic_stack.pop()

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
        semantic_stack.pop()
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
    last_arg_index = -1
    last_arg = semantic_stack.pop()
    if last_arg == 'array':
        last_arg_line = semantic_stack.pop()
        last_arg_index = semantic_stack.pop()

    n = semantic_stack.pop()

    if last_arg == 'array':
        semantic_stack.append(last_arg_index)
        semantic_stack.append(last_arg_line)

    semantic_stack.append(last_arg)
    semantic_stack.append(n + 1)


def call_frame_push(reg: int):
    sp = 12  # TODO : clean code
    generate_code('ASSIGN', str(reg), f'@{sp}')
    generate_code('SUB', f'{sp}', '#4', f'{sp}')


def call_frame_pop(reg: int):
    sp = 12  # TODO: clean code
    generate_code('ADD', f'{sp}', '#4', f'{sp}')
    generate_code('ASSIGN', f'@{sp}', str(reg))


def create_frame():
    # get caller data
    caller = scanner.get_current_scope()
    caller_params_number = len(caller.parameter_list)
    caller_first_temp = caller.temp_begin_address
    temp_used_number = (last_temp - caller_first_temp) >> 2

    # push return address into frame
    ra = 8  # TODO : clean
    call_frame_push(ra)

    # push params
    for i in range(caller_params_number):
        reg = caller.address + (i * 4)
        call_frame_push(reg)

    # push temps
    for i in range(temp_used_number):
        reg = caller_first_temp + (i * 4)
        call_frame_push(reg)


def destroy_frame():
    # get caller data
    caller = scanner.get_current_scope()
    caller_params_number = len(caller.parameter_list)
    caller_first_temp = caller.temp_begin_address
    temp_used_number = (last_temp - caller_first_temp) >> 2

    # pop temps
    for i in range(temp_used_number - 1, -1, -1):
        reg = caller_first_temp + (i * 4)
        call_frame_pop(reg)

    # pop params
    for i in range(caller_params_number - 1, -1, -1):
        reg = caller.address + (i * 4)
        call_frame_pop(reg)

    # pop return address
    ra = 8
    call_frame_pop(ra)


def call_set_params(parameters, callee_func_address):
    for i in range(len(parameters)):
        if parameters[i][0] == Type.array:
            generate_code('ASSIGN', str(parameters[i][1]), callee_func_address + ((i + 1) << 2))
        else:
            generate_code('ASSIGN', str(parameters[i][1]), callee_func_address + ((i + 1) << 2))


def call():
    n = semantic_stack.pop()
    parameters = []
    for _ in range(n):
        arg = semantic_stack.pop()
        if arg == 'array':
            line = semantic_stack.pop()
            arg = semantic_stack.pop()
            parameters.append((Type.array, scanner.symbol_list[arg].address))
        else:
            parameters.append((Type.int, arg))
    parameters.reverse()
    f_index = semantic_stack.pop()
    semantic_stack.pop()  # f_line
    f = scanner.symbol_list[f_index]

    if f.is_function is False:
        raise Exception(f'code maker : expected {f.lexeme} to be function but it was not')
    if len(f.parameter_list) != n:
        report_semantic_error(scanner.line_number, f"Mismatch in numbers of arguments of '{f.lexeme}'")
    else:
        for i in range(len(parameters)):
            if parameters[i][0] != f.parameter_list[i]:
                report_semantic_error(scanner.line_number,
                                      f"Mismatch in type of argument {i + 1} of '{f.lexeme}'. " +
                                      f"Expected '{f.parameter_list[i].name}' but got '{parameters[i][0].name}'"
                                      f" instead")

        if f.lexeme == 'output':
            generate_code('PRINT', parameters[0][1])
        else:
            create_frame()
            call_set_params(parameters, f.address)
            ra = 8  # TODO clean code
            generate_code('ASSIGN', f'#{len(PB) + 2}', 8)
            generate_code('JP', scanner.get_func_entry_point(f.lexeme))
            destroy_frame()

    if f.id_type == Type.array:
        semantic_stack.append(scanner.line_number)

    if f.id_type != Type.void:
        v = 16  # TODO clean this
        semantic_stack.append(v)

    semantic_stack.append(f.id_type.name)


def check_void():
    if scanner.symbol_list[-1].id_type == Type.void and not scanner.symbol_list[-1].is_function:
        report_semantic_error(scanner.last_type_line_number,
                              f"Illegal type of void for '{scanner.symbol_list[-1].lexeme}'")


def start_declaration():
    scanner.start_declaration()


def start_params():
    scanner.symbol_list[-1].temp_begin_address = last_temp
    if scanner.symbol_list[-1].lexeme == 'main':
        patched_line = semantic_stack.pop()
        PB[patched_line] = f'{patched_line}\t(JP, {len(PB)},  ,   )'

    scanner.start_params(len(PB))


def end_declaration():
    scanner.set_declaration_mode(scanner.DeclarationMode.Disabled)
    check_void()


def return_call():
    f = scanner.get_current_scope()
    if f.lexeme != 'main':
        if f.id_type != Type.void:
            v = 16  # TODO clean this
            generate_code('ASSIGN', last_temp - 4, 16)

    generate_code('JP', '@8')


def end_scope():
    f = scanner.get_current_scope()
    if f.id_type != Type.void:
        v = 16  # TODO clean this
        generate_code('ASSIGN', last_temp - 4, 16)

    if f.lexeme != 'main':
        generate_code('JP', '@8')

    scanner.end_scope()


def init():
    generate_code('ASSIGN', '#0', 8)
    generate_code('ASSIGN', f'#{CALL_FRAME_OFFSET}', 12)

    make_patch()


def do_action(action_symbol: str):
    func_name = action_symbol[1:].replace('-', '_')
    globals()[func_name]()
