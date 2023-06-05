# IAWT


def pnext():
    pass

def temp_exch():
    pass

def pid():
    pass

def pplus():
    pass

def pminus():
    pass

def pless():
    pass

def peq():
    pass

def assign():
    pass

def assign_arr():
    pass

def do_op():
    pass

def do_mult():
    pass

def eval_ind():
    pass

def eval_ind_orig():
    pass

def make_patch():
    pass

def end_if():
    pass

def start_repeat():
    pass

def brk():
    pass

def end_repeat():
    pass

def call_output():
    pass

def do_action(action_symbol : str):
    eval(action_symbol[1:] + '()')


semantic_routines = {
    '#pnext' : pnext,
    '#temp_exch' : temp_exch,
    '#pid' : pid,
    '#pplus' : pplus,
    '#pminus' : pminus,
    '#pless' : pless,
    '#peq' : peq,
    '#assign' : assign,
    '#assign_arr' : assign_arr,
    '#do_op' : do_op,
    '#do_mult' : do_mult,
    '#eval_ind' : eval_ind,
    '#eval_ind_orig' : eval_ind_orig,
    '#make_patch' : make_patch,
    '#end_if' : end_if,
    '#start_repeat' : start_repeat,
    '#break' : brk,
    '#end_repeat' : end_repeat,
    '#call_output' : call_output,
}