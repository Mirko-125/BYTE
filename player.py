class Player:
    def __init__(self, color):
        self.color = color
        self.points = 0

    def addPoints(self, points):
        self.points += points

    def isWinner(self):
        return self.points >= 2
<<<<<<< HEAD
            
=======

>>>>>>> 6a521bf92c99067409a7bbcd8b702af45c814f3e
    def __str__(self):
        return f"{self.color} Player - Points: {self.points}"