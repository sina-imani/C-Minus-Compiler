# IAWT

import code_parser
import scanner
import code_maker

# Setting files
try:
    scanner.INPUT_FILE = open('input.txt', 'r')
    code_maker.SEM_ERROR_FILE = open('semantic_errors.txt', 'w')
    code_parser.TREE_FILE = open('tree_file.txt', 'w')
    inter_code_file = open('output.txt', 'w')
    scanner.init_symbol_table()

except (FileNotFoundError, PermissionError):
    print('Error while configuring files: No input.txt.txt or insufficient process access')
    exit(-1)

code_parser.run()

try:
    scanner.INPUT_FILE.close()
    if code_maker.semantic_correctness:
        code_maker.SEM_ERROR_FILE.write('The input.txt program is semantically correct.\n')
        for i in range(len(code_maker.PB) - 1):
            inter_code_file.write(code_maker.PB[i] + '\n')
        if len(code_maker.PB) > 0:
            inter_code_file.write(code_maker.PB[-1])
    else:
        inter_code_file.write('The output code has not been generated.')
    inter_code_file.close()
    code_maker.SEM_ERROR_FILE.close()

except IOError:
    print('Error while closing files.')
    exit(-1)
