from typing import Tuple
from .minimax import iterative_deepening_move
from .evaluator import evaluate_state

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

TIME_LIMIT = 4.5

def make_move(state) -> Tuple[int, int]:
    return iterative_deepening_move(state, eval_func=lambda s, p: evaluate_state(s, p, ACTIVE_STRATEGIES), time_limit=TIME_LIMIT)
