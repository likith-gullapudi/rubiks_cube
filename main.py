import copy
import random



from enum import Enum

class FACE(Enum):
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5


class COLOR(Enum):
    WHITE =0
    GREEN = 1
    RED    = 2
    BLUE   = 3
    ORANGE= 4
    YELLOW= 5


class CubeState:
    def __init__(self, state=None, through_hash=False):
        if through_hash and state:
            color_map = {
                'W': COLOR.WHITE,
                'G': COLOR.GREEN,
                'R': COLOR.RED,
                'B': COLOR.BLUE,
                'O': COLOR.ORANGE,
                'Y': COLOR.YELLOW
            }
            # Assuming the state string is in the format:
            # WWWWWWWWWYYYYYYYYYBBBBBBBBBGGGGGGGGGRRRRRRRRROOOOOOOOO
            self.state = [
                [[color_map[state[i]] for i in range(0, 9)]],    # WHITE face
                [[color_map[state[i]] for i in range(9, 18)]],   # YELLOW face
                [[color_map[state[i]] for i in range(18, 27)]],  # BLUE face
                [[color_map[state[i]] for i in range(27, 36)]],  # GREEN face
                [[color_map[state[i]] for i in range(36, 45)]],  # RED face
                [[color_map[state[i]] for i in range(45, 54)]]   # ORANGE face
            ]
            # Convert each face from a flat list to a 3x3 grid
            for i in range(6):
                self.state[i] = [self.state[i][0][j:j + 3] for j in range(0, 9, 3)]
        elif state and not through_hash:
            self.state = state
        else:
            # Initialize solved cube state
            self.state = [
                [[COLOR.WHITE] * 3 for _ in range(3)],   # WHITE face
                [[COLOR.YELLOW] * 3 for _ in range(3)],  # YELLOW face
                [[COLOR.BLUE] * 3 for _ in range(3)],    # BLUE face
                [[COLOR.GREEN] * 3 for _ in range(3)],   # GREEN face
                [[COLOR.RED] * 3 for _ in range(3)],     # RED face
                [[COLOR.ORANGE] * 3 for _ in range(3)]   # ORANGE face
            ]

    def inversion(self,move):
        move_inversion = {
            "U": "U'",
            "U'": "U",
            "U2": "U2",
            "L": "L'",
            "L'": "L",
            "L2": "L2",
            "F": "F'",
            "F'": "F",
            "F2": "F2",
            "R": "R'",
            "R'": "R",
            "R2": "R2",
            "B": "B'",
            "B'": "B",
            "B2": "B2",
            "D": "D'",
            "D'": "D",
            "D2": "D2",
        }
        return move_inversion[move]

    def get_color_letter(self, color):
        return color.name[0]

    def is_goal_state(self) -> bool:
        for face in self.state:
            color = face[0][0]
            if any(color != face[i][j] for i in range(3) for j in range(3)):
                return False
        return True

    def get_possible_moves(self) -> list:

        return ["L", "L'", "L2", "R", "R'", "R2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]

    def apply_move(self, move):
        # Helper method to rotate a face clockwise
        def rotate_face( ind):
            temp_arr = [[None] * 3 for _ in range(3)]

            # Copy the current face to temp_arr
            for i in range(3):
                for j in range(3):
                    temp_arr[i][j] = self.state[ind][i][j]

            # Rotate the face in place
            for i in range(3):
                self.state[ind][0][i] = temp_arr[2 - i][0]
            for i in range(3):
                self.state[ind][i][2] = temp_arr[0][i]
            for i in range(3):
                self.state[ind][2][2 - i] = temp_arr[i][2]
            for i in range(3):
                self.state[ind][2 - i][0] = temp_arr[2][2 - i]

        if move == "U":
            # Rotate the UP face
            rotate_face(0)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[4][0][2 - i]  # BACK face

            for i in range(3):
                self.state[4][0][2 - i] = self.state[1][0][2 - i]  # LEFT face

            for i in range(3):
                self.state[1][0][2 - i] = self.state[2][0][2 - i]  # FRONT face

            for i in range(3):
                self.state[2][0][2 - i] = self.state[3][0][2 - i]  # RIGHT face

            for i in range(3):
                self.state[3][0][2 - i] = temp_arr[i]  # BACK face
        elif move == "U'":
            self.apply_move("U")
            self.apply_move("U")
            self.apply_move("U")
        elif move == "U2":
            self.apply_move("U")
            self.apply_move("U")

        elif move == "L":
            rotate_face(1)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[0][i][0]  # UP face

            for i in range(3):
                self.state[0][i][0] = self.state[4][2 - i][2]  # BACK face

            for i in range(3):
                self.state[4][2 - i][2] = self.state[5][i][0]  # DOWN face

            for i in range(3):
                self.state[5][i][0] = self.state[2][i][0]  # FRONT face

            for i in range(3):
                self.state[2][i][0] = temp_arr[i]
        elif move == "L'":
            self.apply_move("L")
            self.apply_move("L")
            self.apply_move("L")
        elif move == "L2":
            self.apply_move("L")
            self.apply_move("L")

        elif move == "F":
            rotate_face(2)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[0][2][i]  # UP face

            for i in range(3):
                self.state[0][2][i] = self.state[1][2 - i][2]  # LEFT face

            for i in range(3):
                self.state[1][2 - i][2] = self.state[5][0][2 - i]  # DOWN face

            for i in range(3):
                self.state[5][0][2 - i] = self.state[3][i][0]  # BACK face

            for i in range(3):
                self.state[3][i][0] = temp_arr[i]  # UP face
        elif move=="F'":
            self.apply_move("F")
            self.apply_move("F")
            self.apply_move("F")
        elif move == "F2'":
            self.apply_move("F")
            self.apply_move("F")
        elif move=="R":
            rotate_face(3)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[0][2 - i][2]  # UP face

            for i in range(3):
                self.state[0][2 - i][2] = self.state[2][2 - i][2]  # FRONT face

            for i in range(3):
                self.state[2][2 - i][2] = self.state[5][2 - i][2]  # DOWN face

            for i in range(3):
                self.state[5][2 - i][2] = self.state[4][i][0]  # BACK face

            for i in range(3):
                self.state[4][i][0] = temp_arr[i]
        elif move=="R'":
            self.apply_move("R")
            self.apply_move("R")
            self.apply_move("R")
        elif move == "R2":
            self.apply_move("R")
            self.apply_move("R")

        elif move == "B":
            rotate_face(4)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[0][0][2 - i]  # UP face

            for i in range(3):
                self.state[0][0][2 - i] = self.state[3][2 - i][2]  # LEFT face

            for i in range(3):
                self.state[3][2 - i][2] = self.state[5][2][i]  # DOWN face

            for i in range(3):
                self.state[5][2][i] = self.state[1][i][0]  # FRONT face

            for i in range(3):
                self.state[1][i][0] = temp_arr[i]  # UP face
        elif move == "B'":
            self.apply_move("B")
            self.apply_move("B")
            self.apply_move("B")
        elif move == "B2":
            self.apply_move("B")
            self.apply_move("B")

        elif move == "D":
            rotate_face(5)

            temp_arr = [None] * 3
            for i in range(3):
                temp_arr[i] = self.state[2][2][i]  # DOWN face

            for i in range(3):
                self.state[2][2][i] = self.state[1][2][i]  # FRONT face

            for i in range(3):
                self.state[1][2][i] = self.state[4][2][i]  # UP face

            for i in range(3):
                self.state[4][2][i] = self.state[3][2][i]  # BACK face

            for i in range(3):
                self.state[3][2][i] = temp_arr[i]  # DOWN face
        elif move == "D'":
            self.apply_move("D")
            self.apply_move("D")
            self.apply_move("D")
        elif move == "D2":
            self.apply_move("D")
            self.apply_move("D")

        return self

    def hash_state(self) -> str:
        # Convert each face of the cube into a string
        # self.state is a list of faces, each face is a 2D list of colors
        return ''.join(''.join(c.name[0] for c in row) for face in self.state for row in face)

    def is_valid(self) -> bool:
        color_count = {color: 0 for color in COLOR}
        for face in self.state:
            for row in face:
                for color in row:
                    if color in color_count:
                        color_count[color] += 1
                    else:
                        return False
        return all(count == 9 for count in color_count.values())

    def print_cube(self):
        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[0][0]))
        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[0][1]))
        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[0][2]))

        print()

        for row in range(3):
            print(" ".join(self.get_color_letter(self.state[0][row][col]) for col in range(3)), end=" " * 3)
            print(" ".join(self.get_color_letter(self.state[1][row][col]) for col in range(3)), end=" " * 3)
            print(" ".join(self.get_color_letter(self.state[2][row][col]) for col in range(3)), end=" " * 3)
            print(" ".join(self.get_color_letter(self.state[3][row][col]) for col in range(3)))

        print()

        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[5][0]))
        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[5][1]))
        print(" " * 8 + " ".join(self.get_color_letter(col) for col in self.state[5][2]))
    def random_shuffle(self,moves):
        test=[]
        possible_moves=self.get_possible_moves()
        for i in range(moves):

            temp=random.randint(0,17)
            test.append(possible_moves[temp])
            print(possible_moves[temp])
            self.apply_move(possible_moves[temp])
        return test

    def copy(self) -> 'CubeState':
        # Create a deep copy of the CubeState instance
        new_instance = copy.deepcopy(self)
        return new_instance



