import itertools
from grammar import get_structured_productions, START, is_terminal, first, follow

import scanner.scanner as scanner
from anytree import Node, RenderTree
from typing import List, Tuple, Dict, Set

TREE_FILE = None
SYNTAX_ERROR_FILE = None

stack: List[Tuple[str, 'State', 'Node']] = []  # define stack to track the states in sub calls. #0 edge #1 state
current_position: Tuple[str, 'State']  # the current state of parsing diagram
state_diagram_dict: Dict[str, 'State'] = {}  # the diagram of each non-terminal

CORRECT_PROGRAM = True


class State:
    total_state = itertools.count()

    def __init__(self):
        self.id_s = next(State.total_state)
        self.next_states = []

    def add_next_state(self, edge: str, next_state: 'State') -> None:
        self.next_states.append((edge, next_state))


#
def create_initial_diagram() -> 'State':
    structured_productions: Dict[str, List[List[str]]] = get_structured_productions()
    initial_state_productions: List[List[str]] = structured_productions[START]
    create_diagram(non_terminal=START,
                   production_rules=initial_state_productions
                   )

    return state_diagram_dict[START]


def create_diagram(non_terminal: str, production_rules: List[List[str]]):
    start_state = State()
    for production in production_rules:
        prev: 'State' = start_state
        for edge in production:
            next_state = State()
            prev.add_next_state(edge, next_state)
            prev = next_state

        state_diagram_dict[non_terminal] = start_state


def add_node(edge: str, parent=None):
    if parent is not None:
        n = Node(edge, parent)
    else:
        n = Node(edge)

    return n


def jump_forward(n_state: 'State', edge: 'str'):
    global current_position

    while not n_state.next_states:
        edge, n_state, _ = stack.pop()

    current_position = (edge, n_state)


def move_forward(n_state: 'State', token: Tuple[str, str]):
    global current_position

    # get last element of stack
    parent: 'Node' = stack[-1][2]

    if token[0] == '$':
        format_t = '$'
    elif type(token) == tuple:
        format_t = f"({token[0]}, {token[1]})"
    else:
        format_t = token

    add_node(format_t, parent=parent)

    # check if n_state is diagram-terminal
    p_state = n_state
    p_edge = token[0]
    while not p_state.next_states:
        p_edge, p_state, _ = stack.pop()

    current_position = (p_edge, p_state)


def move_in(un_state: 'State', edge: str):
    global current_position

    parent: 'Node' = stack[-1][2]
    n = add_node(edge, parent=parent)

    stack.append((edge, un_state, n))

    if edge not in state_diagram_dict.keys():
        structured_productions: Dict[str, List[List[str]]] = get_structured_productions()
        production_rules: List[List[str]] = structured_productions[edge]
        create_diagram(edge, production_rules)

    current_position = (edge, state_diagram_dict[edge])


def compute_sentence_first_set(in_edge: 'str', state: 'State') -> Set[str]:
    first_set = set()
    # get first of the symbol

    first_edge = first[in_edge]
    if 'epsilon' in first_edge and state.next_states:
        first_set.update({elem for elem in first_edge if elem != 'epsilon'})

        for e, s in state.next_states:
            if e == '$':
                first_set.add('epsilon')
            elif not is_terminal(e):
                first_set.update(compute_sentence_first_set(e, s))
            else:
                first_set.add(e)

        return first_set

    else:
        return first_edge


def token_key(token: Tuple[str, str]):
    if token[0] in ('ID', 'NUM'):
        return token[0]
    else:
        return token[1]


def select_next_move(position: Tuple[str, 'State'], token):
    for e, s in position[1].next_states:
        # compute the first set
        if is_terminal(e):
            if e == token_key(token):
                move_forward(s, token)
                return None

        elif e != 'epsilon':
            # compute the First of the rhs production
            if token_key(token) in compute_sentence_first_set(e, s):
                move_in(s, e)
                return token

    if token_key(token) in follow[stack[-1][0]]:
        for e, s in position[1].next_states:
            if e == 'epsilon':
                move_forward(s, e)
                return token
            elif not is_terminal(e):
                if 'epsilon' in first[e]:
                    move_in(s, e)
                    return token

    if len(position[1].next_states) > 1:
        RuntimeError('impossible')

    next_edge, next_state = position[1].next_states[0]

    if token_key(token) == '$':
        print_eof_error()
        stack.clear()
        return None

    if is_terminal(next_edge):
        print_missing_error(next_edge)
        jump_forward(next_state, next_edge)
        return token

    else:
        if token_key(token) in follow[next_edge]:
            print_missing_error(next_edge)
            jump_forward(next_state, next_edge)
            return token
        else:
            print_illegal_error(token_key(token))
            return None


def print_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name), file=TREE_FILE)


def print_missing_error(missing_token: str):
    print(f'#{scanner.get_current_line()} : syntax error, missing {missing_token}', file=SYNTAX_ERROR_FILE)
    global CORRECT_PROGRAM
    CORRECT_PROGRAM = False


def print_illegal_error(illegal_token: str):
    print(f'#{scanner.get_current_line()} : syntax error, illegal {illegal_token}', file=SYNTAX_ERROR_FILE)
    global CORRECT_PROGRAM
    CORRECT_PROGRAM = False


def print_eof_error():
    print(f'#{scanner.get_current_line() + 1} : syntax error, Unexpected EOF', file=SYNTAX_ERROR_FILE)
    global CORRECT_PROGRAM
    CORRECT_PROGRAM = False


def run():
    global current_position
    start_state: 'State' = create_initial_diagram()
    current_position = (START, start_state)
    root = add_node(START)

    stack.append((START, start_state, root))
    token = None

    while len(stack) != 0:
        if token is None:
            token = scanner.get_next_token()
            token = select_next_move(current_position, token)
        else:
            token = select_next_move(current_position, token)

    print_tree(root)
