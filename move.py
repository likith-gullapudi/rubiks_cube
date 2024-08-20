class Move:
    def __init__(self, move_type, face, direction):
        self.move_type = move_type  # e.g., rotate, flip
        self.face = face  # e.g., U, D, L, R, F, B
        self.direction = direction  # e.g., clockwise, counterclockwise

    def __repr__(self):
        return f"{self.move_type} {self.face} {self.direction}"
