from piece import Piece

class Stack:
    def __init__(self, element):
        self.x = 0
        self.y = 0
        self.max = 7
        self.list = [element] if element else []

    def add(self, elements: list):
        combinedLength = len(self.list) + len(elements)
        if combinedLength > 8:
            return "Unable to overexceed 8 elements"
        elif combinedLength == 8:
            finalElement = self.list.pop()
            self.list.clear()
            return finalElement
        else:
            self.list.extend(elements)
        return 0

    def isEmpty(self):
        return len(self.list == 0)
    
    def pop(self, count):
        return [self.list.pop() for _ in range(count)]

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.list)
