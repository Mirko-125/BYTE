from graph import Graph
from graphConstants import *

graph = Graph(8)
graph.createTable()

for key in graph.nodes:
    graph.updateLegalMoves(key)
graph.move(9, 1, graph.UR)      
for key, value in graph.nodes.items():
    print(f"Node {key}: {value[neighborNodes]}, {value[allowedMoves]}")