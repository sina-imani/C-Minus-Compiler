import itertools
from parser.grammar import pre_process, grammar
import scanner.scanner as scanner
from anytree import Node, RenderTree
from typing import List, Tuple, Dict

stack = []  # define stack to track the states in sub calls
state_diagram_dict: Dict['str', 'State'] = {}

#
# def create_initial_diagram():
#     start, initial_productions = get_initial_productions()
#     create_diagram(non_terminal=start,
#                    production_rules=initial_productions
#                    )
#     return state_diagram_dict[start]


def create_diagram(non_terminal: str, production_rules: List[List[str]]):
    start_state = State()
    for production in production_rules:
        prev: 'State' = start_state
        for edge in production:
            next_state = State()
            prev.add_next_state(edge, next_state)
            prev = next_state

        state_diagram_dict[non_terminal] = start_state


class State:
    total_state = itertools.count()

    def __init__(self):
        self.id_s = next(State.total_state)
        self.next_states = []

    def add_next_state(self, edge: str, next_state: 'State') -> None:
        self.next_states.append((edge, next_state))


def run():
    pre_process(grammar)

    # current_state: 'State' = create_initial_diagram()

    while True:
        result = scanner.get_next_token()
        print(result)
        if result[0] == '$':
            break
