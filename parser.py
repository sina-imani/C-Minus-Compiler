import itertools
from typing import List, Tuple, Dict, Set

from anytree import Node, RenderTree

import scanner as scanner
from grammar import get_structured_productions, START, is_terminal, first, follow

TREE_FILE = None  # file which the tree is written to
SYNTAX_ERROR_FILE = None  # file which the syntax errors are written to

stack: List[Tuple[str, 'State', 'Node']] = []  # define stack to track the states in sub calls. #0 edge #1 state
current_position: Tuple[str, 'State']  # the current state of parsing diagram
state_diagram_dict: Dict[str, 'State'] = {}  # the diagram of each non-terminal

SYNTAX_CORRECT_PROGRAM = True  # if no error occurs, program has no syntax errors


class State:
    total_state = itertools.count()

    def __init__(self):
        self.id_s = next(State.total_state)
        self.next_states = []

    def add_next_state(self, edge: str, next_state: 'State') -> None:
        self.next_states.append((edge, next_state))


#
def create_initial_diagram() -> 'State':
    """
    This function creates a state diagram for the initial state using the production rules defined in the grammar.
    It returns the state diagram for the 'START' non-terminal symbol.

    Returns:
        A 'State' object representing the state diagram for the 'START' non-terminal symbol.
    """

    # Retrieve the structured production rules dictionary
    structured_productions: Dict[str, List[List[str]]] = get_structured_productions()

    # Retrieve the initial state production rules
    initial_state_productions: List[List[str]] = structured_productions[START]

    # Create the state diagram for the 'START' non-terminal symbol
    create_diagram(non_terminal=START,
                   production_rules=initial_state_productions
                   )
    # Return the state diagram for the 'START' non-terminal symbol
    return state_diagram_dict[START]


def create_diagram(non_terminal: str, production_rules: List[List[str]]) -> None:
    """
    This function creates a state diagram for a given non-terminal symbol using the provided production rules.
    The resulting state diagram is stored in the 'state_diagram_dict' dictionary with the non-terminal symbol
    as the key.

    Args:
        non_terminal: A string representing the non-terminal symbol for which the state diagram is being created.
        production_rules: A list of lists of strings representing the production rules for the non-terminal symbol.
    """
    # Create the start state for the state diagram
    start_state = State()

    # Iterate over each production rule for the non-terminal symbol
    for production in production_rules:
        prev: 'State' = start_state
        # Iterate over each edge in the production rule
        for edge in production:
            # Create a new state for the next edge in the production rule
            next_state = State()
            # Add a transition from the previous state to the next state using the current edge
            prev.add_next_state(edge, next_state)
            # Update the previous state to be the current state
            prev = next_state

    # Store the resulting state diagram in the 'state_diagram_dict' dictionary
    state_diagram_dict[non_terminal] = start_state


def add_node(symbol: str, parent: 'Node' = None) -> Node: # type: ignore
    """
    This function creates a new node with the given symbol and parent node (if provided).
    It returns the newly created node.

    Args:
        symbol: A string representing the symbol for the new node.
        parent: An optional 'Node' object representing the parent node of the new node.

    Returns:
        A 'Node' object representing the newly created node.
    """
    if parent is not None:
        n = Node(symbol, parent=parent)
    else:
        n = Node(symbol)

    return n


def jump_forward(n_state: 'State', edge: 'str') -> None:
    """
    This function takes a current state and an edge as arguments and jumps forward in the state machine
    until a state with one or more next states is reached. It also updates the global variable 'current_position'
    with the new state and edge.

    Args:
        n_state: A 'State' object representing the current state of the state machine.
        edge: A string representing the current edge being processed.

    Returns:
        None.
    """
    global current_position, stack

    # while the current state has no next states, pop the last state from the stack
    while not n_state.next_states:
        edge, n_state, _ = stack.pop()

    # update the global variable 'current_position' with the new state and edge
    current_position = (edge, n_state)


def move_forward(n_state: 'State', token: Tuple[str, str]):
    """
    This function moves the current position forward in the state diagram based on the given token.
    It adds a new node to the state diagram with the given token label and parent node.
    It also updates the current position to the next non-terminal state in the state diagram.

    Args:
        n_state: A 'State' object representing the current state in the state diagram.
        token: A tuple representing the current token being processed, with the first element being the token label
               and the second element being the token value (if applicable).
    """
    global current_position

    # Get the parent node for the new node
    parent: 'Node' = stack[-1][2]

    # Format the token label for display purposes
    if token[0] == '$':
        format_t = '$'
    elif type(token) == tuple:
        format_t = f"({token[0]}, {token[1]})"
    else:
        format_t = token

    # Add a new node to the state diagram with the given token label and parent node
    add_node(format_t, parent=parent)

    # Check if the current state is a diagram-terminal
    p_state = n_state
    p_edge = token[0]
    while not p_state.next_states:
        # Pop the last element from the stack
        p_edge, p_state, _ = stack.pop()

    # Update the current position to the next non-terminal state in the state diagram
    current_position = (p_edge, p_state)


def move_in(un_state: 'State', edge: str):
    """
    This function moves the current position into a new non-terminal state in the state diagram based on the given edge.
    It adds a new node to the state diagram with the given edge label and parent node.
    It also updates the current position to the new non-terminal state in the state diagram.

    Args:
        un_state: A 'State' object representing the current state in the state diagram.
        edge: A string representing the edge label for the new non-terminal state being entered.
    """
    global current_position

    # Get the parent node for the new node
    parent: 'Node' = stack[-1][2]
    # Add a new node to the state diagram with the given edge label and parent node
    n = add_node(edge, parent=parent)

    # Push the current position onto the stack
    stack.append((edge, un_state, n))

    # Check if the new non-terminal state has already been created in the state diagram
    if edge not in state_diagram_dict.keys():
        # If not, create the state diagram for the new non-terminal state
        structured_productions: Dict[str, List[List[str]]] = get_structured_productions()
        production_rules: List[List[str]] = structured_productions[edge]
        create_diagram(edge, production_rules)

    # Update the current position to the new non-terminal state in the state diagram
    current_position = (edge, state_diagram_dict[edge])


def compute_first_set(symbol: str, state: 'State') -> Set[str]:
    """
    This function computes the FIRST set for a given symbol in a given state in the state diagram.
    It returns a set of strings representing the FIRST set for the given symbol.

    Args:
        symbol: A string representing the symbol for which the FIRST set is being computed.
        state: A 'State' object representing the state in the state diagram for which the FIRST set is being computed.

    Returns:
        A set of strings representing the FIRST set for the given symbol.
    """
    first_set = set()

    # Get the FIRST set for the symbol
    symbol_first_set = first[symbol]

    # If the FIRST set contains epsilon and the state has next states, compute the FIRST set for the next states
    if 'epsilon' in symbol_first_set and state.next_states:
        # Add all elements in the FIRST set except epsilon to the result set
        first_set.update({elem for elem in symbol_first_set if elem != 'epsilon'})

        # Compute the FIRST set for each next state
        for next_symbol, next_state in state.next_states:
            if next_symbol == '$':
                first_set.add('epsilon')
            elif not is_terminal(next_symbol):
                first_set.update(compute_first_set(next_symbol, next_state))
            else:
                first_set.add(next_symbol)

        return first_set

    # If the FIRST set does not contain epsilon, return the FIRST set
    else:
        return symbol_first_set


def get_token_key(token: Tuple[str, str]) -> str:
    """
    This function returns a key for the given token, which is used to determine what the parser should look for when
    processing the token. If the token is an ID or NUM, the key is the token type (i.e., 'ID' or 'NUM'). Otherwise, the
    key is the token lexeme.

    Args:
        token: A tuple representing the token being processed, with the first element being the token type
               and the second element being the token lexeme (if applicable).

    Returns:
        A string representing the key for the given token.
    """
    if token[0] in ('ID', 'NUM'):
        # If the token is an ID or NUM, use the token type as the key
        key = token[0]
    else:
        # Otherwise, use the token lexeme as the key
        key = token[1]

    return key


def select_next_move(position: Tuple[str, 'State'], token):
    """
    This function selects the next move for the parser based on the current position in the state diagram and the
    current token being processed. It returns a tuple representing the next position in the state diagram and the
    token that was processed.

    Args:
        position: A tuple representing the current position in the state diagram, with the first element being the
                  current non-terminal symbol and the second element being the current state.
        token: A tuple representing the current token being processed, with the first element being the token type
               and the second element being the token lexeme (if applicable).

    Returns:
        A tuple representing the next position in the state diagram and the token that was processed.
    """
    for e, s in position[1].next_states:
        # compute the first set
        if is_terminal(e):
            if e == get_token_key(token):
                move_forward(s, token)
                return None

        elif e != 'epsilon':
            # compute the First of the rhs production
            if get_token_key(token) in compute_first_set(e, s):
                move_in(s, e)
                return token

    if get_token_key(token) in follow[stack[-1][0]]:
        for e, s in position[1].next_states:
            if e == 'epsilon':
                move_forward(s, e)
                return token
            elif not is_terminal(e):
                if 'epsilon' in first[e]:
                    move_in(s, e)
                    return token

    # ERROR handling
    if len(position[1].next_states) > 1:
        RuntimeError('impossible')

    next_edge, next_state = position[1].next_states[0]

    if get_token_key(token) == '$':
        print_eof_error()
        stack.clear()
        return None

    if is_terminal(next_edge):
        print_missing_error(next_edge)
        jump_forward(next_state, next_edge)
        return token

    else:
        if get_token_key(token) in follow[next_edge]:
            print_missing_error(next_edge)
            jump_forward(next_state, next_edge)
            return token
        else:
            print_illegal_error(get_token_key(token))
            return None


def print_tree(root: Node) -> None:
    """
    This function prints the tree structure of a given root node using the RenderTree module.

    Args:
        root: A 'Node' object representing the root node of the tree.

    Returns:
        None.
    """
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name), file=TREE_FILE)


def print_missing_error(missing_token: str) -> None:
    """
    This function prints an error message when a missing token is encountered during syntax analysis.
    It takes a missing token as an argument and prints an error message with the current line number
    and the missing token. It also sets a global flag 'SYNTAX_CORRECT_PROGRAM' to False, indicating
    that the program has a syntax error.

    Args:
        missing_token: A string representing the missing token.

    Returns:
        None.
    """
    print(f'#{scanner.get_current_line()} : syntax error, missing {missing_token}', file=SYNTAX_ERROR_FILE)
    global SYNTAX_CORRECT_PROGRAM
    SYNTAX_CORRECT_PROGRAM = False


def print_illegal_error(illegal_token: str) -> None:
    """
    This function prints an error message when an illegal token is encountered during syntax analysis.
    It takes an illegal token as an argument and prints an error message with the current line number
    and the illegal token. It also sets a global flag 'SYNTAX_CORRECT_PROGRAM' to False, indicating
    that the program has a syntax error.

    Args:
        illegal_token: A string representing the illegal token.

    Returns:
        None.
    """
    print(f'#{scanner.get_current_line()} : syntax error, illegal {illegal_token}', file=SYNTAX_ERROR_FILE)
    global SYNTAX_CORRECT_PROGRAM
    SYNTAX_CORRECT_PROGRAM = False


def print_eof_error() -> None:
    """
    This function prints an error message when an unexpected end-of-file (EOF) is encountered during
    syntax analysis. It prints an error message with the current line number and the message
    'Unexpected EOF'. It also sets a global flag 'SYNTAX_CORRECT_PROGRAM' to False, indicating that
    the program has a syntax error.

    Args:
        None.

    Returns:
        None.
    """
    print(f'#{scanner.get_current_line()} : syntax error, Unexpected EOF', file=SYNTAX_ERROR_FILE)
    global SYNTAX_CORRECT_PROGRAM
    SYNTAX_CORRECT_PROGRAM = False


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
