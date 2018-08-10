# MIT 6.034 Lab 8: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    acs = set()
    for p in net.get_parents(var):
        acs.add(p)
        acs = acs.union(get_ancestors(net, p))
    return acs

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    dsc = set()
    for p in net.get_children(var):
        dsc.add(p)
        dsc = dsc.union(get_descendants(net, p))
    return dsc

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    nnd = set()
    dsc = get_descendants(net, var)
    for v in net.get_variables():
        if v not in dsc:
            nnd.add(v)
    nnd.remove(var)
    return nnd


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """
    sg = {}
    pr = net.get_parents(var)
    dsc = get_descendants(net, var)
    g = set(givens.keys())
    if pr.issubset(g):
        for k in g.difference(pr):
            if k in dsc:
                return givens
        for k in g:
            if k in pr:
                sg.setdefault(k,givens[k])
        return sg
    return givens
    
def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    if givens == None:
        try:
            pr = net.get_probability(hypothesis)
            return pr
        except ValueError:
            raise LookupError
    g = simplify_givens(net, list(hypothesis)[0], givens)
    #print(net,hypothesis,givens,g)
    try:
        pr = net.get_probability(hypothesis,g)
        return pr
    except ValueError:
        raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    pj = []
    for k in hypothesis.keys():
        pj.append(probability_lookup(net,{k:hypothesis[k]},hypothesis))
    return product(pj)
    
def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    raise NotImplementedError

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    raise NotImplementedError
    
def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    raise NotImplementedError


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    raise NotImplementedError


#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    raise NotImplementedError
    
def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """
    raise NotImplementedError


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
