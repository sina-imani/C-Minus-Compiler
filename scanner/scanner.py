# IAWT

from typing import *

## GLOBAL VARIABLES

INPUT_FILE = None
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
current_char = None
ready_char = None
line_number = 0


## FUNCTIONS

# Characters: reading and examining

def read_next_char():
    global current_char, ready_char, line_number
    if ready_char is None:
        current_char = INPUT_FILE.read(1)
    else:
        current_char = ready_char
        ready_char = None
    if current_char == '\n':
        line_number += 1

def unread_last_char():
    if current_char == '\n':
        line_number -= 1
    ready_char = current_char
    current_char = None


def is_numeric(chr):
    return '0' <= chr <= '9'

def is_letter(chr):
    return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z'

def is_white_slash(chr):
    return chr in WHITE_SPACES or chr == '/'

def is_invalid_char(chr):
    if is_numeric(chr) or is_letter(chr):
        return False
    elif chr in SYMBOLS or is_white_slash(chr):
        return False
    return True


# Token extraction

def extract_number():
    chr = read_next_char()
    if not is_numeric(chr):
        unread_last_char()
        return None
    buff = [chr]
    while is_numeric(chr = read_next_char()):
        buff.append(chr)
    
    if is_white_slash(chr):
        unread_last_char()
        return buff
    buff.append(chr)
    # TODO: invalid number
    return



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