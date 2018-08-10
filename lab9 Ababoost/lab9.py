# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by 6.034 staff

from math import log as ln
from operator import itemgetter, attrgetter
from utils import *


#### Part 1: Helper functions ##################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    w = {}
    f = make_fraction(1/len(training_points))
    for p in training_points:
        w.setdefault(p,f)
    return w

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    er = {}
    for c in classifier_to_misclassified:
        e = 0
        for p in classifier_to_misclassified[c]:
            e += point_to_weight[p]
        er.setdefault(c,e)
    return er

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error:
        h = min(classifier_to_error_rate,key=lambda i:classifier_to_error_rate[i])
        if classifier_to_error_rate[h] >= make_fraction(1,2):
            raise NoGoodClassifiersError
        else:
            return h
    else:
        h = max(classifier_to_error_rate,key=lambda i:classifier_to_error_rate[i])
        if classifier_to_error_rate[h] <= make_fraction(1,2):
            raise NoGoodClassifiersError
        else:
            return h

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        return INF
    elif error_rate == 1:
        return -INF
    return 0.5*ln((1-error_rate)/error_rate)

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    om = []
    for p in training_points:
        y = 0
        n = 0
        for c,v in H:
            if p in classifier_to_misclassified[c]:
                y += v
            else:
                n += v
        if y >= n:
            om.append(p)
    return set(om)

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    om = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
    if len(om) > mistake_tolerance:
        return False
    return True

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    nw = {}
    for p in point_to_weight:
        if p in misclassified_points:
            w = make_fraction(1,2)*make_fraction(1,error_rate)*point_to_weight[p]
            nw.setdefault(p,w)
        else:
            w = make_fraction(1,2)*make_fraction(1,1-error_rate)*point_to_weight[p]
            nw.setdefault(p,w)
    return nw


#### Part 2: Adaboost ##########################################################

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    H = []
    point_to_weight = initialize_weights(training_points)
    while max_rounds > 0:
        max_rounds -= 1
        classifier_to_error_rate = calculate_error_rates(point_to_weight, classifier_to_misclassified)
        try:
            best = pick_best_classifier(classifier_to_error_rate, use_smallest_error)
        except NoGoodClassifiersError:
            return H
        vp = calculate_voting_power(classifier_to_error_rate[best])
        H.append((best,vp))
        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        misclassified_points = get_overall_misclassifications([(best,vp)], training_points, classifier_to_misclassified)
        point_to_weight = update_weights(point_to_weight, misclassified_points, classifier_to_error_rate[best])
    return H

#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
