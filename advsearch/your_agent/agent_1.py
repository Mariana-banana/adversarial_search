from typing import Tuple
from .minimax import minimax_move
from .evaluator import evaluate_state

ACTIVE_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "frontier",
    "coin_parity"
}

def make_move(state) -> Tuple[int, int]:
    # Use max_depth=-1 for iterative deepening bounded by time
    return minimax_move(state, max_depth=-1, eval_func=lambda s, p: evaluate_state(s, p, ACTIVE_STRATEGIES))
