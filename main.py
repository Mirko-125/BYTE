from snapshot import *
from graph import *
from graphConstants import graphStack

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

    mainBoard(graph.nodes,n)