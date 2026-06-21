import random
import time
import os
from typing import Tuple, Callable
import math

def minimax_move(state, max_depth:int, eval_func:Callable, time_limit:float=None) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited/iterative deepening)
    :param eval_func: the function to evaluate a terminal or leaf state
    :param time_limit: the maximum time in seconds the search is allowed to run
    :return: (int, int) tuple with x, y coordinates of the move
    """
    if time_limit is None:
        time_limit = float(os.environ.get('OTHELLO_TIME_LIMIT', 4.8))
        
    root_player = state.player
    start_time = time.time()
    
    def alpha_beta(current_state, depth, alpha, beta, maximizing_player):
        if time.time() - start_time > time_limit:
            raise TimeoutError("Time limit exceeded")
            
        if depth == 0 or current_state.is_terminal():
            return eval_func(current_state, root_player)

        moves = current_state.legal_moves()

        if maximizing_player:
            value = -math.inf
            for move in moves:
                next_st = current_state.next_state(move)
                is_max = (next_st.player == root_player)
                
                value = max(value, alpha_beta(next_st, depth - 1, alpha, beta, is_max))
                alpha = max(alpha, value)
                
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for move in moves:
                next_st = current_state.next_state(move)
                is_max = (next_st.player == root_player)
                
                value = min(value, alpha_beta(next_st, depth - 1, alpha, beta, is_max))
                beta = min(beta, value)
                
                if beta <= alpha:
                    break
            return value

    best_move_overall = None
    legal_moves = state.legal_moves()
    
    if not legal_moves:
        return (-1, -1)
        
    legal_moves_list = list(legal_moves)
    best_move_overall = legal_moves_list[0]
    
    # Se a profundidade for fixa, apenas roda ate a profundidade pedida
    target_depths = [max_depth] if max_depth != -1 else range(1, 100)

    for depth in target_depths:
        best_value_for_depth = -math.inf
        alpha = -math.inf
        beta = math.inf
        best_move_for_depth = None

        try:
            for move in legal_moves:
                if time.time() - start_time > time_limit:
                    raise TimeoutError()
                    
                next_st = state.next_state(move)
                is_max = (next_st.player == root_player)
                
                value = alpha_beta(next_st, depth - 1, alpha, beta, is_max)
                
                if value > best_value_for_depth or best_move_for_depth is None:
                    best_value_for_depth = value
                    best_move_for_depth = move
                    
                alpha = max(alpha, value)
                
            if best_move_for_depth is not None:
                best_move_overall = best_move_for_depth
                
        except TimeoutError:
            # Tempo acabou, retorna a melhor jogada encontrada na profundidade anterior completa
            # ou a melhor jogada parcial da profundidade atual
            if best_move_for_depth is not None:
                best_move_overall = best_move_for_depth
            break

    return best_move_overall
