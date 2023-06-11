# IAWT
import enum

## GLOBAL VARIABLES

SILENT_MODE = True  # Silent mode turned on means that no lexical error will be reported in the corresponding file
NEW_LINE = '\r\n'
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
KEYWORDS = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']
INPUT_FILE = None
ERROR_FILE = None
TOKEN_FILE = None
SYMBOL_FILE = None

symbol_list = []
save_in_buffer = True
current_char = None
ready_char = None
read_buffer = []
line_number = 1
token_lexeme = ''
token_type = ''
last_token_lexem = ''
last_token_type = ''
last_token_line_number = 0
last_error_line_number = 0
last_type_line_number : int
last_param_type : str
declaration_mode = None
last_kw = None
scope_stack = []
MAX_CODE_LENGTH = 100
MAX_DATA_LENGTH = 400
TEMP_OFFSET = MAX_CODE_LENGTH + MAX_DATA_LENGTH
first_empty_data = MAX_CODE_LENGTH


## CLASSES AND ENUMS
class DeclarationMode(enum.Enum):
    Disabled = 0
    Name = 1
    Parameter = 2


class IdentifierType(enum.Enum):
    void = 0
    int = 1
    int_array = 2


class SymbolTableEntry:
    def __init__(self):
        global first_empty_data
        self.lexeme = ''
        self.id_type = IdentifierType.void
        self.is_function = False
        self.parameter_list = []  # types of parameters, respectively
        if declaration_mode == DeclarationMode.Name:
            self.address = first_empty_data
            first_empty_data += 4
        self.array_length = 0
        symbol_list.append(self)


declaration_mode = DeclarationMode.Disabled
symbol_list: list[SymbolTableEntry] = []


## FUNCTIONS


# Characters: reading


def enable_buffer_saving():
    save_in_buffer = True


def disable_buffer_saving():
    save_in_buffer = False


def read_next_char():
    global current_char, ready_char, line_number
    if INPUT_FILE is None:
        return
    if ready_char is None:
        current_char = INPUT_FILE.read(1)
    else:
        current_char = ready_char
        ready_char = None
    if current_char == '\n':
        line_number += 1
    if save_in_buffer:
        read_buffer.append(current_char)


def unread_last_char():
    global current_char, line_number, ready_char
    if current_char == '\n':
        line_number -= 1
    ready_char = current_char
    current_char = None
    if read_buffer and save_in_buffer:
        del read_buffer[-1]


# Characters: examination


def is_numeric(chr):
    return '0' <= chr <= '9'


def is_letter(chr):
    return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z'


def is_numeric_letter(chr):
    return is_letter(chr) or is_numeric(chr)


def is_whitespace(chr):
    return chr in WHITE_SPACES


def is_white_slash(chr):
    return chr in WHITE_SPACES or chr == '/'


def is_symbol(chr):
    return chr in SYMBOLS


def is_invalid_char(chr):
    if chr == '':
        return False
    if is_numeric(chr) or is_letter(chr):
        return False
    elif chr in SYMBOLS or is_white_slash(chr):
        return False
    return True


# Token extraction


def extract_number():
    read_next_char()
    if not is_numeric(current_char):
        unread_last_char()
        return False
    read_next_char()
    while is_numeric(current_char):
        read_next_char()

    if is_invalid_char(current_char) or is_letter(current_char):
        report_invalid_number()
    else:
        unread_last_char()
        add_number_token()
    return True


def extract_id_kw():
    read_next_char()
    if not is_letter(current_char):
        unread_last_char()
        return False
    read_next_char()
    while is_numeric_letter(current_char):
        read_next_char()

    if is_invalid_char(current_char):
        report_invalid_input()
    else:
        unread_last_char()
        add_id_kw_token()
    return True


def extract_symbol():
    read_next_char()
    if not is_symbol(current_char):
        unread_last_char()
        return False
    if current_char == '*':
        read_next_char()
        if is_invalid_char(current_char):
            report_invalid_input()
        elif current_char == '/':
            report_unmatched_comment()
        else:
            unread_last_char()
            add_symbol_token()

    elif current_char == '=':
        read_next_char()
        if is_invalid_char(current_char):
            report_invalid_input()
        elif current_char == '=':
            add_symbol_token()
        else:
            unread_last_char()
            add_symbol_token()

    else:
        add_symbol_token()

    return True


def extract_comment():
    read_next_char()
    if not current_char == '/':
        unread_last_char()
        return False
    read_next_char()
    if not current_char == '*':
        if not is_invalid_char(current_char):
            unread_last_char()
        report_invalid_input()
        return True
    last_char = None
    comment_start_line = line_number
    while last_char != '*' or current_char != '/':
        if len(read_buffer) > 10:
            disable_buffer_saving()
        if current_char == '':
            report_unclosed_comment(comment_start_line)
            enable_buffer_saving()
            return True
        last_char = current_char
        read_next_char()
    enable_buffer_saving()
    return True


def extract_whitespace():
    read_next_char()
    if not is_whitespace(current_char):
        unread_last_char()
        return False
    return True


def update_last_token():
    global last_token_type, last_token_lexem
    last_token_lexem = token_lexeme
    last_token_type = token_type
    return token_type, token_lexeme


# Token extraction entry


def get_next_token():
    global token_lexeme, token_type
    read_buffer.clear()
    read_next_char()
    if current_char == '':
        return '$', '$'
    if is_invalid_char(current_char):
        report_invalid_input()
        return True
    unread_last_char()
    token_type = ''
    token_lexeme = ''
    if extract_number(): return update_last_token()
    if extract_id_kw(): return update_last_token()
    if extract_symbol(): return update_last_token()
    if extract_whitespace() or extract_comment():
        return get_next_token()  # TODO this line can be problematic. we will change it if it breaks anything.
    print("UNREACHABLE PRINT STATEMENT")
    return True


# Saving results and reporting errors


def build_string_from_buffer():
    s = ''
    for c in read_buffer:
        s += c
    return s


def write_to_file(file, last_lineno, content, line_num=None):
    if SILENT_MODE:
        return
    if file is None or not file.writable():
        return
    if line_num is None:
        line_num = line_number
    if not last_lineno is None and last_lineno < line_num:
        if last_lineno > 0:
            file.write(NEW_LINE)
        file.write(str(line_num) + '.\t')
    file.write(content)


def write_token():
    global last_token_line_number
    write_to_file(TOKEN_FILE, last_token_line_number,
            '(' + token_type + ', ' + token_lexeme + ') ')
    last_token_line_number = line_number


def write_error_with_prompt(prompt: str, line_num=None):
    global last_error_line_number
    if line_num is None:
        line_num = line_number
    write_to_file(ERROR_FILE, last_error_line_number,
                  '(' + build_string_from_buffer() + ', ' + prompt + ') ', line_num)
    last_error_line_number = line_num


def report_invalid_number():
    write_error_with_prompt("Invalid number")


def report_invalid_input():
    write_error_with_prompt("Invalid input")


def report_unmatched_comment():
    write_error_with_prompt("Unmatched comment")


def report_unclosed_comment(command_start_line):
    global read_buffer, last_error_line_number
    if len(read_buffer) > 7:
        read_buffer = read_buffer[:7]
        read_buffer += ['.', '.', '.']
    write_error_with_prompt("Unclosed comment", command_start_line)


def add_number_token():
    global token_lexeme, token_type, first_empty_data
    token_lexeme = build_string_from_buffer()
    token_type = 'NUM'
    if declaration_mode == DeclarationMode.Name:
        if symbol_list[-1].id_type == IdentifierType.int_array:
            symbol_list[-1].array_length = int(token_lexeme)
            first_empty_data += 4 * (int(token_lexeme) - 1)
    write_token()


def add_id_kw_token():
    global token_lexeme, token_type, last_type_line_number, last_param_type
    token_lexeme = build_string_from_buffer()
    token_type = 'KEYWORD' if token_lexeme in KEYWORDS else 'ID'
    if declaration_mode == DeclarationMode.Name:    
        if token_lexeme == 'void':
            symbol_list[-1].id_type = IdentifierType.void
            last_type_line_number = line_number
        elif token_lexeme == 'int':
            symbol_list[-1].id_type = IdentifierType.int
            last_type_line_number = line_number
        elif not token_lexeme in KEYWORDS:
            symbol_list[-1].lexeme = token_lexeme
    elif declaration_mode == DeclarationMode.Parameter:
        if token_lexeme in ['int', 'void']:
            last_param_type = token_lexeme
        elif token_lexeme not in KEYWORDS:
            new_parameter = SymbolTableEntry()
            new_parameter.id_type = IdentifierType.int if last_param_type == 'int' else IdentifierType.void
            symbol_list[scope_stack[-1] - 1].parameter_list.append(new_parameter.id_type)
            last_type_line_number = line_number
            symbol_list[-1].lexeme = token_lexeme

    write_token()


def add_symbol_token():
    global token_lexeme, token_type
    token_lexeme = build_string_from_buffer()
    token_type = 'SYMBOL'
    if token_lexeme == '[' and \
            declaration_mode in [DeclarationMode.Name, DeclarationMode.Parameter]:
        if symbol_list[-1].id_type == IdentifierType.int:
            symbol_list[-1].id_type = IdentifierType.int_array
        if declaration_mode == DeclarationMode.Parameter:
            if symbol_list[scope_stack[-1] - 1].parameter_list[-1] == IdentifierType.int:
                symbol_list[scope_stack[-1] - 1].parameter_list[-1] = IdentifierType.int_array

    write_token()


def init_symbol_table():
    output_function = SymbolTableEntry()
    output_function.id_type = IdentifierType.void
    output_function.lexeme = 'output'
    output_function.is_function = True
    output_function.parameter_list.append(IdentifierType.int)


def get_current_line():
    return line_number


def get_last_token():
    return last_token_type, last_token_lexem


def symbol_table_lookup(lexeme: str):
    """
    Looks up the symbol table for an ID with lexeme
    equal to LEXEME. Returns its index if it is found, -1 otherwise
    Input

    Args:
        lexeme : The string which is to mach some entry's lexeme in symbol table.
    
    Returns:
        The index of entry in symbol table with that lexeme, or -1 if no such 
        entry exists.
    """

    for i in range(len(symbol_list)):
        if symbol_list[i].lexeme == lexeme:
            return i

    return -1


# Symbol table management
def set_declaration_mode(mode):
    global declaration_mode
    declaration_mode = mode


def start_declaration():
    set_declaration_mode(DeclarationMode.Name)
    new_entry = SymbolTableEntry()
    if last_token_lexem == 'int':
        new_entry.id_type = IdentifierType.int
    elif last_token_lexem == 'void':
        new_entry.id_type = IdentifierType.void
    else:
        raise Exception("Inappropriate type specification")
    

def start_params():
    set_declaration_mode(DeclarationMode.Parameter)
    symbol_list[-1].is_function = True
    scope_stack.append(len(symbol_list))


def end_scope():
    global symbol_list
    symbol_list = symbol_list[:scope_stack[-1]]
