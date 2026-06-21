from typing import Tuple
from .minimax import minimax_move
from .evaluator import evaluate_state

ACTIVE_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "stability",
    "quiet_moves"
}

def make_move(state) -> Tuple[int, int]:
    return minimax_move(state, max_depth=-1, eval_func=lambda s, p: evaluate_state(s, p, ACTIVE_STRATEGIES))
