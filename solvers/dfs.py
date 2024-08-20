from main import CubeState

fans=[[]]
def dfs(cube:CubeState,depth=0,ans=[]):

    if cube.is_goal_state():
        fans[0]=ans
        cube.print_cube()
        print(ans)
        return True
    if depth>5:
        return False

    for move in cube.get_possible_moves():

        cube.apply_move(move)
        if dfs(cube,depth+1,ans+[move]):
            return True
        cube.apply_move(cube.inversion(move))
# Example usage
cube = CubeState()
cube.apply_move('D')

dfs(cube)







