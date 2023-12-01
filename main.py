from snapshot import *
from graph import *
from graphConstants import graphStack

def stackMove(graph,key,count,direction, interfaceTools):
    graph.move(key,count,direction)
    drawChips(interfaceTools, graph.nodes[key][graphStack])
    drawChips(interfaceTools, graph.nodes[direction(key)][graphStack])

if __name__ == '__main__':
    n = getEvenPositiveInput()
    graph = Graph(n)
    graph.createTable()
    graph.nodes[5][graphStack].add([Piece('Black').color])
    graph.nodes[5][graphStack].add([Piece('White').color])
    graph.nodes[5][graphStack].add([Piece('White').color])
    graph.nodes[5][graphStack].add([Piece('Black').color])
    graph.nodes[5][graphStack].add([Piece('White').color])
    graph.nodes[5][graphStack].add([Piece('White').color])

    for key, value in graph.nodes.items():
        print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")

    interfaceTools = InterfaceTools(n)
    mainBoard(graph.nodes,interfaceTools)
    stackMove(graph, 5, 4, graph.DR, interfaceTools)