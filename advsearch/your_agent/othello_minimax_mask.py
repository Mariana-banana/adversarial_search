from typing import Tuple
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

# mask template adjusted from https://web.fe.up.pt/~eol/IA/MIA0203/trabalhos/Damas_Othelo/Docs/Eval.html
# could optimize for symmetries but just put all values here for coding speed :P
# DO NOT CHANGE!
EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

# Profundidade fixa calibrada para caber nos 5s da maquina do torneio (Passo 7).
# Medido: ~0,72s @ prof 5 no Mac; com fator ~4x da maquina de referencia -> ~2,9s (margem ok).
MASK_MAX_DEPTH = 5


def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado dado, usando minimax com poda alfa-beta
    e a heuristica posicional (valor das casas pela EVAL_TEMPLATE).
    :param state: estado para fazer a jogada
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return minimax_move(state, MASK_MAX_DEPTH, evaluate_mask)


def evaluate_mask(state, player: str) -> float:
    """
    Avalia um estado de Othello pelo ponto de vista do jogador dado, usando o valor
    posicional das pecas: soma os valores (EVAL_TEMPLATE) das casas ocupadas pelo
    jogador e subtrai os das casas ocupadas pelo oponente.
    :param state: estado a avaliar (GameState)
    :param player: jogador para avaliar o estado (B ou W)
    """
    tiles = state.board.tiles
    opponent = 'W' if player == 'B' else 'B'
    score = 0
    for y in range(8):              # y = linha
        for x in range(8):          # x = coluna
            piece = tiles[y][x]
            if piece == player:
                score += EVAL_TEMPLATE[y][x]
            elif piece == opponent:
                score -= EVAL_TEMPLATE[y][x]
    return score
