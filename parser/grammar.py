from typing import List, Set, Dict

START = 'Program'

productions: Dict[str, List[List[str]]] | None = None

first: Dict[str, Set[str]] = {
    'Program': {';', '[', '(', 'int', 'void', 'epsilon'},
    'Declaration-list': {';', '[', '(', 'int', 'void', 'epsilon'},
    'Declaration': {';', '[', '(', 'int', 'void'},
    'Declaration-initial': {'int', 'void'},
    'Declaration-prime': {';', '[', '('},
    'Var-declaration-prime': {';', '['},
    'Fun-declaration-prime': {'('},
    'Type-specifier': {'int', 'void'},
    'Params': {'int', 'void'},
    'Param-list': {',', 'epsilon'},
    'Param': {'int', 'void'},
    'Param-prime': {'[', 'epsilon'},
    'Compound-stmt': {'{'},
    'Statement-list': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'epsilon'},
    'Statement': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'},
    'Expression-stmt': {'ID', ';', 'NUM', '(', 'break'},
    'Selection-stmt': {'if'},
    'Iteration-stmt': {'repeat'},
    'Return-stmt': {'return'},
    'Return-stmt-prime': {'ID', ';', 'NUM', '('},
    'Expression': {'ID', 'NUM', '('},
    'B': {'[', '(', '=', '<', '==', '+', '-', '*', 'epsilon'},
    'H': {'=', '<', '==', '+', '-', '*', 'epsilon'},
    'Simple-expression-zegond': {'NUM', '('},
    'Simple-expression-prime': {'(', '<', '==', '+', '-', '*', 'epsilon'},
    'C': {'<', '==', 'epsilon'},
    'Relop': {'<', '=='},
    'Additive-expression': {'ID', 'NUM', '('},
    'Additive-expression-prime': {'(', '+', '-', '*', 'epsilon'},
    'Additive-expression-zegond': {'NUM', '('},
    'D': {'+', '-', 'epsilon'},
    'Addop': {'+', '-'},
    'Term': {'ID', 'NUM', '('},
    'Term-prime': {'(', '*', 'epsilon'},
    'Term-zegond': {'NUM', '('},
    'G': {'*', 'epsilon'},
    'Factor': {'ID', 'NUM', '('},
    'Var-call-prime': {'[', '(', 'epsilon'},
    'Var-prime': {'[', 'epsilon'},
    'Factor-prime': {'(', 'epsilon'},
    'Factor-zegond': {'NUM', '('},
    'Args': {'ID', 'NUM', '(', 'epsilon'},
    'Arg-list': {'ID', 'NUM', '('},
    'Arg-list-prime': {',', 'epsilon'}
}

follow: Dict[str, Set[str]] = {
    'Program': {'$'},
    'Declaration-list': {'$', 'repeat', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Declaration': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Declaration-initial': {'$', 'repeat', 'int', 'if', '(', 'ID', ',', '[', 'void', '{', 'NUM', '}', 'break', 'return',
                            ')', ';'},
    'Declaration-prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return', ';'},
    'Var-declaration-prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return',
                              ';'},
    'Fun-declaration-prime': {'$', 'repeat', 'int', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break', 'return',
                              ';'},
    'Type-specifier': {'ID'},
    'Params': {')'},
    'Param-list': {')'},
    'Param': {',', ')'},
    'Param-prime': {',', ')'},
    'Compound-stmt': {'$', 'repeat', 'int', 'else', 'until', 'if', '(', 'ID', '[', 'void', '{', 'NUM', '}', 'break',
                      'return', ';'},
    'Statement-list': {'}'},
    'Statement': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Expression-stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Selection-stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Iteration-stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Return-stmt': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Return-stmt-prime': {'repeat', 'else', 'until', 'if', '(', 'ID', '{', 'break', '}', 'NUM', 'return', ';'},
    'Expression': {',', ')', ']', ';'},
    'B': {',', ')', ']', ';'},
    'H': {',', ')', ']', ';'},
    'Simple-expression-zegond': {',', ')', ']', ';'},
    'Simple-expression-prime': {',', ')', ']', ';'},
    'C': {',', ')', ']', ';'},
    'Relop': {'(', 'NUM', 'ID'},
    'Additive-expression': {',', ')', ']', ';'},
    'Additive-expression-prime': {'<', ']', ',', '==', ')', ';'},
    'Additive-expression-zegond': {'<', ']', ',', '==', ')', ';'},
    'D': {'<', ']', ',', '==', ')', ';'},
    'Addop': {'(', 'NUM', 'ID'},
    'Term': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Term-prime': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Term-zegond': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'G': {'<', ']', '+', ',', '-', '==', ')', ';'},
    'Factor': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Var-call-prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Var-prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Factor-prime': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Factor-zegond': {'<', ']', '+', '*', ',', '-', '==', ')', ';'},
    'Args': {')'},
    'Arg-list': {')'},
    'Arg-list-prime': {')'}
}

grammar: List[str] = ["Program -> Declaration-list $",
                      "Declaration-list -> Declaration Declaration-list | epsilon",
                      "Declaration -> Declaration-initial Declaration-prime",
                      "Declaration-initial -> Type-specifier ID",
                      "Declaration-prime -> Fun-declaration-prime | Var-declaration-prime",
                      "Var-declaration-prime -> ; | [ NUM ] ;",
                      "Fun-declaration-prime -> ( Params ) Compound-stmt",
                      "Type-specifier -> int | void",
                      "Params -> int ID Param-prime Param-list | void",
                      "Param-list -> , Param Param-list | epsilon",
                      "Param -> Declaration-initial Param-prime",
                      "Param-prime -> [ ] | epsilon",
                      "Compound-stmt -> { Declaration-list Statement-list }",
                      "Statement-list -> Statement Statement-list | epsilon",
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
                      "C -> Relop Additive-expression | epsilon",
                      "Relop -> < | ==",
                      "Additive-expression -> Term D",
                      "Additive-expression-prime -> Term-prime D",
                      "Additive-expression-zegond -> Term-zegond D",
                      "D -> Addop Term D | epsilon", "Addop -> + | -",
                      "Term -> Factor G",
                      "Term-prime -> Factor-prime G",
                      "Term-zegond -> Factor-zegond G",
                      "G -> * Factor G | epsilon",
                      "Factor -> ( Expression ) | ID Var-call-prime | NUM",
                      "Var-call-prime -> ( Args ) | Var-prime",
                      "Var-prime -> [ Expression ] | epsilon",
                      "Factor-prime -> ( Args ) | epsilon",
                      "Factor-zegond -> ( Expression ) | NUM",
                      "Args -> Arg-list | epsilon",
                      "Arg-list -> Expression Arg-list-prime",
                      "Arg-list-prime -> , Expression Arg-list-prime | epsilon"]

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

        elif p[0] == 'epsilon':
            first_set.add('epsilon')

        else:
            for i, s in enumerate(p):
                first_s = find_first(s, productions)
                if 'epsilon' not in first_s:
                    first_set |= first_s
                    break
                else:
                    first_set.update({elem for elem in first_s if elem != 'epsilon'})
                    if i == len(p) - 1:
                        first_set.add('epsilon')

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

                            if 'epsilon' not in f:
                                for x in f:
                                    follow_set.add(x)
                                break
                            elif 'epsilon' in f and idx != len(productions[i][j]) - 1:
                                f.remove('epsilon')
                                for k in f:
                                    follow_set.add(k)

                            elif 'epsilon' in f and idx == len(productions[i][j]) - 1:
                                f.remove('epsilon')
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
    global productions
    if productions is None:
        productions = {}
        for production in grammar:
            lhs, rhs = production.split(' -> ')
            productions[lhs] = parse_production(rhs)

        return productions

    else:
        return productions
