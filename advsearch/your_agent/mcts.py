import time
import math
import random
from typing import Tuple

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0.0
        self.visits = 0
        self.untried_moves = list(state.legal_moves()) if state.player is not None else []
        
    def ucb1(self, c=1.414):
        if self.visits == 0:
            return math.inf
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def make_move(state) -> Tuple[int, int]:
    """
    Retorna uma jogada usando Monte Carlo Tree Search (MCTS) com UCB1.
    Roda simulacoes pelo tempo disponivel (4.5s) e devolve a melhor jogada.
    """
    time_limit = 4.5
    deadline = time.time() + time_limit
    
    legal_moves = list(state.legal_moves())
    if not legal_moves:
        return (-1, -1)
        
    # Se so tem uma jogada, a faz
    if len(legal_moves) == 1:
        return legal_moves[0]
        
    root = MCTSNode(state)
    
    while time.time() < deadline:
        node = root
        
        # Selection
        while not node.untried_moves and node.children:
            node = max(node.children, key=lambda c: c.ucb1())
            
        # Expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            next_state = node.state.next_state(move)
            child = MCTSNode(next_state, parent=node, move=move)
            node.children.append(child)
            node = child
            
        # Simulation (Rollout)
        current_rollout_state = node.state
        while not current_rollout_state.is_terminal():
            moves = list(current_rollout_state.legal_moves())
            if not moves:
                break
                
            # Rollout pseudo-aleatorio: evita jogar nas casas adjacentes as quinas (X e C) se possivel
            bad_squares = [(1,1), (1,6), (6,1), (6,6), (0,1), (1,0), (0,6), (1,7), (6,0), (7,1), (6,7), (7,6)]
            safe_moves = [m for m in moves if m not in bad_squares]
            
            if safe_moves:
                move = random.choice(safe_moves)
            else:
                move = random.choice(moves)
                
            current_rollout_state = current_rollout_state.next_state(move)
            
        # Backpropagation
        winner = current_rollout_state.winner()
        temp_node = node
        while temp_node is not None:
            temp_node.visits += 1
            if winner is None:
                temp_node.wins += 0.5
            elif temp_node.parent is not None and winner == temp_node.parent.state.player:
                # O pai do no avaliado foi quem fez a jogada que ganhou
                temp_node.wins += 1.0
            temp_node = temp_node.parent

    # Escolhe o filho mais visitado na raiz
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move
