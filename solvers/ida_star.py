import heapq
from typing import List, Tuple, Dict, Any
from main import CubeState

class CornerPatternDatabase:
    def from_file(self, file_name: str):
        # Load the pattern database from file
        pass

    def get_num_moves(self, cube: CubeState) -> int:
        # Return the heuristic estimate of moves to solve the cube
        pass

class IDAstarSolver:
    def __init__(self, rubiks_cube: CubeState, file_name: str):
        self.rubiks_cube = rubiks_cube
        #self.corner_db = CornerPatternDatabase()
        #self.corner_db.from_file(file_name)
        self.moves = []
        self.move_done = {}
        self.visited: Dict[CubeState, bool] = {}

    class Node:
        def __init__(self, cube: CubeState, depth: int, estimate: int):
            self.cube = cube.copy()  # Ensure we use a copy of the cube
            self.depth = depth
            self.estimate = estimate


        def __lt__(self, other: 'IDAstarSolver.Node') -> bool:
            # Define the comparison for priority queue
            return (self.depth + self.estimate) < (other.depth + other.estimate)

    def reset_structure(self):
        self.moves.clear()
        self.move_done.clear()
        self.visited.clear()

    def ida_star(self, bound: int) -> Tuple[CubeState, int]:
        priority_queue = []
        start_node = self.Node(self.rubiks_cube, 0, 0)#self.corner_db.get_num_moves(self.rubiks_cube))
        heapq.heappush(priority_queue, (0,0,start_node))
        next_bound = float('inf')

        x=1
        while priority_queue:

            temp=len(priority_queue)
            #print("in prority queue loop is lenghts is ", temp)

            for _ in range(temp):
                node_tuple = heapq.heappop(priority_queue)
                node: IDAstarSolver.Node = node_tuple[2]  # Explicitly specifying the type
                m = node_tuple[1]
                #print("popped",node.cube.hash_state())
                if node.cube.hash_state() in self.visited:
                    continue
                #print(node.cube.hash_state()=="WWWWWWWWWYYYYYYBBBBBBBBBGGGGGGGGGRRRRRRRRRYYYOOOOOOOOO")

                self.visited[node.cube.hash_state()] = True
                self.move_done[node.cube.hash_state()] = m
                if node.cube.is_goal_state():

                    return node.cube,bound

                node.depth += 1
                #print(type(node.cube))
                # print("for loop before")
                # print(node.cube.hash_state())
                for curr_move in node.cube.get_possible_moves():
                    #print(curr_move, node.cube.hash_state())
                    node.cube.apply_move(curr_move)

                    #print(curr_move,node.cube.hash_state())
                    #print(curr_move)
                    #print("node not in visited",node.cube.hash_state() not in self.visited)
                    if node.cube.hash_state() not in self.visited:

                        node.estimate = 0#self.corner_db.get_num_moves(node.cube)
                        if node.estimate + node.depth > bound:
                            #print("increasing bound")
                            next_bound = min(next_bound, node.estimate + node.depth)
                        else:
                            #print("adding to heap",node.estimate + node.depth , bound)
                            heapq.heappush(priority_queue, (node.estimate + node.depth, curr_move,self.Node(node.cube, node.depth, node.estimate)))
                    node.cube.apply_move(node.cube.inversion(curr_move))

                #print("for loop ended")
            x+=1
        #print("bound and next_bound is ",bound,next_bound)
        return self.rubiks_cube, next_bound

    def solve(self) :
        bound = 2
        solved_cube, new_bound = self.ida_star(bound)
        #print("solved cube is ",solved_cube.hash_state())
        while bound<7 and  new_bound != bound:
            #print("startting bound is in while loop",bound)
            #print(bound)
            self.reset_structure()
            bound = new_bound
            #print('a',bound)

            solved_cube, new_bound = self.ida_star(bound)

            #print("afeter solving uding bound",bound,new_bound)
        print('solved cube is')
        solved_cube.print_cube()
        assert solved_cube.is_goal_state()
        #print(self.move_done)
        curr_cube = solved_cube
        #print(curr_cube.hash_state(),curr_cube.hash_state() in self.move_done,self.move_done[curr_cube.hash_state()])

        #print()
        #print(self.move_done)
        while  curr_cube.hash_state()!=self.rubiks_cube.hash_state() :
            #print( curr_cube.hash_state())
            curr_move = self.move_done[curr_cube.hash_state()]
            #print(curr_move,curr_cube.inversion(curr_move))
            self.moves.append(curr_move)
            #print(curr_move)
            curr_cube.apply_move( curr_cube.inversion(curr_move))
            #print(curr_cube.hash_state())


        self.rubiks_cube = solved_cube
        self.moves.reverse()
        return self.moves
cube=CubeState()
cube.random_shuffle(5)
#print("start")
print("unsolved cube is")
cube.print_cube()


obj=IDAstarSolver(cube,'a')

ans=obj.solve()

print("moves shoule be ",ans)
#WWWWWWWWWYYYYYYBBBBBBBBBGGGGGGGGGRRRRRRRRRYYYOOOOOOOOO
