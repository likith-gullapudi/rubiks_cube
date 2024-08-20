from cube_state import CubeState
from move import Move
from collections import deque

def bfs_solve(initial_state: CubeState) -> list:
    queue = deque([initial_state])
    visited = set()

    while queue:
        current_state = queue.popleft()

        if current_state.is_goal_state():
            # Return the sequence of moves to solve the cube
            pass

        for move in current_state.get_possible_moves():
            next_state = current_state.apply_move(move)
            state_hash = next_state.hash_state()

            if state_hash not in visited:
                visited.add(state_hash)
                queue.append(next_state)

    return []

def dfs_solve(initial_state: CubeState, max_depth: int) -> list:
    def dfs(state, depth):
        if depth > max_depth:
            return None
        if state.is_goal_state():
            return []  # Return empty move list, indicating solved

        for move in state.get_possible_moves():
            next_state = state.apply_move(move)
            result = dfs(next_state, depth + 1)
            if result is not None:
                return [move] + result

        return None

    return dfs(initial_state, 0) or []
