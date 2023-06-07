# IAWT

import parser
import scanner
import code_maker

# Setting files
try:
    scanner.INPUT_FILE = open('input.txt')
    scanner.init_symbol_table()
    code_maker_file = open('output.txt')

except (FileNotFoundError, PermissionError):
    print('Error while configuring files: No input.txt or insufficient process access')
    exit(-1)

parser.run()

try:
    if parser.SYNTAX_CORRECT_PROGRAM:
        parser.SYNTAX_ERROR_FILE.write('There is no syntax error.')

    scanner.INPUT_FILE.close()
    parser.TREE_FILE.close()
    parser.SYNTAX_ERROR_FILE.close()
    for i in range(len(code_maker.PB) - 1):
        code_maker_file.write(code_maker.PB[i] + '\n')
    if len(code_maker.PB) > 0:
        code_maker_file.write(code_maker.PB[-1])
    code_maker_file.close()

except IOError:
    print('Error while closing files.')
    exit(-1)
