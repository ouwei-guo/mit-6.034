# MIT 6.034 Lab 3: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1
import time

INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    c = board.get_all_chains()
    for p in c:
        if len(p) > 3:
            return True
    for i in range(board.num_cols):
        if board.is_column_full(i):
            if i == 6:
                return True
        else:
            return False

def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    t = []
    for i in range(board.num_cols):
        if not board.is_column_full(i):
            t.append(board.add_piece(i))
    return t

def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_current_player_maximizer:
        p = -1000
        c = board.get_all_chains(not is_current_player_maximizer)
    else:
        p = 1000
        c = board.get_all_chains(is_current_player_maximizer)
    for s in c:
        if len(s) > 3:
            return p
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if is_current_player_maximizer:
        p = -1000-(1000/board.count_pieces(not is_current_player_maximizer))
        c = board.get_all_chains(not is_current_player_maximizer)
    else:
        p = 1000+(1000/board.count_pieces(is_current_player_maximizer))
        c = board.get_all_chains(is_current_player_maximizer)
    for s in c:
        if len(s) > 3:
            return p
    return 0

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    curr_chain = board.get_all_chains(is_current_player_maximizer)
    prev_chain = board.get_all_chains(not is_current_player_maximizer)
    heur = 0
    if is_current_player_maximizer:
        if board.get_piece(3, 5) == 1:
            heur = 100
    elif board.get_piece(3, 5) == 1:
        heur = -100
    heur += len(prev_chain)/(len(curr_chain)+1)
    for c in curr_chain:
        if len(c) > 2:
            heur += 5
        else:
            heur += len(c)
    for c in prev_chain:
        if len(c) > 2:
            heur -= 5
        else:
            heur -= len(c)
    if heur == 0:
        return -1
    return heur**3/10

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    nex = state.generate_next_states()
    agenda = []
    best_path = []
    for p in nex:
        agenda.append([state,p])
    best_score = 0
    number_eval = 0
    while len(agenda) > 0:
        t = agenda.pop(0)
        if t[-1].is_game_over():
            number_eval += 1
            if t[-1].get_endgame_score() > best_score:
                best_score = t[-1].get_endgame_score()
                best_path = t
        else:
            nex = t[-1].generate_next_states()
            tem = []
            for p in nex:
                tem.append(t+[p])
            agenda = tem + agenda
    return (best_path,best_score,number_eval)


# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

#pretty_print_dfs_type(dfs_maximizing(GAME1))

def minimax_endgame_search(state, maximize=True):
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    number_eval = 0    
    def min_play(state, maximize):
        if state[-1].is_game_over():
            nonlocal number_eval
            number_eval +=1
            return state, state[-1].get_endgame_score(maximize)
        min_score = INF
        min_path = []
        agenda = []
        for p in state[-1].generate_next_states():
            agenda.append(state+[p])
        while len(agenda) > 0:
            t = agenda.pop(0)
            path, score = max_play(t, not maximize)
            if min_score > score:
                min_path = path
                min_score = score
        return min_path, min_score

    def max_play(state, maximize):
        if state[-1].is_game_over():
            nonlocal number_eval
            number_eval +=1
            return state, state[-1].get_endgame_score(maximize)
        max_score = -INF
        max_path = []
        agenda = []
        for p in state[-1].generate_next_states():
            agenda.append(state+[p])
        while len(agenda) > 0:
            t = agenda.pop(0)
            path, score = min_play(t, not maximize)
            if max_score < score:
                max_path = path
                max_score = score
        return max_path, max_score
    best_path = []
    best_score = 0
    if maximize:
        best_path, best_score = max_play([state],maximize)
    else:
        best_path, best_score = min_play([state],maximize)
    return (best_path,best_score,number_eval)

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER,True))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    number_eval = 0    
    def min_play(state, depth, maximize):
        if state[-1].is_game_over():
            nonlocal number_eval
            number_eval +=1
            return state, state[-1].get_endgame_score(maximize)
        elif depth == 0:
            number_eval +=1
            return state, heuristic_fn(state[-1].snapshot,maximize)
        min_score = INF
        min_path = []
        agenda = []
        for p in state[-1].generate_next_states():
            agenda.append(state+[p])
        while len(agenda) > 0:
            t = agenda.pop(0)
            path, score = max_play(t, depth-1, not maximize)
            if min_score > score:
                min_path = path
                min_score = score
        return min_path, min_score

    def max_play(state, depth, maximize):
        if state[-1].is_game_over():
            nonlocal number_eval
            number_eval +=1
            return state, state[-1].get_endgame_score(maximize)
        elif depth == 0:
            number_eval +=1
            return state, heuristic_fn(state[-1].snapshot,maximize)
        max_score = -INF
        max_path = []
        agenda = []
        for p in state[-1].generate_next_states():
            agenda.append(state+[p])
        while len(agenda) > 0:
            t = agenda.pop(0)
            path, score = min_play(t, depth-1, not maximize)
            if max_score < score:
                max_path = path
                max_score = score
        return max_path, max_score
    best_path = []
    best_score = 0
    if maximize:
        best_path, best_score = max_play([state],depth_limit,maximize)
    else:
        best_path, best_score = min_play([state],depth_limit,maximize)
    return (best_path,best_score,number_eval)

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(GAME1,False))
#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))
print(GAME1)

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type 
    as dfs_maximizing."""
    number_eval = 0
    def alpha_beta_search(state, maximize, depth, alpha, beta, alpha_node=[], beta_node=[]):
        if state[-1].is_game_over():
            nonlocal number_eval
            number_eval +=1
            return state[-1].get_endgame_score(maximize), state
        elif depth == 0:
            number_eval +=1
            return heuristic_fn(state[-1].snapshot, maximize), state
        agenda = []
        for p in state[-1].generate_next_states():
            agenda.append(state+[p])
        while len(agenda) > 0:
            t = agenda.pop(0)
            score, path = alpha_beta_search(t, not maximize, depth-1, alpha, beta, alpha_node, beta_node)
            #print(score)
            if maximize:
                if score > alpha:
                    alpha_node = path
                    alpha = score
            elif score < beta:
                beta_node = path
                beta = score
            if beta <= alpha:
                agenda = []
        if maximize:
            return alpha, alpha_node
        else:
            return beta, beta_node
    best_path = []
    best_score = 0
    best_score, best_path = alpha_beta_search([state],maximize,depth_limit,alpha,beta)
    return (best_path,best_score,number_eval)

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))
#print('------------')

def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()
    for i in range(depth_limit):
        value = minimax_search_alphabeta(state,heuristic_fn=heuristic_fn,depth_limit=i+1,maximize=maximize)
        if value != anytime_value.get_value():
            anytime_value.set_value(value)
            #anytime_value.pretty_print()
    return anytime_value


# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=3).pretty_print()

# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented


#### Part 3: Multiple Choice ###################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
