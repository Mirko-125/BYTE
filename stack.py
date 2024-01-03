class Stack:
    def __init__(self, element):
        self.x = 0
        self.y = 0
        self.max = 8
        self.list = [element] if element else []

    def add(self, elements: list):
        combinedLength = len(self.list) + len(elements)
        if combinedLength > 8:
            raise ValueError("Length over 8 is not allowed")
        self.list.extend(elements)
        if combinedLength == 8:
            finalElement = self.list.pop()
            self.list.clear()
            return finalElement
        return 0
    
    def getTopElement(self):
        if self.isEmpty():
            return None
        return self.list[self.length() - 1]

    def getSizeFromIndex(self, index):
        return self.length() - index

    def getIndexesForColor(self, height, color):
        count = min(height, self.length())
        return [index for index in range(count) if self.list[index] == color]

    def validateMaxSize(self, index, stack):
        return stack.length() + self.getSizeFromIndex(index) <= self.max

    def length(self):
        return len(self.list)

    def isEmpty(self):
        return self.length() == 0

    def pop(self, index):
        return [self.list.pop() for _ in range(self.getSizeFromIndex(index))][::-1]

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.list)