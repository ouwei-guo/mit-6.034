# MIT 6.034 Lab 7: Support Vector Machines
# Written by 6.034 staff

from svm_data import *
from functools import reduce
import math
INF = float('inf')
#### Part 1: Vector Math #######################################################

def dot_product(u, v):
    """Computes the dot product of two vectors u and v, each represented 
    as a tuple or list of coordinates. Assume the two vectors are the
    same length."""
    u = list(u)
    v = list(v)
    dp = 0
    for a,b in zip(u,v):
        dp += a*b
    return dp

def norm(v):
    """Computes the norm (length) of a vector v, represented 
    as a tuple or list of coords."""
    return math.sqrt(dot_product(v,v))


#### Part 2: Using the SVM Boundary Equations ##################################

def positiveness(svm, point):
    """Computes the expression (w dot x + b) for the given Point x."""
    return dot_product(svm.w,point.coords) + svm.b

def classify(svm, point):
    """Uses the given SVM to classify a Point. Assume that the point's true
    classification is unknown.
    Returns +1 or -1, or 0 if point is on boundary."""
    p = positiveness(svm, point)
    if p > 0:
        return 1
    elif p < 0:
        return -1
    return 0

def margin_width(svm):
    """Calculate margin width based on the current boundary."""
    return 2/norm(svm.w)

def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification, for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    tp = set()
    for p in svm.training_points:
        if p in svm.support_vectors:
            if p.classification != positiveness(svm, p):
                tp.add(p)
        else:
            if abs(positiveness(svm, p)) <= margin_width(svm):
                tp.add(p)
    return tp


#### Part 3: Supportiveness ####################################################

def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    ca = set()
    for p in svm.training_points:
        if p in svm.support_vectors:
            if p.alpha <= 0:
                ca.add(p)
        elif p.alpha != 0:
            ca.add(p)
    return ca

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False. Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    sp = [0,0]
    t = 0
    for p in svm.training_points:
        if p in svm.support_vectors:
            sp = vector_add(sp,scalar_mult(p.classification*p.alpha,p.coords))
            #sp[1] += p.classification*p.alpha*p.coords[1]
        t += p.classification*p.alpha
    if t == 0 and sp == svm.w:
        return True
    return False


#### Part 4: Evaluating Accuracy ###############################################

def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    return check_gutter_constraint(svm)


#### Part 5: Training an SVM ###################################################

def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b. Return the updated SVM."""
    ca = check_alpha_signs(svm)
    for p in ca:
        if p in svm.support_vectors:
            svm.support_vectors.remove(p)
    w = [0,0]
    bp = -INF
    bm = INF
    for p in svm.training_points:
        if p.alpha != 0:
            if p not in svm.support_vectors:
                svm.support_vectors.append(p)
            w = vector_add(w,scalar_mult(p.classification*p.alpha,p.coords))
    for p in svm.support_vectors:
        if p.classification == -1:
            bm = min(bm, p.classification-dot_product(w,p.coords))
        else:
            bp = max(bp, p.classification-dot_product(w,p.coords))
    return svm.set_boundary(w, (bm+bp)/2)


#### Part 6: Multiple Choice ###################################################

ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A', 'D']
ANSWER_6 = ['A', 'B', 'D']
ANSWER_7 = ['A', 'B', 'D']
ANSWER_8 = []
ANSWER_9 = ['A', 'B', 'D']
ANSWER_10 = ['A', 'B', 'D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
