# IAWT

from typing import *

## GLOBAL VARIABLES

INPUT_FILE = None
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
current_char = None
ready_char = None
read_buffer = []
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
    read_buffer.append(current_char)

def unread_last_char():
    global current_char, line_number, ready_char
    if current_char == '\n':
        line_number -= 1
    ready_char = current_char
    current_char = None
    if read_buffer:
        del read_buffer[-1]

def is_numeric(chr):
    return '0' <= chr <= '9'

def is_letter(chr):
    return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z'

def is_numeric_letter(chr):
    return is_letter(chr) or is_numeric(letter)

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
    read_next_char()
    if not is_numeric(current_char):
        unread_last_char()
        return
    read_next_char()
    while is_numeric(current_char):
        read_next_char()
    
    if is_white_slash(current_char) or current_char == '':
        unread_last_char()
        # TODO: add number token to tokens.txt

    else:
        pass
        # TODO: report lexical error: invalid number
    return

def extract_id():
    read_next_char()
    if not is_letter(current_char):
        unread_last_char()
        return
    read_next_char()
    while (is_numeric_letter(current_char)):
        read_next_char()
    if is_white_slash(current_char) or current_char == '':
        unread_last_char()
        # TODO : add id to tokens.txt and symbols.txt   
    
    else:
        pass
        # TODO : report lexical error : invalid input

    



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