from piece import Piece
from stack import Stack
from graphConstants import neighborNodes, graphStack

class Graph:
    def __init__(self, N):
        self.N = N
        self.K = 1
        self.size = int(N**2 / 2) 
        self.offset = int(N/2)
        self.oddRange = set()
        for number in range (1, int(N/2 + 1)):
            self.oddRange.add(number)
        self.nodes = self.initializeGraph()

    def UL(self, K):
        if (self.isOdd(K)):
           return K - self.offset - 1
        else:
            return K - self.offset

    def UR(self, K):
        return self.UL(K) + 1
    
    def DL(self, K):
        if (self.isOdd(K)):
            return K + self.offset - 1
        else:
            return K + self.offset
        
    def DR(self, K):
        return self.DL(K) + 1

    def isOdd(self, K):
        if (K % self.N in self.oddRange):
            return True
        return False

    def isFirstRow(self, K):
        return K < self.N/2 + 1

    def isFirstOddElement(self, K):
        return K % int(self.N/2) == 1

    def isLastEvenElement(self, K):
        return K % self.N == 0

    def initializeGraph(self):
        graph = {}
        for key in range(1, int(self.N**2/2) + 1):
            graph[key] = {neighborNodes: [], graphStack: Stack(False)}
        return graph
    
    def move(self, key, count, direction):
        if (key > 0 and key <= self.size):
            newKey = direction(key)
            if (newKey in self.nodes[key][neighborNodes]):
                return self.nodes[newKey][graphStack].add(self.nodes[key][graphStack].pop(count))
            else:
                ValueError("The node in this direction does not exist")
        else:
            raise ValueError(f"Value {key} must be between 0 and {self.size}")
        
    def createTable(self):
        firstIteration = int(self.N/2) + 1
        secondIteration = int(self.N**2 / 2 - self.N/2) + 1
        finalIteration = int(self.N**2/2) 
        self.nodes[1][neighborNodes].append(self.DR(1))
        for key in range(2, firstIteration):
            self.nodes[key][neighborNodes].extend([self.DL(key), self.DR(key)])
        for key in range(firstIteration, secondIteration):
            if self.isOdd(key):
                self.nodes[key][graphStack].add([Piece("White").color])
                if self.isFirstOddElement(key):
                    self.nodes[key][neighborNodes].extend([self.UR(key), self.DR(key)])
                else:
                    self.nodes[key][neighborNodes].extend([self.UR(key), self.UL(key), self.DL(key), self.DR(key)])
            else:
                self.nodes[key][graphStack].add([Piece("Black").color])
                if self.isLastEvenElement(key):
                    self.nodes[key][neighborNodes].extend([self.UL(key), self.DL(key)])
                else:
                    self.nodes[key][neighborNodes].extend([self.UR(key), self.UL(key), self.DL(key), self.DR(key)])
        for key in range(secondIteration, finalIteration):
            self.nodes[key][neighborNodes].extend([self.UL(key), self.UR(key)])
        self.nodes[key+1][neighborNodes].append(self.UL(key + 1))

#graph.move(9, 1, graph.DL)
#graph.move(13, 2, graph.DR)
#graph.move(17, 3, graph.DR)
#graph.move(17, 4, graph.UL)
#
#for key, value in graph.nodes.items():
#    print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")