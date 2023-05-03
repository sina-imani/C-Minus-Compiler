# IAWT

from scanner import scanner
from parser import parser

# Setting files
try:
    scanner.INPUT_FILE = open('input.txt')
    scanner.ERROR_FILE = open('lexical_errors.txt', 'w')
    scanner.TOKEN_FILE = open('tokens.txt', 'w')
    scanner.SYMBOL_FILE = open('symbol_table.txt', 'w')
    parser.TREE_FILE = open('parse_tree.txt', 'w')
    parser.SYNTAX_ERROR_FILE = open('syntax_error.txt', 'w')

    scanner.init_symbol_table()
except (FileNotFoundError, PermissionError):
    print('Error while configuring files: No input.txt or insufficient process access')
    exit(-1)

parser.run()

try:
    if scanner.last_error_line_number == 0:
        scanner.ERROR_FILE.write('There is no lexical error.')
    else:
        scanner.ERROR_FILE.write(scanner.NEW_LINE)
    scanner.TOKEN_FILE.write(scanner.NEW_LINE)

    scanner.INPUT_FILE.close()
    scanner.ERROR_FILE.close()
    scanner.TOKEN_FILE.close()
    scanner.SYMBOL_FILE.close()
except IOError:
    print('Error while closing files.')
    exit(-1)
