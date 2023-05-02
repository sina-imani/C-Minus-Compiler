import itertools
from parser.grammar import get_structured_productions, START, is_terminal, first

import scanner.scanner as scanner
from anytree import Node, RenderTree
from typing import List, Tuple, Dict, Set

stack: List[Tuple[str, 'State']] = []  # define stack to track the states in sub calls. #0 edge #1 state
current_state: 'State'  # the current state of parsing diagram
state_diagram_dict: Dict['str', 'State'] = {}  # the diagram of each non-terminal


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


def move_forward(n_state: 'State', token: Tuple[str, str]):
    global current_state
    current_state = n_state

    # get last element of stack
    parent: str = stack[-1][0]
    Node(token, parent=parent)

    # check if n_state is diagram-terminal
    if not n_state.next_states:
        p_state = stack.pop()
        current_state = p_state


def move_in(un_state: 'State', edge: str):
    global current_state

    parent: str = stack[-1][0]
    Node(edge, parent=parent)

    stack.append((edge, un_state))

    if edge not in state_diagram_dict.keys():
        structured_productions: Dict[str, List[List[str]]] = get_structured_productions()
        production_rules: List[List[str]] = structured_productions[edge]
        create_diagram(edge, production_rules)

    current_state = state_diagram_dict[edge]


def compute_sentence_first_set(in_edge: 'str', state: 'State') -> Set[str]:
    first_set = set()
    # get first of the symbol

    first_edge = first[in_edge]
    if 'EPSILON' in first_edge and state.next_states:
        first_set.update({elem for elem in first_set if elem != 'EPSILON'})

        for e, s in state.next_states:
            first_set.update(compute_sentence_first_set(e, s))

    else:
        return first_edge


def select_next_move(state: 'State', token):
    # define flag to know if parser move froward or move in

    for e, s in state.next_states:
        # compute the first set
        if is_terminal(e):
            if e == token[0]:
                move_forward(s, token)
                return token

        else:
            # compute the First of the rhs production
            if token[0] in compute_sentence_first_set(s, e):
                move_in(s, e)
                return None


def run():
    global current_state
    start_state: 'State' = create_initial_diagram()
    current_state = start_state

    stack.append((START, start_state))
    Node(START)

    token = None

    while len(stack) != 0:
        if token is None:
            token = scanner.get_next_token()
            token = select_next_move(current_state, token)
        else:
            token = select_next_move(current_state, token)
