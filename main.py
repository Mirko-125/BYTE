import sys

from snapshot import *
from graph import *
from graphConstants import GRAPH_STACK
from player import Player

def stackMove(graph,key,count,direction, interfaceTools):
    graph.move(key,count,direction)
    drawChips(interfaceTools, graph.nodes[key][GRAPH_STACK])
    drawChips(interfaceTools, graph.nodes[direction(key)][GRAPH_STACK])

if __name__ == '__main__':
    n = prompt()
    graph = Graph(n)
    whitePlayer = Player("White")
    blackPlayer = Player("Black")

    #whitePlayer.addPoints(2)
    #if (whitePlayer.isWinner()):
        #pg.quit()
    #if (blackPlayer.isWinner()): # da je whitePlayer pobedio bi
        #sys.exit()
    #for key, value in graph.nodes.items():
        #print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")

    interfaceTools = InterfaceTools(n)
    if mainBoard(graph, interfaceTools, whitePlayer, blackPlayer)=='WhiteWon':
        print("White got the BYTE")
    else:
        print("Black got the BYTE")
