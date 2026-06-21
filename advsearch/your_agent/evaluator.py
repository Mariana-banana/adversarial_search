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

    # Weights configuration
    weights = {
        "corner_control": 1000.0,
        "corner_closeness": 300.0,
        "mobility": 50.0 if phase != "late" else 20.0,
        "frontier": 20.0 if phase != "late" else 5.0,
        "stability": 200.0,
        "coin_parity": -5.0 if phase == "early" else (5.0 if phase == "mid" else 100.0), # Evaporation built-in if early
        "region_parity": 50.0 if phase == "late" else 0.0,
        "quiet_moves": 15.0,
        "edge_configurations": 100.0,
        "evaporation": 10.0 if phase == "early" else 0.0
    }

    my_pieces = []
    opp_pieces = []
    empty_squares = set()
    
    for y in range(8):
        for x in range(8):
            p = board.tiles[y][x]
            if p == player:
                my_pieces.append((x, y))
            elif p == opponent:
                opp_pieces.append((x, y))
            else:
                empty_squares.add((x, y))

    if "corner_control" in active_strategies:
        my_corners = sum(1 for c in CORNERS if board.tiles[c[1]][c[0]] == player)
        opp_corners = sum(1 for c in CORNERS if board.tiles[c[1]][c[0]] == opponent)
        score += weights["corner_control"] * (my_corners - opp_corners)

    if "corner_closeness" in active_strategies:
        my_bad = 0
        opp_bad = 0
        for corner, xs in X_SQUARES.items():
            cx, cy = corner
            if board.tiles[cy][cx] == '.': # Corner is empty
                for xx, xy in xs:
                    if board.tiles[xy][xx] == player: my_bad += 1
                    if board.tiles[xy][xx] == opponent: opp_bad += 1
        for corner, cs in C_SQUARES.items():
            cx, cy = corner
            if board.tiles[cy][cx] == '.': # Corner is empty
                for cx_sq, cy_sq in cs:
                    if board.tiles[cy_sq][cx_sq] == player: my_bad += 1
                    if board.tiles[cy_sq][cx_sq] == opponent: opp_bad += 1
        score -= weights["corner_closeness"] * (my_bad - opp_bad)

    if "mobility" in active_strategies:
        my_moves = len(state.legal_moves()) if state.player == player else 0
        # To get opponent moves, we need to create a hypothetical state where it's their turn
        opp_state = GameState(board, opponent)
        opp_moves = len(opp_state.legal_moves())
        # If it's currently player's turn, we know my_moves precisely.
        # But we approximate opponent's mobility
        score += weights["mobility"] * (my_moves - opp_moves)

    # Frontier Discs
    if "frontier" in active_strategies or "quiet_moves" in active_strategies:
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

        if "frontier" in active_strategies:
            score -= weights["frontier"] * (my_frontier - opp_frontier)
            
        if "quiet_moves" in active_strategies:
            my_internal = len(my_pieces) - my_frontier
            opp_internal = len(opp_pieces) - opp_frontier
            score += weights["quiet_moves"] * (my_internal - opp_internal)

    if "coin_parity" in active_strategies:
        score += weights["coin_parity"] * (len(my_pieces) - len(opp_pieces))
        
    if "evaporation" in active_strategies:
        # Just heavily penalize having pieces in the early game
        score -= weights["evaporation"] * len(my_pieces)

    if "stability" in active_strategies:
        # Simple stability: pieces on edges that are connected to a corner of the same color
        my_stable = 0
        opp_stable = 0
        
        # Check horizontal edges (y=0, y=7)
        for y in [0, 7]:
            for dx in [1, -1]:
                start_x = 0 if dx == 1 else 7
                if board.tiles[y][start_x] == player:
                    x = start_x + dx
                    while 0 <= x < 8 and board.tiles[y][x] == player:
                        my_stable += 1
                        x += dx
                if board.tiles[y][start_x] == opponent:
                    x = start_x + dx
                    while 0 <= x < 8 and board.tiles[y][x] == opponent:
                        opp_stable += 1
                        x += dx
                        
        # Check vertical edges (x=0, x=7)
        for x in [0, 7]:
            for dy in [1, -1]:
                start_y = 0 if dy == 1 else 7
                if board.tiles[start_y][x] == player:
                    y = start_y + dy
                    while 0 <= y < 8 and board.tiles[y][x] == player:
                        my_stable += 1
                        y += dy
                if board.tiles[start_y][x] == opponent:
                    y = start_y + dy
                    while 0 <= y < 8 and board.tiles[y][x] == opponent:
                        opp_stable += 1
                        y += dy
                        
        score += weights["stability"] * (my_stable - opp_stable)

    if "edge_configurations" in active_strategies:
        my_bad_edges = 0
        opp_bad_edges = 0
        
        edges = [
            [(x, 0) for x in range(8)],
            [(x, 7) for x in range(8)],
            [(0, y) for y in range(8)],
            [(7, y) for y in range(8)]
        ]
        
        for edge in edges:
            my_count = sum(1 for px, py in edge[1:7] if board.tiles[py][px] == player)
            opp_count = sum(1 for px, py in edge[1:7] if board.tiles[py][px] == opponent)
            c1_empty = board.tiles[edge[0][1]][edge[0][0]] == '.'
            c2_empty = board.tiles[edge[7][1]][edge[7][0]] == '.'
            
            if (c1_empty or c2_empty):
                if my_count == 5 or my_count == 6: my_bad_edges += 1
                if opp_count == 5 or opp_count == 6: opp_bad_edges += 1
                
        score -= weights["edge_configurations"] * (my_bad_edges - opp_bad_edges)

    if "region_parity" in active_strategies and phase == "late":
        # Simplified: if the number of empty squares is odd, it's a slight advantage to the current player
        # A true implementation would find connected components and count odd regions.
        visited = set()
        odd_regions = 0
        
        for ex, ey in empty_squares:
            if (ex, ey) not in visited:
                # BFS
                region_size = 0
                queue = [(ex, ey)]
                visited.add((ex, ey))
                while queue:
                    cx, cy = queue.pop(0)
                    region_size += 1
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in empty_squares and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                if region_size % 2 != 0:
                    odd_regions += 1
                    
        # If I am the player to move, an odd region parity means I likely get the last move in that region
        if state.player == player:
            score += weights["region_parity"] * odd_regions
        else:
            score -= weights["region_parity"] * odd_regions

    return score
