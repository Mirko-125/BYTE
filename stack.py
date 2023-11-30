from piece import Piece

class Stack:
    def __init__(self, element):
        self.max = 7
        self.list = [element] if element else []
    def add(self, elements: list):
        combinedLength = len(self.list) + len(elements)
        if combinedLength > 8:
            return "Unable to overexeed 8 elements"
        elif combinedLength == 8:
            self.list.clear()
        else:
            self.list.extend(elements)
    def isEmpty(self):
        if len(self.list == 0):
            return True
        return False
    
        
