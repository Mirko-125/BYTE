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
    n = getEvenPositiveInput()
    graph = Graph(n)
    graph.createTable()
    graph.move(5, 1, graph.DR)

    # graph.move(5, 1, graph.DR) # pomeranje u dijagonalu sa polja 10 na polje dole desno od njega
    whitePlayer = Player("White")
    blackPlayer = Player("Black")
    whitePlayer.addPoints(2)
    if (whitePlayer.isWinner()):
        pg.quit()
    if (blackPlayer.isWinner()): # da je whitePlayer pobedio bi
        sys.exit()

    for key, value in graph.nodes.items():
        print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")

    interfaceTools = InterfaceTools(n)
    mainBoard(graph.nodes,interfaceTools)