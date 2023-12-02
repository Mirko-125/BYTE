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
    whitePlayer = Player("White")
    blackPlayer = Player("Black")
    whitePlayer.addPoints(2)

    if (whitePlayer.isWinner()):
        pg.quit()

    for key, value in graph.nodes.items():
        print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")

    interfaceTools = InterfaceTools(n)
    mainBoard(graph.nodes,interfaceTools)
    #stackMove(graph, 5, 4, graph.DR, interfaceTools)