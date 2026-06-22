from typing import Tuple
from .minimax import iterative_deepening_move
from .evaluator import evaluate_state

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# Conjunto de estrategias usado pela heuristica customizada (config do agent_1).
# Os pesos por fase do jogo (early/mid/late) ficam dentro de evaluate_state (evaluator.py).
BEST_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "frontier",
    "coin_parity",
}

# Valor atribuido a estados terminais (domina qualquer pontuacao heuristica).
WIN_SCORE = 1_000_000.0

# Orcamento de tempo por jogada para o mini-torneio do relatorio (bem abaixo dos 5s).
TIME_LIMIT = 2.0


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado dado, usando minimax com poda alfa-beta e
    aprofundamento iterativo limitado por tempo, guiado pela heuristica customizada
    (conjunto de estrategias do agent_1, com pesos por fase do jogo).
    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return iterative_deepening_move(state, evaluate_custom, time_limit=TIME_LIMIT)


def evaluate_custom(state, player: str) -> float:
    """
    Avalia um estado de Othello pelo ponto de vista do jogador dado.
    Se o estado for terminal, retorna o resultado REAL (vitoria/derrota/empate) com
    valor extremo -- nao faz sentido "chutar" quando o jogo ja acabou.
    Caso contrario, retorna a estimativa heuristica combinando as estrategias de BEST_STRATEGIES.
    :param state: estado a avaliar (GameState)
    :param player: jogador para avaliar o estado (B ou W)
    """
    if state.is_terminal():
        winner = state.winner()
        if winner == player:
            return WIN_SCORE
        elif winner is None:        # empate
            return 0.0
        else:
            return -WIN_SCORE
    return evaluate_state(state, player, BEST_STRATEGIES)
