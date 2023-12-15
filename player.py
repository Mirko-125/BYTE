class Player:
    def __init__(self, color):
        self.color = color
        self.points = 0

    def addPoints(self, points):
        self.points += points

    def isWinner(self, n):
        #8-2
        #10-3
        #16-5
        if n == 8:
            return self.points >= 2
        elif n == 10:
            return self.points >= 3
        elif n == 16:
            return self.points >= 5
    def __str__(self):
        return f"{self.color} Player - Points: {self.points}"