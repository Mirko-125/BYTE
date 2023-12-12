from piece import Piece
from stack import Stack
from graphConstants import *

class Graph:
    def __init__(self, N):
        self.N = N
        self.K = 1
        self.size = int(N**2 / 2) 
        self.offset = int(N/2)
        self.oddRange = set()
        self.validDirections = [self.UR, self.UL, self.DL, self.DR]
        for number in range (1, int(N/2 + 1)):
            self.oddRange.add(number)
        self.nodes = self.initializeGraph()
        self.createTable()
        for key in self.nodes:
            self.updateLegalMoves(key)

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
    
    def oppositeDirection(self, direction_func):
        if direction_func == self.UL:
            return self.DR
        elif direction_func == self.UR:
            return self.DL
        elif direction_func == self.DL:
            return self.UR
        elif direction_func == self.DR:
            return self.UL
        else:
            return None

    def isFirstRow(self, K):
        return K < self.N/2 + 1

    def isFirstOddElement(self, K):
        return K % int(self.N/2) == 1

    def isLastEvenElement(self, K):
        return K % self.N == 0

    def initializeGraph(self):
        graph = {}
        for key in range(1, int(self.N**2/2) + 1):
            graph[key] = {neighborNodes: [], graphStack: Stack(False), allowedMoves: {}}
        return graph
    
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
    
    def validateKey(self, key):
        if (key > 0 and key <= self.size):
            return True
        raise ValueError("The field does not exist")
    
    def validateStack(self, key):
        if (self.nodes[key][graphStack].isEmpty()):
            raise MemoryError("The stack is empty")
        return True
    
    def nearbyStackAltitudes(self, moves):
        viableNeighborNodes = list(moves.keys())
        return {
            node: stackAltitude
            if (self.nodes[node][graphStack].isEmpty()) else self.nodes[node][graphStack].length()
            for node in viableNeighborNodes
            }

    def filterMovesPerSize(self, indexes: list, stack, comparedStack):
        return [index for index in indexes if stack.validateMaxSize(index, comparedStack)]

    def parseMovesPerColor(self, moves, altitudeDifferences, stack, color):
        return { key : (direction, indexes)
                 for key, direction in moves.items()
                 if (indexes := self.filterMovesPerSize(stack.getIndexesForColor(altitudeDifferences[key], color), stack, self.nodes[key][graphStack]))
        }
    
    def parseMovesPerPlayer(self, moves, key):
        stack = self.nodes[key][graphStack]
        altitudeDifferences = self.nearbyStackAltitudes(moves)
        return {'Black': self.parseMovesPerColor(moves, altitudeDifferences, stack, "Black"),
        'White': self.parseMovesPerColor(moves, altitudeDifferences, stack, "White")}
        
    
    def validateDirection(self, direction, key):
        if direction in self.validDirections:
            dstKey = direction(key)
            if (dstKey in self.nodes[key][neighborNodes]):
                return True
        return False
    
    def playersLegalMoves(self, color):
        legalMoves = []
        for node in self.nodes:
            if color in node[graphStack]:
                legalMoves += (node.keys(), node[allowedMoves])

    def updateLegalMoves(self, key):
        closestDistance = self.BFS(key, self.N, key)
        moves = self.closestDirections(key, closestDistance)
        self.nodes[key][allowedMoves] = self.parseMovesPerPlayer(moves, key)   # [(node, visina indexa)]
   
    def closestDirections(self, key, maxDistance):
        return {
            direction(key): direction
            for direction in self.validDirections
            if (
                self.validateDirection(direction, key) 
                and not self.nodes[key][graphStack].isEmpty()
                and self.BFS(direction(key), maxDistance, key)
                and direction(key) in self.nodes[key][neighborNodes]
            )
        }
    
    def nodesToUpdate(self, srcKey, dstKey):
        visited = {0}
        queue = [srcKey, dstKey]
        toUpdateList = []
        while (len(queue)>0):
            iteration = len(queue)
            for _ in range(iteration):
                key = queue.pop(0)
                visited.add(key)
                for neighborNode in self.nodes[key][neighborNodes]:
                    if neighborNode not in visited:
                        if self.nodes[neighborNode][graphStack].isEmpty():
                            queue.append(neighborNode)
                        else:
                            visited.add(neighborNode)
                            toUpdateList.append(neighborNode)
        return toUpdateList
    
    def updateState(self, srcKey, dstKey):
        for node in self.nodesToUpdate(srcKey, dstKey):
            self.updateLegalMoves(node)

    def BFS(self, key, maxDistance, src = 0):
        visited = {src}
        queue = [key]
        distance = 0
        while (distance < maxDistance):
            iteration = len(queue)
            for _ in range(iteration):
                key = queue.pop(0)
                if not self.nodes[key][graphStack].isEmpty():
                    if key != src:
                        if (distance == 0):
                            return 1 
                        else:
                            return distance
                visited.add(key)
                for neighborNode in self.nodes[key][neighborNodes]:
                    if (neighborNode not in visited):
                        queue.append(neighborNode)
            distance += 1
        return False
    
    def isLegalMove(self, key, dstKey, index, color):
        if dstKey in self.nodes[key][allowedMoves][color]:
            if index in self.nodes[key][allowedMoves][color][dstKey][1]:
                return True
            return False
        
    def move(self, key, index, direction, color):
        self.validateKey(key)
        self.validateStack(key)
        if not self.validateDirection(direction, key):
            raise ValueError("Invalid direction")

        dstKey = direction(key)
        if (self.isLegalMove(key, dstKey, index, color)):
            topElement = self.nodes[dstKey][graphStack].add(self.nodes[key][graphStack].pop(index))
            self.updateState(key, dstKey)
            return topElement
        return False