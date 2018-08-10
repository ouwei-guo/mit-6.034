# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by 6.034 Staff

from api import *
from data import *
import math
from operator import itemgetter, attrgetter
from collections import Counter
log2 = lambda x: math.log(x, 2)
INF = float('inf')


################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################


#### Part 1A: Classifying points ###############################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        return id_tree.get_node_classification()
    return id_tree_classify_point(point, id_tree.apply_classifier(point))

#### Part 1B: Splitting data with a classifier #################################

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    m = {}
    for d in data:
        m.setdefault(classifier.classify(d),[]).append(d)
    #print(m)
    return m


#### Part 1C: Calculating disorder #############################################

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    dis = 0.0
    cl = split_on_classifier(data, target_classifier)
    for k in cl.keys():
        dis += -(len(cl[k])/len(data))*log2(len(cl[k])/len(data))
        #print((len(cl[k])/len(data)))
    return dis

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    dis = 0.0
    cl = split_on_classifier(data, test_classifier)
    for k in cl:
        dis += (len(cl[k])/len(data))*branch_disorder(cl[k], target_classifier)
        #print(dis)
    return dis


## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:

#for classifier in tree_classifiers:
#    print(classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type")))


#### Part 1D: Constructing an ID tree ##########################################

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    dis = 2
    clas = None
    for c in possible_classifiers:
        av = average_test_disorder(data, c, target_classifier)
        #print(c,av)
        if av < dis:
            dis = av
            clas = c
            if dis <= 0:
                return clas
    if clas != None and len(split_on_classifier(data,clas).keys()) == 1:
        raise NoGoodClassifiersError("No good classifiers found")
    return clas


## To find the best classifier from 2014 Q2, Part A, uncomment:
#print(find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type")))

def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if id_tree_node == None:
        id_tree_node = IdentificationTreeNode(target_classifier)
    if branch_disorder(data, target_classifier) == 0.0:
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
    else:
        try:
            bc = find_best_classifier(data, possible_classifiers, target_classifier)
        except NoGoodClassifiersError:
            return id_tree_node
        f = split_on_classifier(data, bc)
        id_tree_node.set_classifier_and_expand(bc, f)
        possible_classifiers.remove(bc)
        br = id_tree_node.get_branches()
        for k in br:
            br[k] = construct_greedy_id_tree(f[k],possible_classifiers,target_classifier,br[k])
    return id_tree_node


## To construct an ID tree for 2014 Q2, Part A:
#print(construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type")))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print(id_tree_classify_point(tree_test_point, tree_tree))

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print(construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification")))
#print(construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class")))


#### Part 1E: Multiple choice ##################################################

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


#### OPTIONAL: Construct an ID tree with medical data ##########################

## Set this to True if you'd like to do this part of the lab
DO_OPTIONAL_SECTION = False

if DO_OPTIONAL_SECTION:
    from parse import *
    medical_id_tree = construct_greedy_id_tree(heart_training_data, heart_classifiers, heart_target_classifier_discrete)


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### Part 2A: Drawing Boundaries ###############################################

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### Part 2B: Distance metrics #################################################

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    u = list(u)
    v = list(v)
    dp = 0
    for a,b in zip(u,v):
        dp += a*b
    return dp

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return math.sqrt(dot_product(v,v))

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    ed = 0
    for a,b in zip(point1.coords,point2.coords):
        ed += (a-b)**2
    return math.sqrt(ed)

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    md = 0
    for a,b in zip(point1.coords,point2.coords):
        md += abs(a-b)
    return md

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    return sum(v1 != v2 for v1,v2 in zip(point1.coords,point2.coords))

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    return 1-(dot_product(point1.coords,point2.coords)/(norm(point1.coords)*norm(point2.coords)))


#### Part 2C: Classifying points ###############################################

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    t = []
    m = []
    for p in sorted(data,key=attrgetter('coords')):
        t.append((p,distance_metric(point,p)))
    for p in sorted(t,key=itemgetter(1)):
        m.append(p[0])
    return m[0:k]

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    m = []
    kn = get_k_closest_points(point, data, k, distance_metric)
    for p in kn:
        m.append(p.classification)
    d = Counter(m)
    return d.most_common(1)[0][0]


## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print(knn_classify_point(knn_tree_test_point, knn_tree_data, 1, euclidean_distance))


#### Part 2C: Choosing k #######################################################

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    c = []
    #p = []
    cv = 0
    for d in data:
        c = data[:]
        c.remove(d)
        #p = get_k_closest_points(d, c, k, distance_metric)
        if d.classification == knn_classify_point(d, c, k, distance_metric):
            cv += 1
    return cv/len(data)

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    k = 0
    m = 0.0
    dm = euclidean_distance
    for i in range(len(data)-1):
        cv = cross_validate(data,i+1,euclidean_distance)
        if cv > m:
            m = cv
            k = i
            dm = euclidean_distance
    for i in range(len(data)-1):
        cv = cross_validate(data,i+1,manhattan_distance)
        if cv > m:
            m = cv
            k = i
            dm = manhattan_distance
    for i in range(len(data)-1):
        cv = cross_validate(data,i+1,hamming_distance)
        if cv > m:
            m = cv
            k = i
            dm = hamming_distance
    for i in range(len(data)-1):
        cv = cross_validate(data,i+1,cosine_distance)
        
        if cv > m:
            m = cv
            k = i
            dm = cosine_distance
    return (k,dm)

## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print(find_best_k_and_metric(knn_tree_data))


#### Part 2E: More multiple choice #############################################

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
