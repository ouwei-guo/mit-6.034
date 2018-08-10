# MIT 6.034 Lab 3: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1

INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    chains = board.get_all_chains()
    for c in chains:
        if len(c) >= 4:
            return True
        
    for col in range(board.num_cols):
        if board.is_column_full(col) == False:
            return False
    return True
        
def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    moves = []
    if is_game_over_connectfour(board):
        return moves

    for col in range(board.num_cols):
        if board.is_column_full(col) == False:
            moves.append(col)
    return [board.add_piece(m) for m in moves]    
    
def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_game_over_connectfour(board):
        chains = board.get_all_chains()
        for c in chains:
            if len(c) >= 4:
                if is_current_player_maximizer:
                    return -1000
                else:
                    return 1000
        else:
            return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    pieces = board.count_pieces()
    if is_game_over_connectfour(board):
        chains = board.get_all_chains()
        for c in chains:
            if len(c) >= 4:
                if is_current_player_maximizer:
                    return -2000 + pieces
                else:
                    return 2000 - pieces
        else:
            return 0

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    current_chains = board.get_all_chains(is_current_player_maximizer)
    other_chains = board.get_all_chains(not(is_current_player_maximizer))
    score = 0
    
    for c in current_chains:
        if len(c) == 1:
            score +=1
        if len(c) == 2:
            score +=10
        if len(c) == 3:
            score +=100
    for c in other_chains:
        if len(c) == 1:
            score -=1
        if len(c) == 2:
            score -=10
        if len(c) == 3:
            score -=100      
    return score

            
#Now we can create AbstractGameState objects for Connect Four, using some of
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
    agenda = [[state]]
    static_evals = 0
    best_path = None, None #path, endgame_score
    
    while agenda!=[]:
        path = agenda.pop()
        node = path[-1]
      
        children = node.generate_next_states()
        
        if children!=[]:
            for c in children:
                if c not in path:
                    agenda.append(path + [c])
        else:
            node_val = node.get_endgame_score(is_current_player_maximizer=True)
            static_evals += 1
            
            if best_path == (None, None) or node_val > best_path[-1]:
                    best_path = path, node_val 
                                              
    return best_path[-2], best_path[-1], static_evals

# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:
#pretty_print_dfs_type(dfs_maximizing(GAME1))
    
def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    static_evals = 0
    best_path = None, None #path, #minimax_score
    
    next_states = state.generate_next_states()
    
    if  next_states == []:
        return [state], state.get_endgame_score(is_current_player_maximizer=maximize), 1

    if maximize == True:
        for ns in next_states:
            new_res = minimax_endgame_search(ns, False) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] > best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
    else:
        for ns in next_states:
            new_res = minimax_endgame_search(ns, True) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] < best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
                
    return best_path[-2], best_path[-1], static_evals

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:
#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    static_evals = 0
    best_path = None, None #path, #minimax_score
    
    next_states = state.generate_next_states()
    
    if  next_states == []:
        return [state], state.get_endgame_score(is_current_player_maximizer=maximize), 1

    if depth_limit == 0:
        return [state], heuristic_fn(state.get_snapshot(), maximize), 1
    
    if maximize == True:
        for ns in next_states:
            new_res = minimax_search(ns, heuristic_fn, depth_limit-1, False) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] > best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
    else:
        for ns in next_states:
            new_res = minimax_search(ns, heuristic_fn, depth_limit-1, True) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] < best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
                
    return best_path[-2], best_path[-1], static_evals

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:
#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type 
    as dfs_maximizing."""
    static_evals = 0
    best_path = None, None #path, #minimax_score
    
    next_states = state.generate_next_states()
    
    if  next_states == []:
        return [state], state.get_endgame_score(is_current_player_maximizer=maximize), 1

    if depth_limit == 0:
        return [state], heuristic_fn(state.get_snapshot(), maximize), 1
    
    if maximize == True:
        for ns in next_states:
            new_res = minimax_search_alphabeta(ns, alpha, beta, 
                                               heuristic_fn, depth_limit-1, False) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] > best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
                alpha = max(new_res[-2], alpha)
                if alpha >= beta:
                    return best_path[-2], alpha, static_evals          
    else:
        for ns in next_states:
            new_res = minimax_search_alphabeta(ns, alpha, beta,
                                     heuristic_fn, depth_limit-1, True) #path, minimax, static, -3, -2, -1
            static_evals += new_res[-1]
            
            if best_path[-1] == None or new_res[-2] < best_path[-1]:
                best_path = [state] + new_res[-3], new_res[-2]
                beta = min(new_res[-2], beta)
                if alpha >= beta:
                    return best_path[-2], beta, static_evals
                
    return best_path[-2], best_path[-1], static_evals

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.
#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))

def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime = AnytimeValue()
    for d in range(1, depth_limit+1):
        result = minimax_search_alphabeta(state, -INF, INF, heuristic_fn, d, maximize)
        anytime.set_value(result)
    return anytime
        
# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


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
