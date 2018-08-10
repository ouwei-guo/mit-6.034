# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import *


#### Part 1: Warmup ############################################################

def has_empty_domains(csp) :
    """Returns True if the problem has one or more empty domains, otherwise False"""
    for key in list(csp.domains.keys()):
        if len(csp.domains[key]) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    if csp.assignments == {}:
        return True
    for c in csp.get_all_constraints():
        one = csp.get_assignment(c.var1)
        two = csp.get_assignment(c.var2)
        if one != None and two != None:
            if not c.check(one,two):
                return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem) :
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    if has_empty_domains(problem):
        return None, 1
    num_extensions = 0
    agenda = [problem]
    while len(agenda) > 0:
        p = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(p) and check_all_constraints(p):
            uns = p.pop_next_unassigned_var()
            if uns == None:
                return p.assignments,num_extensions
            cop = []
            for val in p.get_domain(uns):
                cop.append(p.copy().set_assignment(uns,val))
            cop = cop + agenda
            agenda = cop
    return None,num_extensions

#print(solve_constraint_dfs(get_pokemon_problem()))

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.


ANSWER_1 = 20


#### Part 3: Forward Checking ##################################################

def eliminate_from_neighbors(csp, var) :
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    dom = {}
    cop = csp.copy()
    for nb in csp.get_neighbors(var):
        c = csp.constraints_between(nb, var)
        if len(c) > 1:
            csp.set_domain(nb, [])
            return None
        else:
            for val1 in csp.get_domain(nb):
                count = 0
                for val2 in csp.get_domain(var):
                    if not c[0].check(val1,val2):
                        count += 1
                if count == len(csp.get_domain(var)):
                    cop.eliminate(nb,val1)
                    csp.set_domain(nb,cop.get_domain(nb))
                    if len(csp.get_domain(nb)) == 0:
                        return None
                    dom.setdefault(nb)
    return sorted(dom.keys())


#p=get_pokemon_problem()
#p.set_assignment('Q1', 'B')
#p=CSP_B_nope.copy()
#print(p)
#print(eliminate_from_neighbors(p,'Q1'))
#print(p)
# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors

def solve_constraint_forward_checking(problem) :
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    #print(problem)
    if has_empty_domains(problem):
        return None, 1
    num_extensions = 0
    agenda = [problem]
    while len(agenda) > 0:
        p = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(p) and check_all_constraints(p):
            uns = p.pop_next_unassigned_var()
            if uns == None:
                return p.assignments,num_extensions
            cop = []
            for val in p.get_domain(uns):
                csp = p.copy().set_assignment(uns,val)
                forward_check(csp,uns)
                #csp = eliminate_from_neighbors(p.copy().set_assignment(uns,val),uns)
                cop.append(csp)
            cop = cop + agenda
            agenda = cop
    return None,num_extensions

#print(solve_constraint_forward_checking(get_pokemon_problem()))

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = 9


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None) :
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    if queue == None:
        queue = csp.get_all_variables()
    deque = []
    while len(queue) > 0:
        var = queue.pop(0)
        fc = forward_check(csp,var)
        if fc == None:
            return None
        queue += fc
        deque.append(var)
    return deque

#p=CSP_almost_stuck.copy()
#print(domain_reduction(p,['A']))
#p=get_pokemon_problem()
#print(domain_reduction(p))
#print(solve_constraint_forward_checking(p))

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

ANSWER_3 = 6


def solve_constraint_propagate_reduced_domains(problem) :
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    if has_empty_domains(problem):
        return None, 1
    num_extensions = 0
    agenda = [problem]
    while len(agenda) > 0:
        p = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(p) and check_all_constraints(p):
            uns = p.pop_next_unassigned_var()
            if uns == None:
                return p.assignments,num_extensions
            cop = []
            for val in p.get_domain(uns):
                csp = p.copy().set_assignment(uns,val)
                #forward_check(csp,uns)
                domain_reduction(csp,[uns])
                cop.append(csp)
            cop = cop + agenda
            agenda = cop
    return None,num_extensions

#p=get_pokemon_problem()
#print(solve_constraint_propagate_reduced_domains(p))
# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = 7


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None) :
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    if queue == None:
        queue = csp.get_all_variables()
    deque = []
    while len(queue) > 0:
        var = queue.pop(0)
        fc = forward_check(csp,var)
        if fc == None:
            return None
        for v in fc:
            if enqueue_condition_fn(csp,v):
                queue.append(v)
        deque.append(var)
    return deque

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var)) == 1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None) :
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    if has_empty_domains(problem):
        return None, 1
    num_extensions = 0
    agenda = [problem]
    while len(agenda) > 0:
        p = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(p) and check_all_constraints(p):
            uns = p.pop_next_unassigned_var()
            if uns == None:
                return p.assignments,num_extensions
            cop = []
            for val in p.get_domain(uns):
                csp = p.copy().set_assignment(uns,val)
                if enqueue_condition != None:
                    propagate(enqueue_condition, csp,[uns])
                cop.append(csp)
            cop = cop + agenda
            agenda = cop
    return None,num_extensions

p=get_pokemon_problem()
print(solve_constraint_generic(p,condition_singleton))

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = 8


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return m-1 == n or m+1 == n

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return m-1 != n and m+1 != n

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    con = []
    for i in range(len(variables)-1):
        for j in range(len(variables)-i-1):
            con.append(Constraint(variables[i],variables[i+j+1],constraint_different))
    return con


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
