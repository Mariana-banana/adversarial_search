from typing import Tuple
from .minimax import iterative_deepening_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# Orcamento de tempo por jogada para o mini-torneio do relatorio (bem abaixo dos 5s).
TIME_LIMIT = 2.0


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado dado, usando minimax com poda alfa-beta e
    aprofundamento iterativo limitado por tempo, com a heuristica de contagem de pecas.
    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return iterative_deepening_move(state, evaluate_count, time_limit=TIME_LIMIT)


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
