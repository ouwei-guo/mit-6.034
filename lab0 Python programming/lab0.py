# MIT 6.034 Lab 0: Getting Started
# Written by jb16, jmn, dxh, and past 6.034 staff

from point_api import Point

#### Multiple Choice ###########################################################

# These are multiple choice questions. You answer by replacing
# the symbol 'None' with a letter (or True or False), corresponding 
# to your answer.

# True or False: Our code supports both Python 2 and Python 3
# Fill in your answer in the next line of code (True or False):
ANSWER_1 = False

# What version(s) of Python do we *recommend* for this course?
#   A. Python v2.3
#   B. Python V2.5 through v2.7
#   C. Python v3.2 or v3.3
#   D. Python v3.4 or higher
# Fill in your answer in the next line of code ("A", "B", "C", or "D"):
ANSWER_2 = "D"


################################################################################
# Note: Each function we require you to fill in has brief documentation        # 
# describing what the function should input and output. For more detailed      # 
# instructions, check out the lab 0 wiki page!                                 #
################################################################################


#### Warmup ####################################################################

import math

def is_even(x):
    "If x is even, returns True; otherwise returns False"
    return x%2 == 0

def decrement(x):
    """Given a number x, returns x - 1 unless that would be less than
    zero, in which case returns 0."""
    if x <= 0:
        return 0
    return x-1

def cube(x):
    "Given a number x, returns its cube (x^3)"
    return x**3


#### Iteration #################################################################

def is_prime(x):
    "Given a number x, returns True if it is prime; otherwise returns False"
    if x < 2:
        return False
    if x == 2:
        return True
    if is_even(x):
        return False
    r = int(math.sqrt(x))
    for i in range(r):
        if x%(i+2) == 0:
            return False
    return True


def fast_is_prime(x):
    None

    
def primes_up_to(x):
    "Given a number x, returns an in-order list of all primes up to and including x"
    t = []
    n = int(x)
    if n < 2:
        return t
    for i in range(n+1):
        if is_prime(i):
            t.append(i)
    return t


#### Recursion #################################################################

def fibonacci(n):
    "Given a positive int n, uses recursion to return the nth Fibonacci number."
    if n < 0:
        return 0
    if n <= 2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)

def expression_depth(expr):
    """Given an expression expressed as Python lists, uses recursion to return
    the depth of the expression, where depth is defined by the maximum number of
    nested operations."""
    if isinstance(expr,str) or isinstance(expr,int):
        return 0
    if isinstance(expr,list):
        a = expression_depth(expr[1])
        b = expression_depth(expr[2])
        if b > a:
            return b+1
        return a+1
    
#### Built-in data types #######################################################

def remove_from_string(string, letters):
    """Given a string and a list of individual letters, returns a new string
    which is the same as the old one except all occurrences of those letters
    have been removed from it."""
    t = []
    for letter in string:
        if letter not in letters:
            t.append(letter)
    return ''.join(t)
            

def compute_string_properties(string):
    """Given a string of lowercase letters, returns a tuple containing the
    following three elements:
        0. The length of the string
        1. A list of all the characters in the string (including duplicates, if
           any), sorted in REVERSE alphabetical order
        2. The number of distinct characters in the string (hint: use a set)
    """
    t = len(string), sorted(list(string),reverse=True), len(set(string))
    return t

def tally_letters(string):
    """Given a string of lowercase letters, returns a dictionary mapping each
    letter to the number of times it occurs in the string."""
    return {x:string.count(x) for x in string}


#### Functions that return functions ###########################################

def create_multiplier_function(m):
    "Given a multiplier m, returns a function that multiplies its input by m."
    def multiply(a):
        return a*m
    return multiply

def create_length_comparer_function(check_equal):
    """Returns a function that takes as input two lists. If check_equal == True,
    this function will check if the lists are of equal lengths. If
    check_equal == False, this function will check if the lists are of different
    lengths."""
    def is_equal(a,b):
        return (check_equal or len(a) != len(b)) and (not (check_equal and len(a) != len(b)))
    return is_equal


#### Objects and APIs: Copying and modifing objects ############################

def sum_of_coordinates(point):
    """Given a 2D point (represented as a Point object), returns the sum
    of its X- and Y-coordinates."""
    return point.getX()+point.getY()

def get_neighbors(point):
    """Given a 2D point (represented as a Point object), returns a list of the
    four points that neighbor it in the four coordinate directions. Uses the
    "copy" method to avoid modifying the original point."""
    t = []
    t.append(point.copy().setX(point.getX()+1))
    t.append(point.copy().setX(point.getX()-1))
    t.append(point.copy().setY(point.getY()+1))
    t.append(point.copy().setY(point.getY()-1))
    return t


#### Using the "key" argument ##################################################

def sort_points_by_Y(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "sorted"
    with the "key" argument to create and return a list of the SAME (not copied)
    points sorted in decreasing order based on their Y coordinates, without
    modifying the original list."""
    my_sorting_function = lambda point: point.getY()
    t = sorted(list_of_points,key=my_sorting_function)
    return t[::-1]

def furthest_right_point(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "max" with
    the "key" argument to return the point that is furthest to the right (that
    is, the point with the largest X coordinate)."""
    my_sorting_function = lambda point: point.getX()
    return max(list_of_points,key=my_sorting_function)


#### SURVEY ####################################################################

# How much programming experience do you have, in any language?
#     A. No experience (never programmed before this lab)
#     B. Beginner (just started learning to program, e.g. took one programming class)
#     C. Intermediate (have written programs for a couple classes/projects)
#     D. Proficient (have been programming for multiple years, or wrote programs for many classes/projects)
#     E. Expert (could teach a class on programming, either in a specific language or in general)

PROGRAMMING_EXPERIENCE = "C"


# How much experience do you have with Python?
#     A. No experience (never used Python before this lab)
#     B. Beginner (just started learning, e.g. took 6.0001)
#     C. Intermediate (have used Python in a couple classes/projects)
#     D. Proficient (have used Python for multiple years or in many classes/projects)
#     E. Expert (could teach a class on Python)

PYTHON_EXPERIENCE = "B"


# Finally, the following questions will appear at the end of every lab.
# The first three are required in order to receive full credit for your lab.

NAME = 'Ouwei Guo'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = '0'
SUGGESTIONS = None #optional
