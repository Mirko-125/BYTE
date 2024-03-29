from piece import Piece
from stack import Stack
import random
import copy
import sys
from graphConstants import *

class Graph:
    def __init__(self, N):
        self.N = N
        self.K = 1
        self.size = int(N ** 2 / 2)
        self.offset = int(N / 2)
        self.oddRange = set()
        self.canWhiteMove = False
        self.canBlackMove = False
        self.turn = 0
        self.whitePoints = 0
        self.blackPoints = 0
        self.validDirections = [self.UR, self.UL, self.DL, self.DR]
        for number in range(1, int(N / 2 + 1)):
            self.oddRange.add(number)
        self.nodes = self.initializeGraph()
        self.createTable()
        for key in self.nodes:
            self.updateValidMoves(key)

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
    
    def addPoints(self, color):
        if not color:
            return
        if color == 'White':
            self.whitePoints += 1
        else:
            self.blackPoints += 1

    def findMaxHeight(self):
        maxSize = 0
        for node in self.nodes:
            nodeLength = self.nodes[node][GRAPH_STACK].length()
            if nodeLength > maxSize:
                maxSize = nodeLength
        return maxSize

    def findStacksFromHeight(self, height):
        return [self.nodes[node][GRAPH_STACK] for node in self.nodes if self.nodes[node][GRAPH_STACK].length() == height]

    def getPlayerPoints(self, color):
        if color == 'White':
            return self.whitePoints
        return self.blackPoints

    def winConPoints(self):
        if self.N == 8:
            return 2
        if self.N == 10:
            return 3
        return 8

    def checkWinner(self):
        if self.whitePoints >= self.winConPoints():
            return (True, 'White')
        if self.blackPoints >= self.winConPoints():
            return (True, 'Black')
        return (False, '')

    def boolToColor(self, bool):
        if bool:
            return 'White'
        return 'Black'

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
        return K < self.N / 2 + 1

    def isFirstOddElement(self, K):
        return K % int(self.N / 2) == 1

    def isLastEvenElement(self, K):
        return K % self.N == 0

    def initializeGraph(self):
        graph = {}
        for key in range(1, int(self.N**2/2) + 1):
            graph[key] = {NEIGHBOR_NODES: [], GRAPH_STACK: Stack(False), ALLOWED_MOVES: {}}
        return graph
    
    def matchFuncToCopy(self, func):
        return getattr(self, func.__name__)
    
    def createTable(self):
        firstIteration = int(self.N/2) + 1
        secondIteration = int(self.N**2 / 2 - self.N/2) + 1
        finalIteration = int(self.N**2/2) 
        self.nodes[1][NEIGHBOR_NODES].append(self.DR(1))
        for key in range(2, firstIteration):
            self.nodes[key][NEIGHBOR_NODES].extend([self.DL(key), self.DR(key)])
        for key in range(firstIteration, secondIteration):
            if self.isOdd(key):
                self.nodes[key][GRAPH_STACK].add([Piece("White").color])
                if self.isFirstOddElement(key):
                    self.nodes[key][NEIGHBOR_NODES].extend([self.UR(key), self.DR(key)])
                else:
                    self.nodes[key][NEIGHBOR_NODES].extend([self.UR(key), self.UL(key), self.DL(key), self.DR(key)])
            else:
                self.nodes[key][GRAPH_STACK].add([Piece("Black").color])
                if self.isLastEvenElement(key):
                    self.nodes[key][NEIGHBOR_NODES].extend([self.UL(key), self.DL(key)])
                else:
                    self.nodes[key][NEIGHBOR_NODES].extend([self.UR(key), self.UL(key), self.DL(key), self.DR(key)])
        for key in range(secondIteration, finalIteration):
            self.nodes[key][NEIGHBOR_NODES].extend([self.UL(key), self.UR(key)])
        self.nodes[key+1][NEIGHBOR_NODES].append(self.UL(key + 1))
    
    def validateKey(self, key):
        if (key > 0 and key <= self.size):
            return True
        raise ValueError("The field does not exist")

    def validateStack(self, key):
        if (self.nodes[key][GRAPH_STACK].isEmpty()):
            raise MemoryError("The stack is empty")
        return True

    def nearbyStackAltitudes(self, moves):
        viableNeighborNodes = list(moves.keys())
        return {
            node: STACK_ALTITUDE
            if (self.nodes[node][GRAPH_STACK].isEmpty()) else self.nodes[node][GRAPH_STACK].length()
            for node in viableNeighborNodes
        }

    def filterMovesPerSize(self, indexes: list, stack, comparedStack):
        return [index for index in indexes if stack.validateMaxSize(index, comparedStack)]

    def parseMovesPerColor(self, moves, altitudeDifferences, stack, color):
        return { 
                key: (direction, indexes)
                for key, direction in moves.items()
                if (indexes := self.filterMovesPerSize(stack.getIndexesForColor(altitudeDifferences[key], color), stack, self.nodes[key][GRAPH_STACK]))
            }
    
    def parseMovesPerPlayer(self, moves, key):
        stack = self.nodes[key][GRAPH_STACK]
        altitudeDifferences = self.nearbyStackAltitudes(moves)
        return {'Black': self.parseMovesPerColor(moves, altitudeDifferences, stack, "Black"),
                'White': self.parseMovesPerColor(moves, altitudeDifferences, stack, "White")}

    def validateDirection(self, direction, key):
        if direction in self.validDirections:
            dstKey = direction(key)
            if (dstKey in self.nodes[key][NEIGHBOR_NODES]):
                return True
        return False
    
    def findOneMove(self, color):
        for node in self.nodes:
            if (len(self.nodes[node][ALLOWED_MOVES][color])):
                return True
        return False
    
    def getMovesForPlayer(self, color):
        return {node: items for node in self.nodes if (len(items:=self.nodes[node][ALLOWED_MOVES][color]))}
    
    def setOnlyBottomIndex(self, key):
        if not self.nodes[key][GRAPH_STACK].isEmpty():
            if self.nodes[key][GRAPH_STACK].list[0] == 'Black':
                for dstKey, value in self.nodes[key][ALLOWED_MOVES]['Black'].items():
                    self.nodes[key][ALLOWED_MOVES]['Black'][dstKey] = (value[0], [0])
                    self.nodes[key][ALLOWED_MOVES]['White'] = {}
            else:
                for dstKey, value in self.nodes[key][ALLOWED_MOVES]['White'].items():
                    self.nodes[key][ALLOWED_MOVES]['White'][dstKey] = (value[0], [0])
                    self.nodes[key][ALLOWED_MOVES]['Black'] = {}

    def updateValidMoves(self, key):
        closestDistance = self.BFS(key, self.N, key)
        moves = self.closestDirections(key, closestDistance)
        self.nodes[key][ALLOWED_MOVES] = self.parseMovesPerPlayer(moves, key)
        if (closestDistance > 1):
            self.setOnlyBottomIndex(key)
        if self.nodes[key][ALLOWED_MOVES]["Black"]:
            self.canBlackMove = True
        if self.nodes[key][ALLOWED_MOVES]["White"]:
            self.canBlackMove = True

    def closestDirections(self, key, maxDistance):
        return {
            direction(key): direction
            for direction in self.validDirections
            if (
                self.validateDirection(direction, key) 
                and not self.nodes[key][GRAPH_STACK].isEmpty()
                and self.BFS(direction(key), maxDistance, key)
                and direction(key) in self.nodes[key][NEIGHBOR_NODES]
            )
        }

    def nodesToUpdate(self, srcKey, dstKey):
        visited = {srcKey, dstKey}
        queue = [srcKey, dstKey]
        toUpdateList = [srcKey, dstKey]
        while (len(queue) > 0):
            iteration = len(queue)
            for _ in range(iteration):
                key = queue.pop(0)
                visited.add(key)
                for neighborNode in self.nodes[key][NEIGHBOR_NODES]:
                    if neighborNode not in visited:
                        if self.nodes[neighborNode][GRAPH_STACK].isEmpty():
                            queue.append(neighborNode)
                        else:
                            visited.add(neighborNode)
                            toUpdateList.append(neighborNode)
        return toUpdateList

    def updateState(self, srcKey, dstKey):
        for node in self.nodesToUpdate(srcKey, dstKey):
            self.updateValidMoves(node)
        if self.nodes[srcKey][GRAPH_STACK].isEmpty():
            self.updateValidMoves(srcKey)
        if self.nodes[dstKey][GRAPH_STACK].isEmpty():
            self.updateValidMoves(dstKey)
        self.canBlackMove = self.findOneMove('Black')
        self.canWhiteMove = self.findOneMove('White')

    def BFS(self, key, maxDistance, src=0):
        visited = {src}
        queue = [key]
        distance = 0
        while (distance < maxDistance):
            iteration = len(queue)
            for _ in range(iteration):
                key = queue.pop(0)
                if not self.nodes[key][GRAPH_STACK].isEmpty():
                    if key != src:
                        if (distance == 0):
                            return 1
                        else:
                            return distance
                visited.add(key)
                for neighborNode in self.nodes[key][NEIGHBOR_NODES]:
                    if (neighborNode not in visited):
                        queue.append(neighborNode)
            distance += 1
        return False 
    
    def canPlayerMove(self, color):
        if color == "Black":
            return self.canBlackMove
        if color == "White":
            return self.canWhiteMove
    
    def isValidMove(self, key, dstKey, index, color):
        if dstKey in self.nodes[key][ALLOWED_MOVES][color]:
            if index in self.nodes[key][ALLOWED_MOVES][color][dstKey][1]:
                return True
        raise ValueError("Invalid move")
        
    def move(self, key, index, direction, color):
        self.validateKey(key)
        self.validateStack(key)
        if not self.validateDirection(direction, key):
            raise ValueError("Invalid direction")
        self.turn += 1
        dstKey = direction(key)
        if (self.isValidMove(key, dstKey, index, color)):
            topElement = self.nodes[dstKey][GRAPH_STACK].add(self.nodes[key][GRAPH_STACK].pop(index))
            self.addPoints(topElement)
            self.updateState(key, dstKey)
            return topElement
        return False
    
    def stateEvaluation(self):
        winner = self.checkWinner()
        if winner[0]:
            if winner[1] == "White":
                return sys.maxsize
            else:
                return -sys.maxsize
        else:
            elementCounter = 0
            if not self.canBlackMove:
                elementCounter += 5
            if not self.canWhiteMove:
                elementCounter -= 5

            for key in self.nodes:
                stack = self.nodes[key][GRAPH_STACK]
                value = stack.length()
                if stack.getTopElement() == "Black":
                    value = -value
                elementCounter += value
            return 15 * (self.whitePoints - self.blackPoints) + elementCounter
        
            
    def newState(self, key, index, direction, color):
        newState = copy.deepcopy(self)
        matched_direction = newState.matchFuncToCopy(direction)
        newState.move(key, index, matched_direction, color)
        return newState
    
    
    def parsePossibleStatesPerPlayer(self, color):
        stateList = []
        playerMoves = self.getMovesForPlayer(color)
        for key, moves in playerMoves.items():
            for _, items in moves.items():
                direction, indexes = items
                for index in indexes:
                    state = self.newState(key, index, direction, color)
                    evaluatedPosition = state.stateEvaluation()
                    stateList.append((state, (key, index, direction, color), evaluatedPosition))
        return stateList

    def possibleStates(self):
        stateList = self.parsePossibleStatesPerPlayer('White')
        stateList.extend(self.parsePossibleStatesPerPlayer('Black'))
        return stateList
    
    def bestMove(self, color):
        depth = MAX_DEPTH
        valueCount = 5
        maxHeight = self.findMaxHeight()
        if self.turn < 12 and maxHeight < 4:
            depth -= 1
        else:
            valueCount = 10

        sortedStateList = sorted(self.parsePossibleStatesPerPlayer(color), key=lambda x: x[2], reverse = (color == "White"))
        if len(sortedStateList) < 10:
            depth += 1

        stateList = sortedStateList[:valueCount]
        if maxHeight > 5:
            stateList.extend(stateList[:-valueCount])

        maxValue = -sys.maxsize
        minValue = sys.maxsize
        bestMoveWhite = bestMoveBlack = stateList[0][1]

        for stateTuple in stateList:
            if self.turn < 5:
                return stateList[random.randint(1, len(stateList) - 1)][1]
            value = minMax(stateTuple[0], depth, -sys.maxsize, sys.maxsize, color == "White")
            if value > maxValue:
                maxValue = value
                bestMoveWhite = stateTuple[1]
            if value < minValue:
                minValue = value
                bestMoveBlack = stateTuple[1]

        if color == "White":
            return bestMoveWhite
        return bestMoveBlack
    

def minMax(graph, depth, alpha, beta, isWhitePlayer):
    if depth == 0 or graph.checkWinner()[0]:
        return graph.stateEvaluation()
    
    if isWhitePlayer:
        maxEval = -sys.maxsize
        for state in graph.parsePossibleStatesPerPlayer("White"):
            eval = minMax(state[0], depth - 1, alpha, beta, False)
            maxEval = max(eval, maxEval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    
    minEval = sys.maxsize
    for state in graph.parsePossibleStatesPerPlayer("Black"):
        eval = minMax(state[0], depth - 1, alpha, beta, True)
        minEval = min(minEval, eval)
        beta = min(beta, eval)
        if beta <= alpha:
            break
    return minEval