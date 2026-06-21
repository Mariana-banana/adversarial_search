from typing import Tuple
from .minimax import minimax_move
from .evaluator import evaluate_state

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# Conjunto completo de estrategias (config que venceu o torneio interno dos colegas).
# Os pesos por fase do jogo (early/mid/late) ficam dentro de evaluate_state (evaluator.py).
ALL_STRATEGIES = {
    "corner_control",
    "corner_closeness",
    "mobility",
    "frontier",
    "stability",
    "coin_parity",
    "region_parity",
    "quiet_moves",
    "edge_configurations",
    "evaporation",
}

# Valor atribuido a estados terminais (domina qualquer pontuacao heuristica).
WIN_SCORE = 1_000_000.0

# Profundidade fixa calibrada para caber nos 5s da maquina do torneio (Passo 7).
# Esta heuristica e' a mais cara (varre o tabuleiro varias vezes): ~1,9s @ prof 5 no Mac
# (-> ~7,7s na maquina de referencia, arriscado), entao fica em prof 4 (~0,2s -> ~0,8s, seguro).
CUSTOM_MAX_DEPTH = 4


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado dado, usando minimax com poda alfa-beta
    e a heuristica customizada (multiplos fatores, com pesos por fase do jogo).
    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return minimax_move(state, CUSTOM_MAX_DEPTH, evaluate_custom)


def evaluate_custom(state, player: str) -> float:
    """
    Avalia um estado de Othello pelo ponto de vista do jogador dado.
    Se o estado for terminal, retorna o resultado REAL (vitoria/derrota/empate) com
    valor extremo -- nao faz sentido "chutar" quando o jogo ja acabou.
    Caso contrario, retorna a estimativa heuristica combinando as 10 estrategias.
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
    return evaluate_state(state, player, ALL_STRATEGIES)
