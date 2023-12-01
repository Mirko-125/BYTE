#N = unos() done
#graph_generator = GraphGenerator(N, 1)
#graph_generator.createTable()
#resulting_graph = graph_generator.graph
#createTable(resulting_graph: Graph)
from snapshot import *
from graph import *

if __name__ == '__main__':
    n = getEvenPositiveInput()
    graph = Graph(n)
    graph.createTable()

    for key, value in graph.nodes.items():
        print(f"Node {key}: {value[neighborNodes]}, {value[graphStack]}")

    mainBoard(graph.nodes,n)