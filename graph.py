from piece import Piece
from stack import Stack

class GraphGenerator:
    def __init__(self, N, K):
        self.N = N
        self.K = K
        self.graph = self.initializeGraph()

    def LO(self, K):
        return int(K - self.N/2)

    def UO(self, K):
        return int(K + self.N/2)

    def isOdd(self, K):
        return K % self.N + 1 > self.N / 2

    def isFirstRow(self, K):
        return K < self.N/2 + 1

    def isFirstOddElement(self, K):
        return K % self.N == 4

    def isLastEvenElement(self, K):
        return K % self.N == 5

    def initializeGraph(self):
        graph = {}
        for key in range(1, int(self.N**2/2) + 1):
            graph[key] = ([], Stack(False), [])
        return graph
    
    
    def createTable(self):
        self.graph[1][0].append(self.UO(1) + 1)
        for key in range(2, int(self.N/2) + 1):
            self.graph[key][0].extend([self.UO(key), self.UO(key) + 1])
        for key in range(int(self.N/2) + 1, int(self.N**2 / 2 - self.N/2) + 1):
            if self.isOdd(key):
                self.graph[key][1].add([Piece("White").color])
                if self.isFirstOddElement(key):
                    self.graph[key][0].extend([self.LO(key) + 1, self.UO(key) + 1])
                else:
                    self.graph[key][0].extend([self.LO(key), self.LO(key) + 1, self.UO(key), self.UO(key) + 1])
            else:
                self.graph[key][1].add([Piece("Black").color])
                if self.isLastEvenElement(key):
                    self.graph[key][0].extend([self.LO(key) - 1, self.UO(key) - 1])
                else:
                    self.graph[key][0].extend([self.LO(key) - 1, self.LO(key), self.UO(key) - 1, self.UO(key)])
        for key in range(int(self.N**2 / 2 - self.N/2) + 1, int(self.N**2 / 2)):
            self.graph[key][0].extend([self.LO(key) - 1, self.LO(key)])
        self.graph[int(self.N**2/2)][0].append(self.LO(int(self.N**2/2)) - 1)

N = 8
K = 1
graph_generator = GraphGenerator(N, K)
graph_generator.createTable()
resulting_graph = graph_generator.graph

for key, value in resulting_graph.items():
    print(f"Node {key}: {value[1].list}")