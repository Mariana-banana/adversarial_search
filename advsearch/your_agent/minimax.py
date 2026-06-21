import math
import time
from typing import Tuple, Callable


def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Retorna a jogada escolhida pelo minimax com poda alfa-beta para o estado dado.
    Implementacao independente do jogo (usa apenas a interface de GameState).

    :param state: estado atual (GameState)
    :param max_depth: profundidade maxima de busca. -1 = ilimitada (vai ate estados terminais)
    :param eval_func: funcao de avaliacao. Recebe (estado, jogador) e retorna float.
                      E' chamada em estados terminais ou ao atingir max_depth.
    :return: tupla (x, y) = (coluna, linha) da jogada
    """
    return _search_root(state, max_depth, eval_func, deadline=None)


def iterative_deepening_move(state, eval_func: Callable,
                             time_limit: float = 4.8,
                             max_depth_cap: int = 64) -> Tuple[int, int]:
    """
    Aprofundamento iterativo limitado por tempo (para o Othello/torneio respeitar os 5s).
    Busca profundidade 1, 2, 3, ... e guarda sempre a melhor jogada da ultima
    profundidade COMPLETADA antes do tempo acabar. Se o tempo estoura no meio de uma
    profundidade, descarta o resultado parcial e mantem o da profundidade anterior.

    :param time_limit: tempo maximo de busca em segundos (margem abaixo dos 5s reais)
    :param max_depth_cap: teto de profundidade (64 = profundidade maxima do Othello)
    """
    legal = list(state.legal_moves())
    if not legal:                 # sem jogadas validas: jogador passa a vez
        return (-1, -1)

    deadline = time.time() + time_limit
    best_move = legal[0]
    for depth in range(1, max_depth_cap + 1):
        try:
            move = _search_root(state, depth, eval_func, deadline=deadline)
        except TimeoutError:
            break                 # tempo acabou no meio: fica com a profundidade anterior
        if move is not None:
            best_move = move
        if time.time() >= deadline:
            break
    return best_move


def _search_root(state, max_depth: int, eval_func: Callable, deadline) -> Tuple[int, int]:
    """
    Camada da raiz: escolhe a melhor jogada para o jogador da vez.
    O jogador da raiz e' SEMPRE o maximizador (decidimos a jogada para ele).
    """
    root_player = state.player
    best_move = None
    best_value = -math.inf
    alpha, beta = -math.inf, math.inf

    # truque do -1: se ilimitado, a profundidade dos filhos continua -1 (nunca chega a 0),
    # entao a busca so para em estado terminal.
    child_depth = -1 if max_depth == -1 else max_depth - 1

    for move in state.legal_moves():
        child = state.next_state(move)
        # se o oponente nao tem jogada, a vez pode voltar pra raiz -> filho ainda e' MAX
        is_max = (child.player == root_player)
        value = _alpha_beta(child, child_depth, alpha, beta, is_max, root_player, eval_func, deadline)
        if best_move is None or value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)
    return best_move


def _alpha_beta(state, depth: int, alpha: float, beta: float,
                maximizing: bool, root_player: str, eval_func: Callable, deadline) -> float:
    # corte por tempo (so ativo no aprofundamento iterativo, quando deadline != None)
    if deadline is not None and time.time() >= deadline:
        raise TimeoutError()

    # para em estado terminal OU ao esgotar a profundidade (depth == 0).
    # com depth == -1 (ilimitado) esta condicao so dispara em terminal.
    if depth == 0 or state.is_terminal():
        return eval_func(state, root_player)

    child_depth = -1 if depth == -1 else depth - 1

    if maximizing:
        value = -math.inf
        for move in state.legal_moves():
            child = state.next_state(move)
            is_max = (child.player == root_player)
            value = max(value, _alpha_beta(child, child_depth, alpha, beta, is_max,
                                           root_player, eval_func, deadline))
            alpha = max(alpha, value)
            if alpha >= beta:     # poda: o minimizador acima nunca deixaria chegar aqui
                break
        return value
    else:
        value = math.inf
        for move in state.legal_moves():
            child = state.next_state(move)
            is_max = (child.player == root_player)
            value = min(value, _alpha_beta(child, child_depth, alpha, beta, is_max,
                                           root_player, eval_func, deadline))
            beta = min(beta, value)
            if beta <= alpha:     # poda: o maximizador acima ja garantiu algo melhor
                break
        return value
