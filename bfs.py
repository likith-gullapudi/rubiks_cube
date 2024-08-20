from collections import deque

from main import CubeState


def dfs(cube:CubeState):
    q=deque()
    q.append(cube)
    while q:
        present_state,path=q.popleft()
        if present_state.is_goal_state():
            return path
        for move in cube.get_possible_moves():

            cube.apply_move(move)
            q.append((cube,))
            if dfs(cube, depth + 1, ans + [move]):
                return True
            cube.apply_move(cube.inversion(move))
