from typing import Tuple
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# Profundidade fixa calibrada para caber nos 5s da maquina do torneio (Passo 7).
# Medido: ~0,65s @ prof 5 no Mac; com fator ~4x da maquina de referencia -> ~2,6s (margem ok).
COUNT_MAX_DEPTH = 5


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado dado, usando minimax com poda alfa-beta
    e a heuristica de contagem de pecas.
    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return minimax_move(state, COUNT_MAX_DEPTH, evaluate_count)


def evaluate_count(state, player: str) -> float:
    """
    Avalia um estado de Othello pelo ponto de vista do jogador dado.
    Retorna a diferenca entre o numero de pecas do jogador e do oponente.
    :param state: estado a avaliar (GameState)
    :param player: jogador para avaliar o estado (B ou W)
    """
    board = state.board
    opponent = 'W' if player == 'B' else 'B'
    return board.num_pieces(player) - board.num_pieces(opponent)
