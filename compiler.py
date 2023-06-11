# IAWT

import code_parser
import scanner
import code_maker

# Setting files
try:
    scanner.INPUT_FILE = open('input.txt', 'r')
    code_maker.SEM_ERROR_FILE = open('semantic_errors.txt', 'w')
    scanner.init_symbol_table()
    code_maker_file = open('output.txt', 'w')

except (FileNotFoundError, PermissionError):
    print('Error while configuring files: No input.txt or insufficient process access')
    exit(-1)

code_parser.run()

try:
    scanner.INPUT_FILE.close()
    for i in range(len(code_maker.PB) - 1):
        code_maker_file.write(code_maker.PB[i] + '\n')
    if len(code_maker.PB) > 0:
        code_maker_file.write(code_maker.PB[-1])
    code_maker_file.close()
    if code_maker.semantic_correctness:
        code_maker.SEM_ERROR_FILE.write('The input program is semantically correct.\n')
    code_maker.SEM_ERROR_FILE.close()

except IOError:
    print('Error while closing files.')
    exit(-1)
