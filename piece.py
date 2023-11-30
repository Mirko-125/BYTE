class Piece:
    def __init__(self, color):
        if color in {"White", "Black"}:
            self.color = color
        else:
            raise ValueError("Invalid color. Must be 'Black' or 'White'.")