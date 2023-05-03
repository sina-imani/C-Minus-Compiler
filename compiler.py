# IAWT

from scanner import scanner
from parser import parser

# Setting files
try:
    scanner.INPUT_FILE = open('input.txt')
    parser.TREE_FILE = open('parse_tree.txt', 'w')
    parser.SYNTAX_ERROR_FILE = open('syntax_errors.txt', 'w')

    scanner.init_symbol_table()
except (FileNotFoundError, PermissionError):
    print('Error while configuring files: No input.txt or insufficient process access')
    exit(-1)

parser.run()

try:
    if parser.CORRECT_PROGRAM:
        parser.SYNTAX_ERROR_FILE.write('There is no syntax error.')

    scanner.INPUT_FILE.close()
    parser.TREE_FILE.close()
    parser.SYNTAX_ERROR_FILE.close()

except IOError:
    print('Error while closing files.')
    exit(-1)
