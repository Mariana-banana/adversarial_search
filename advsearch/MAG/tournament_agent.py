from typing import Tuple
from .minimax import iterative_deepening_move
from .othello_minimax_custom import evaluate_custom

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# Orcamento de tempo abaixo dos 5s para deixar margem (overhead do servidor / comunicacao).
TIME_LIMIT = 4.5


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o torneio de Othello, usando a melhor implementacao do grupo:
    minimax com poda alfa-beta + aprofundamento iterativo limitado por tempo, guiado pela
    heuristica customizada (10 estrategias com pesos por fase + tratamento de terminal).

    O aprofundamento iterativo garante que sempre devolvemos uma jogada dentro do tempo
    (nunca desclassifica) e usa toda a profundidade que a maquina permitir.

    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada; (-1, -1) se nao houver jogada legal
    """
    return iterative_deepening_move(state, evaluate_custom, time_limit=TIME_LIMIT)
