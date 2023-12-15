from graph import *
from graphConstants import *

graph = Graph(8)
for key in graph.nodes:
    graph.updateValidMoves(key)
graph.move(9, 0, graph.UR, 'White')      
#print(graph.getMovesForPlayer('White'))
pos_states = graph.possibleStates()
print(pos_states[8].nodes)
#for key, value in graph.nodes.items():
#    print(f"Node {key}: {value[NEIGHBOR_NODES]}, {value[ALLOWED_MOVES]}")