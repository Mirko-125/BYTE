class Player:
    def __init__(self, color):
        self.color = color
        self.points = 0

    def add_points(self, points):
        self.points += points

    def __str__(self):
        return f"{self.color} Player - Points: {self.points}"