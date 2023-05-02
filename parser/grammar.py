from typing import List, Set, Tuple, Dict

START = 'Program'

first: Dict[str, Set[str]] = {}
follow: Dict[str, Set[str]] = {}
productions: Dict[str, List[List[str]]] | None = None

first = {
    'Program': {';', '[', '(', 'int', 'void', ''},
    'Declaration_list': {';', '[', '(', 'int', 'void', ''},
    'Declaration': {';', '[', '(', 'int', 'void'},
    'Declaration_initial': {'int', 'void'},
    'Declaration_prime': {';', '[', '('},
    'Var_declaration_prime': {';', '['},
    'Fun_declaration_prime': {'('},
    'Type_specifier': {'int', 'void'},
    'Params': {'int', 'void'},
    'Param_list': {',', ''},
    'Param': {'int', 'void'},
    'Param_prime': {'[', ''},
    'Compound_stmt': {'{'},
    'Statement_list': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', ''},
    'Statement': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'},
    'Expression_stmt': {'ID', ';', 'NUM', '(', 'break'},
    'Selection_stmt': {'if'},
    'Iteration_stmt': {'repeat'},
    'Return_stmt': {'return'},
    'Return_stmt_prime': {'ID', ';', 'NUM', '('},
    'Expression': {'ID', 'NUM', '('},
    'B': {'[', '(', '=', '<', '==', '+', '-', '*', ''},
    'H': {'=', '<', '==', '+', '-', '*', ''},
    'Simple_expression_zegond': {'NUM', '('},
    'Simple_expression_prime': {'(', '<', '==', '+', '-', '*', ''},
    'C': {'<', '==', ''},
    'Relop': {'<', '=='},
    'Additive_expression': {'ID', 'NUM', '('},
    'Additive_expression_prime': {'(', '+', '-', '*', ''},
    'Additive_expression_zegond': {'NUM', '('},
    'D': {'+', '-', ''},
    'Addop': {'+', '-'},
    'Term': {'ID', 'NUM', '('},
    'Term_prime': {'(', '*', ''},
    'Term_zegond': {'NUM', '('},
    'G': {'*', ''},
    'Factor': {'ID', 'NUM', '('},
    'Var_call_prime': {'[', '(', ''},
    'Var_prime': {'[', ''},
    'Factor_prime': {'(', ''},
    'Factor_zegond': {'NUM', '('},
    'Args': {'ID', 'NUM', '(', ''},
    'Arg_list': {'ID', 'NUM', '('},
    'Arg_list_prime': {',', ''}
}


follow = {
    'Program': {'$'},
    'Declaration_list': {'$', 'repeat', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Declaration': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Declaration_initial': {'$', 'repeat', 'int', 'if', '(', 'ID', ',', '[', 'void', '{', 'NUM', '}', 'break', 'return', ')', ';'},
    'Declaration_prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Var_declaration_prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Fun_declaration_prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Type_specifier': {'ID'},
    'Params': {')'},
    'Param_list': {')'},
    'Param': {',', ')'},
    'Param_prime': {',', ')'},
    'Compound_stmt': {'$', 'repeat', 'int', 'else', 'until', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Statement_list': {'}'},
    'Statement': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Expression_stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Selection_stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Iteration_stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Return_stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Return_stmt_prime': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Expression': {',', ')', ']', ';'},
    'B': {',', ')', ']', ';'},
    'H': {',', ')', ']', ';'},
    'Simple_expression_zegond': {',', ')', ']', ';'},
    'Simple_expression_prime': {',', ')', ']', ';'},
    'C': {',', ')', ']', ';'},
    'Relop': {'(', 'NUM', 'ID'},
    'Additive_expression': {',', ')', ']', ';'},
    'Additive_expression_prime': {'<', ']', ',', '==', ')', ';'},
    'Additive_expression_zegond': {'<', ']', ',', '==', ')', ';'},
    'D': {'<', ']', ',', '==', ')', ';'},
    'Addop': {'(', 'NUM', 'ID'},
    'Term': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Term_prime': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Term_zegond': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'G': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Factor': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Var_call_prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Var_prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Factor_prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Factor_zegond': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Args': {')'},
    'Arg_list': {')'},
    'Arg_list_prime': {')'}
}

grammar: List[str] = ["Program -> Declaration-list $",
                      "Declaration-list -> Declaration Declaration-list | EPSILON",
                      "Declaration -> Declaration-initial Declaration-prime",
                      "Declaration-initial -> Type-specifier ID",
                      "Declaration-prime -> Fun-declaration-prime | Var-declaration-prime",
                      "Var-declaration-prime -> ; | [ NUM ] ;",
                      "Fun-declaration-prime -> ( Params ) Compound-stmt",
                      "Type-specifier -> int | void",
                      "Params -> int ID Param-prime Param-list | void",
                      "Param-list -> , Param Param-list | EPSILON",
                      "Param -> Declaration-initial Param-prime",
                      "Param-prime -> [ ] | EPSILON",
                      "Compound-stmt -> { Declaration-list Statement-list }",
                      "Statement-list -> Statement Statement-list | EPSILON",
                      "Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt",
                      "Expression-stmt -> Expression ; | break ; | ;",
                      "Selection-stmt -> if ( Expression ) Statement else Statement",
                      "Iteration-stmt -> repeat Statement until ( Expression )",
                      "Return-stmt -> return Return-stmt-prime",
                      "Return-stmt-prime -> ; | Expression ;",
                      "Expression -> Simple-expression-zegond | ID B",
                      "B -> = Expression | [ Expression ] H | Simple-expression-prime",
                      "H -> = Expression | G D C",
                      "Simple-expression-zegond -> Additive-expression-zegond C",
                      "Simple-expression-prime -> Additive-expression-prime C",
                      "C -> Relop Additive-expression | EPSILON",
                      "Relop -> < | ==",
                      "Additive-expression -> Term D",
                      "Additive-expression-prime -> Term-prime D",
                      "Additive-expression-zegond -> Term-zegond D",
                      "D -> Addop Term D | EPSILON", "Addop -> + | -",
                      "Term -> Factor G", "Term-prime -> Factor-prime G",
                      "Term-zegond -> Factor-zegond G",
                      "G -> * Factor G | EPSILON",
                      "Factor -> ( Expression ) | ID Var-call-prime | NUM",
                      "Var-call-prime -> ( Args ) | Var-prime",
                      "Var-prime -> [ Expression ] | EPSILON",
                      "Factor-prime -> ( Args ) | EPSILON",
                      "Factor-zegond -> ( Expression ) | NUM", "Args -> Arg-list | EPSILON",
                      "Arg-list -> Expression Arg-list-prime",
                      "Arg-list-prime -> , Expression Arg-list-prime | EPSILON"]

terminals: Set[str] = {
    ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==',
    'break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void', 'NUM', 'ID',
    '$'
}


def is_terminal(edge: str) -> bool:
    """
    check if the edge is a terminal or non-terminal

    :param edge: the action which change the current state
    :return: true if the edge is a terminal and false if the edge is a non-terminal
    """
    return edge in terminals


def get_productions(non_terminal: str) -> str:
    for p in grammar:
        if p.split()[0] == non_terminal:
            return p


def find_first(symbol: str, productions: Dict[str, List[List[str]]]) -> Set[str]:
    """
    Find first set of str symbol give the production rules
    :param symbol:
    :param productions:
    :return:
    """

    if symbol in first.keys():
        return first[symbol]

    first_set = set()

    symbol_productions = productions[symbol]

    for p in symbol_productions:

        if is_terminal(p[0]):
            first_set.add(p[0])

        elif p[0] == 'EPSILON':
            first_set.add('EPSILON')

        else:
            for i, s in enumerate(p):
                first_s = find_first(s, productions)
                if 'EPSILON' not in first_s:
                    first_set |= first_s
                    break
                else:
                    first_set.update({elem for elem in first_s if elem != 'EPSILON'})
                    if i == len(p) - 1:
                        first_set.add('EPSILON')

    first[symbol] = first_set
    return first_set


def find_follow(s, productions):
    follow_set = set()

    if s == START:
        follow_set.add('$')

    for i in productions:
        for j in range(len(productions[i])):
            if s in productions[i][j]:
                idx = productions[i][j].index(s)

                if idx == len(productions[i][j]) - 1:
                    if productions[i][j][idx] == i:
                        break
                    else:
                        f = find_follow(i, productions)
                        for x in f:
                            follow_set.add(x)
                else:
                    while idx != len(productions[i][j]) - 1:
                        idx += 1
                        if not productions[i][j][idx].isupper():
                            follow_set.add(productions[i][j][idx])
                            break
                        else:
                            f = find_follow(productions[i][j][idx], productions)

                            if 'EPSILON' not in f:
                                for x in f:
                                    follow_set.add(x)
                                break
                            elif 'EPSILON' in f and idx != len(productions[i][j]) - 1:
                                f.remove('EPSILON')
                                for k in f:
                                    follow_set.add(k)

                            elif 'EPSILON' in f and idx == len(productions[i][j]) - 1:
                                f.remove('EPSILON')
                                for k in f:
                                    follow_set.add(k)

                                f = find_follow(i, productions)
                                for x in f:
                                    follow_set.add(x)
    follow[s] = follow_set
    return follow_set


def print_first():
    for key, value in enumerate(first):
        print(value, first[value])


def parse_production(production: str) -> List[List[str]]:
    production_list: List[List[str]] = []
    productions_nt = production.split(' | ')
    for prod in productions_nt:
        production_list.append(prod.split())

    return production_list


def get_structured_productions() -> Dict[str, List[List[str]]]:
    if productions is None:
        productions_cfg = {}
        for production in grammar:
            lhs, rhs = production.split(' -> ')
            productions_cfg[lhs] = parse_production(rhs)
        return productions_cfg

    else:
        return productions
