# IAWT


## GLOBAL VARIABLES

INPUT_FILE = None
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
ready_char = None
line_number = 0


## FUNCTIONS

def read_next_char():
    if not ready_char is None:
        ready_char = None
        return ready_char
    return INPUT_FILE.read(1)


def is_invalid_char(chr):
    if '0' <= chr <= '9' or 'a' <= chr <= 'z' or 'A' <= chr <= 'Z':
        return False
    elif chr in SYMBOLS or chr in WHITE_SPACES:
        return False
    elif chr == '/':
        return False
    return True




## MAIN
try:
    INPUT_FILE = open('input.txt', 'r')
except:
    print('No input file found!')





"""
read_next_char()
get_next_token ()

extract_number / id / symbol / comment / white_space ()

is_keyword ()
is_invalid_char ()

INPUT_FILE
ready_char
line_number
"""