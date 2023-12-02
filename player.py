class Player:
    def __init__(self, color):
        self.color = color
        self.points = 0

    def addPoints(self, points):
        self.points += points

    def isWinner(self):
        return self.points >= 2
            
    def __str__(self):
        return f"{self.color} Player - Points: {self.points}"