N = 8
K = 1
def LO (K, N):
    return K - N/2
def UO (K, N):
    return K + N/2
def isOdd (K, N):
    return K % N + 1 > N / 2
def isFirstRow(K, N):
    return K < N/2 + 1
def isFirstOddElement(K, N):
    return K % N == 4
def isLastEvenElement(K, N):
    return K % N == 5

def initializeGraph():
    graph = {}
    for key in range(1, N**2/2 + 1):
        graph[key] = ([], [], [])
    return graph

def createTable(graph):
    graph[1][0].add(UO+1)
    for key in range(2, N/2 + 1):
        graph[key][0].add(UO, UO+1)
    for key in range(N/2+1, N**2 / 2 - N/2 + 1):
        if isOdd(key, N):
            if isFirstOddElement(key, N):
                graph[key][0].add(LO + 1, UO + 1)
            else:
                graph[key][0].add(LO, LO + 1, UO, UO + 1)
        else:
            if isLastEvenElement(key, N):
                graph[key][0].add(LO - 1, UO - 1)
            else:
                graph[key][0].add(LO - 1, LO, UO - 1, UO)
    for key in range(N**2 / 2 - N/2 + 1, N**2 / 2):
        graph[key][0].add(LO - 1, LO, UO - 1, UO)
    graph[N**2/2][0].add(UO - 1)

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
            graph[key] = ([], [], [])
        return graph

    def createTable(self):
        self.graph[1][0].append(self.UO(1) + 1)
        for key in range(2, int(self.N/2) + 1):
            self.graph[key][0].extend([self.UO(key), self.UO(key) + 1])
        for key in range(int(self.N/2) + 1, int(self.N**2 / 2 - self.N/2) + 1):
            if self.isOdd(key):
                if self.isFirstOddElement(key):
                    self.graph[key][0].extend([self.LO(key) + 1, self.UO(key) + 1])
                else:
                    self.graph[key][0].extend([self.LO(key), self.LO(key) + 1, self.UO(key), self.UO(key) + 1])
            else:
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
    print(f"Node {key}: {value}")