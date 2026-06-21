import random
from typing import Tuple, Callable
import math



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                      This function should take a GameState object and a string identifying the player,
                      and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    best_move = None
    
    # O root_player é o "dono" da árvore de busca. Queremos sempre maximizar a pontuação
    # do ponto de vista DESTE jogador, independentemente de quem está jogando lá embaixo na árvore.
    root_player = state.player

    def alpha_beta(current_state, depth, alpha, beta, maximizing_player):
        # Condição de parada: chegamos ao fim do jogo OU esgotamos a profundidade máxima permitida.
        if depth == 0 or current_state.is_terminal():
            # A função de avaliação SEMPRE deve olhar pelo ponto de vista do root_player
            return eval_func(current_state, root_player)

        # Pegamos todas as jogadas possíveis para o jogador da vez (neste estado)
        moves = current_state.legal_moves()

        if maximizing_player:
            # Se for o nosso turno (ou de quem queremos maximizar), o objetivo é encontrar 
            # o MAIOR valor possível. Começamos com -infinito (o pior possível).
            value = -math.inf
            for move in moves:
                # Simula a jogada e cria um universo paralelo (next_st)
                next_st = current_state.next_state(move)
                
                # Descobre de quem é a vez no próximo universo. Se o oponente não tiver jogadas válidas,
                # a vez pode voltar para nós! (Comum no Othello)
                is_max = (next_st.player == root_player)
                
                # Chamada recursiva descendo um nível na árvore
                # Se depth == -1 (ilimitado), passamos -1 novamente para não cair na condição depth == 0
                new_depth = - 1 if depth == -1 else depth - 1
                value = max(value, alpha_beta(next_st, new_depth, alpha, beta, is_max))
                
                # Atualiza o Alpha. Alpha é o "pior cenário aceitável" para o maximizador.
                # Como encontramos um `value`, garantimos que daqui para frente, se alguém nos
                # oferecer menos que `alpha`, nós ignoramos.
                alpha = max(alpha, value)
                
                # PODA ALPHA-BETA: Se o nosso alpha (lucro garantido) for maior ou igual ao beta 
                # (o limite do que o adversário vai permitir), não precisamos olhar as outras jogadas 
                # deste galho. O adversário NUNCA vai deixar chegarmos aqui de qualquer forma.
                if alpha >= beta:
                    break
            return value
        else:
            # Turno do Oponente (minimizador). Ele quer o nosso MAL, então ele vai buscar
            # a jogada que retorne o MENOR valor possível para nós.
            value = math.inf
            for move in moves:
                next_st = current_state.next_state(move)
                is_max = (next_st.player == root_player)
                
                new_depth = - 1 if depth == -1 else depth - 1
                value = min(value, alpha_beta(next_st, new_depth, alpha, beta, is_max))
                
                # Atualiza o Beta. Beta é o máximo que o minimizador vai "permitir" que a gente ganhe.
                beta = min(beta, value)
                
                # PODA ALPHA-BETA: Se o minimizador já achou uma jogada que deixa nossa pontuação 
                # menor que o nosso Alpha (nosso lucro mínimo garantido em outro galho), ele com 
                # certeza escolherá essa jogada ou uma pior ainda. Logo, nós (root) nunca
                # entraremos neste galho principal, então paramos de avaliar o resto.
                if beta <= alpha:
                    break
            return value

    # A busca principal começa aqui! Como nós (root_player) somos o maximizador original,
    # inicializamos buscando bater -infinito.
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf

    # Avaliamos cada jogada da raiz
    for move in state.legal_moves():
        next_st = state.next_state(move)
        is_max = (next_st.player == root_player)
        
        new_depth = max_depth - 1 if max_depth != -1 else -1
        value = alpha_beta(next_st, new_depth, alpha, beta, is_max)
        
        # Se encontramos uma jogada com pontuação maior que a melhor que já tínhamos visto,
        # anotamos ela como a nossa nova "melhor jogada oficial"
        if value > best_value or best_move is None:
            best_value = value
            best_move = move
            
        # O alpha da raiz é atualizado para passar pros próximos galhos a informação de que
        # "Eu já garanti X pontos. Se você for me dar menos que X, nem perca tempo calculando."
        alpha = max(alpha, value)

    return best_move
