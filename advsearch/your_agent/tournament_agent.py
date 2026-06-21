import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

ACTIVE_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "frontier",
    "stability",
    "coin_parity",
    "region_parity",
    "quiet_moves",
    "edge_configurations",
    "evaporation"
}

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    Consider that this will be called in the Othello tournament situation,
    so you should call the best implementation you got.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    return minimax_move(state, max_depth=-1, eval_func=lambda s, p: evaluate_state(s, p, ACTIVE_STRATEGIES))
