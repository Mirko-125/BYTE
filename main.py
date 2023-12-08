import sys

from snapshot import *
from graph import *
from graphConstants import graphStack
from player import Player

def stackMove(graph,key,count,direction, interfaceTools):
    graph.move(key,count,direction)
    drawChips(interfaceTools, graph.nodes[key][graphStack])
    drawChips(interfaceTools, graph.nodes[direction(key)][graphStack])

if __name__ == '__main__':
    n = prompt()
    graph = Graph(n)
    graph.createTable()
    #graph.move(5, 1, graph.DR)
    whitePlayer = Player("White")
    blackPlayer = Player("Black")
    #whitePlayer.addPoints(2)
    #if (whitePlayer.isWinner()):
        #pg.quit()
    #if (blackPlayer.isWinner()): # da je whitePlayer pobedio bi
        #sys.exit()
    #for key, value in graph.nodes.items():
        #print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")
    points = 0
    while whitePlayer.isWinner() is False or blackPlayer.isWinner() is False:
        interfaceTools = InterfaceTools(n)
        if mainBoard(graph, interfaceTools): # mozda cemo morati da vratimo tuple umesto Tru/Flase
            points += 1
            whitePlayer.addPoints(points)
        else:
            points += 1
            blackPlayer.addPoints(points)
        points = 0
    pg.quit()