from typing import Tuple
from .minimax import iterative_deepening_move
from .evaluator import evaluate_state

ACTIVE_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "frontier",
    "coin_parity"
}

TIME_LIMIT = 4.5

def make_move(state) -> Tuple[int, int]:
    return iterative_deepening_move(state, eval_func=lambda s, p: evaluate_state(s, p, ACTIVE_STRATEGIES), time_limit=TIME_LIMIT)
