from advsearch.othello.gamestate import GameState
from advsearch.othello.board import Board

CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
X_SQUARES = {
    (0, 0): [(1, 1)],
    (0, 7): [(1, 6)],
    (7, 0): [(6, 1)],
    (7, 7): [(6, 6)]
}
C_SQUARES = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 7): [(0, 6), (1, 7)],
    (7, 0): [(6, 0), (7, 1)],
    (7, 7): [(6, 7), (7, 6)]
}

def get_opponent(player: str) -> str:
    return 'W' if player == 'B' else 'B'

def evaluate_state(state: GameState, player: str, active_strategies: set) -> float:
    board = state.board
    opponent = get_opponent(player)
    
    empty_count = board.num_pieces('.')
    total_squares = 64
    phase = "early"
    if empty_count <= 20:
        phase = "late"
    elif empty_count <= 44:
        phase = "mid"
        
    score = 0.0

    weights = {
        "corner_control": 1000.0,
        "corner_closeness": 150.0,
        "mobility": 100.0 if phase != "late" else 30.0,
        "frontier": 30.0 if phase != "late" else 5.0,
        "coin_parity": -10.0 if phase == "early" else (5.0 if phase == "mid" else 150.0),
    }

    my_pieces = []
    opp_pieces = []
    
    for y in range(8):
        for x in range(8):
            p = board.tiles[y][x]
            if p == player:
                my_pieces.append((x, y))
            elif p == opponent:
                opp_pieces.append((x, y))

    if "corner_control" in active_strategies:
        my_corners = sum(1 for c in CORNERS if board.tiles[c[1]][c[0]] == player)
        opp_corners = sum(1 for c in CORNERS if board.tiles[c[1]][c[0]] == opponent)
        score += weights["corner_control"] * (my_corners - opp_corners)

    if "corner_closeness" in active_strategies:
        my_bad = 0
        opp_bad = 0
        for corner, xs in X_SQUARES.items():
            cx, cy = corner
            if board.tiles[cy][cx] == '.':
                for xx, xy in xs:
                    if board.tiles[xy][xx] == player: my_bad += 1
                    if board.tiles[xy][xx] == opponent: opp_bad += 1
        for corner, cs in C_SQUARES.items():
            cx, cy = corner
            if board.tiles[cy][cx] == '.':
                for cx_sq, cy_sq in cs:
                    if board.tiles[cy_sq][cx_sq] == player: my_bad += 1
                    if board.tiles[cy_sq][cx_sq] == opponent: opp_bad += 1
        score -= weights["corner_closeness"] * (my_bad - opp_bad)

    if "mobility" in active_strategies:
        my_state = state if state.player == player else GameState(board, player)
        opp_state = state if state.player == opponent else GameState(board, opponent)
        my_moves = len(my_state.legal_moves())
        opp_moves = len(opp_state.legal_moves())
        score += weights["mobility"] * (my_moves - opp_moves)

    if "frontier" in active_strategies:
        my_frontier = 0
        opp_frontier = 0
        
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for px, py in my_pieces:
            is_frontier = False
            for dx, dy in directions:
                nx, ny = px + dx, py + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and board.tiles[ny][nx] == '.':
                    is_frontier = True
                    break
            if is_frontier: my_frontier += 1
            
        for px, py in opp_pieces:
            is_frontier = False
            for dx, dy in directions:
                nx, ny = px + dx, py + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and board.tiles[ny][nx] == '.':
                    is_frontier = True
                    break
            if is_frontier: opp_frontier += 1

        score -= weights["frontier"] * (my_frontier - opp_frontier)

    if "coin_parity" in active_strategies:
        score += weights["coin_parity"] * (len(my_pieces) - len(opp_pieces))
        
    return score
