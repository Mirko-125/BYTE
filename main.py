import sys
from snapshot import *
from graph import *
from player import Player

if __name__ == '__main__':
    n = prompt()
    graph = Graph(n)
    whitePlayer = Player("White")
    blackPlayer = Player("Black")
    interfaceTools = InterfaceTools(n)
    
    if mainBoard(n, graph, interfaceTools, whitePlayer, blackPlayer)=='WhiteWon':
        print("White got the BYTE")
    else:
        print("Black got the BYTE")