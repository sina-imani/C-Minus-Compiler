# IAWT



## GLOBAL VARIABLES


SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
INPUT_FILE = None
ERROR_FILE = None
TOKEN_FILE = None
SYMBOL_FILE = None


symbol_list = []
save_in_buffer : bool = True
current_char : str | None = None
ready_char : str | None = None
read_buffer : list = []
line_number : int = 1
token_lexeme : str
token_type : str
last_token_line_number : int = 0
last_error_line_number : int = 0


## FUNCTIONS


# Characters: reading


def enable_buffer_saving ():
    save_in_buffer = True


def disable_buffer_saving ():
    save_in_buffer = False


def read_next_char ():
    global current_char, ready_char, line_number
    if INPUT_FILE is None:
        return
    if ready_char is None:
        current_char = INPUT_FILE.read (1)
    else:
        current_char = ready_char
        ready_char = None
    if current_char == '\n':
        line_number += 1
    if save_in_buffer and current_char != '':
        read_buffer.append (current_char)


def unread_last_char ():
    global current_char, line_number, ready_char
    if current_char == '\n':
        line_number -= 1
    ready_char = current_char
    current_char = None
    if read_buffer and save_in_buffer:
        del read_buffer[-1]


# Characters: examination


def is_numeric (chr):
    return '0' <= chr <= '9'


def is_letter (chr):
    return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z'


def is_numeric_letter (chr):
    return is_letter (chr) or is_numeric (chr)


def is_whitespace (chr):
    return chr in WHITE_SPACES


def is_white_slash (chr):
    return chr in WHITE_SPACES or chr == '/'


def is_symbol (chr):
    return chr in SYMBOLS


def is_invalid_char (chr):
    if chr == '':
        return False
    if is_numeric (chr) or is_letter (chr):
        return False
    elif chr in SYMBOLS or is_white_slash (chr):
        return False
    return True


# Token extraction


def extract_number ():
    read_next_char ()
    if not is_numeric (current_char):
        unread_last_char ()
        return
    read_next_char ()
    while is_numeric (current_char):
        read_next_char ()
    
    if is_invalid_char (current_char) or is_letter (current_char):
        report_invalid_number ()
    else:
        unread_last_char ()
        add_number_token ()


def extract_id_kw ():
    read_next_char ()
    if not is_letter (current_char):
        unread_last_char ()
        return
    read_next_char ()
    while (is_numeric_letter (current_char)):
        read_next_char ()
    
    if is_invalid_char (current_char):
        report_invalid_input ()
    else:
        unread_last_char ()
        add_id_kw_token ()


def extract_symbol ():
    read_next_char ()
    if not is_symbol (current_char):
        unread_last_char ()
        return
    if current_char == '*':
        read_next_char ()
        if is_invalid_char (current_char):
            report_invalid_input ()
        elif current_char == '/':
            # TODO : report lexical error: unmatched comment
            pass
        else:
            unread_last_char ()
            add_symbol_token ()

    elif current_char == '=':
        read_next_char ()
        if is_invalid_char (current_char):
            report_invalid_input ()
        elif current_char == '=':
            add_symbol_token ()
        else:
            unread_last_char ()
            add_symbol_token ()
    
    else:
        add_symbol_token ()


def extract_comment ():
    read_next_char ()
    if not current_char == '/':
        unread_last_char ()
        return
    read_next_char ()
    if not current_char == '*':
        unread_last_char ()
        report_invalid_input ()
        return
    last_char = None
    while last_char != '*' or current_char != '/':
        read_next_char ()
        if len (read_buffer) > 10:
            disable_buffer_saving ()
        if current_char == '':
            # TODO : report lexical error : unclosed comment
            enable_buffer_saving ()
            return
        last_char = current_char
    enable_buffer_saving ()


def extract_whitespace ():
    disable_buffer_saving ()
    read_next_char ()
    if not is_whitespace (current_char):
        unread_last_char ()
    enable_buffer_saving ()


# Token extraction entry


def get_next_token ():
    read_buffer.clear ()
    read_next_char ()
    if current_char == '':
        return None
    if is_invalid_char (current_char):
        report_invalid_input ()
        return None
    extract_number ()
    extract_id_kw ()
    extract_symbol ()
    extract_whitespace ()
    extract_comment ()
    return (token_type, token_lexeme)


# Saving results and reporting errors


def build_string_from_buffer ():
    s = ''
    for c in read_buffer:
        s += c
    return s


def write_to_file (file, last_lineno, content):
    if file is None or not file.writable ():
        return
    if not last_lineno is None and last_lineno < line_number:
        if line_number > 1:
            file.write ('\n')
        file.write (str (line_number) + '.\t')
    file.write(content)


def write_token ():
    global last_token_line_number
    write_to_file (TOKEN_FILE, last_token_line_number, \
        '(' + token_type + ', ' + token_lexeme + ') ')
    last_token_line_number = line_number


def write_error_with_prompt (prompt : str):
    global last_error_line_number
    write_to_file (ERROR_FILE, last_error_line_number, \
        '(' + build_string_from_buffer () + ', ' + prompt + ') ')
    last_error_line_number = line_number


def add_new_symbol (sym):
    symbol_list.append(sym)
    write_to_file (SYMBOL_FILE, None, str (len (symbol_list)) + '\t' + sym + '\n')


def report_invalid_number ():
    write_error_with_prompt ("Invalid number")


def report_invalid_input ():
    write_error_with_prompt ("Invalid input")



def add_number_token ():
    global token_lexeme, token_type
    token_lexeme = build_string_from_buffer ()
    token_type = 'NUM'
    write_token ()


def add_id_kw_token ():
    global token_lexeme, token_type
    token_lexeme = build_string_from_buffer ()
    token_type = 'KEYWORD' if token_lexeme in KEYWORDS else 'ID'
    if not token_lexeme in symbol_list:
        add_new_symbol (token_lexeme)
    write_token ()


def add_symbol_token ():
    global token_lexeme, token_type
    token_lexeme = build_string_from_buffer ()
    token_type = 'SYMBOL'
    write_token ()



## MAIN


for kw in KEYWORDS:
    add_new_symbol(kw)



"""
read_next_char ()
get_next_token ()

extract_number / id / symbol / comment / white_space ()

is_keyword ()
is_invalid_char ()

INPUT_FILE
ready_char
line_number
"""