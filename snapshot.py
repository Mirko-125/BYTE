import itertools
import pygame as pg
import sys
from graphConstants import * # graph ih vec poziva
from graph import *
import random

def drawChips(interfaceTools,stack):
    offset = 0
    for element in stack.list:
        if len(stack.list) == 1:
            drawChip(interfaceTools, stack.x, stack.y - offset, element)
        else:
            drawChip(interfaceTools,stack.x+random.randint(-2, 2),stack.y-offset,element)
        offset += 13
def drawChip(interfaceTools,x,y,element):
    if element == 'Black':
        interfaceTools.background.blit(interfaceTools.blackChip, (x,y))
    else:
        interfaceTools.background.blit(interfaceTools.whiteChip, (x,y))
def prompt():
    pg.init()
    windowSize = (835, 400)
    screen = pg.display.set_mode(windowSize)
    pg.display.set_caption("BYTE | Set your dimensions")
    font = pg.font.Font(None, 36)
    inputText = ""
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    try:
                        number = int(inputText)
                        if number > 0 and number % 2 == 0:
                            pg.quit()
                            return number
                        else:
                            inputText = ""
                    except ValueError:
                        inputText = ""
                elif event.key == pg.K_BACKSPACE:
                    inputText = inputText[:-1]
                else:
                    inputText += event.unicode
        screen.fill((60, 70, 90))
        promptText = font.render("Board size NxN, N is:", True, (200, 200, 200))
        inputPrompt = font.render(inputText, True, (220, 220, 220))
        screen.blit(promptText, (50, 50))
        screen.blit(inputPrompt, (50, 100))
        pg.display.flip()

def loadAndScaleImage(imagePath, targetSize):
    image = pg.image.load(imagePath)
    return pg.transform.scale(image, targetSize)

class InterfaceTools:
    _instance = None  # Class variable to store the instance
    def __new__(cls, n):
        if cls._instance is None:
            cls._instance = super(InterfaceTools, cls).__new__(cls)
            cls._instance.tileSize = 75
            cls._instance.blackChip = loadAndScaleImage("./Assets/black-chip.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.whiteChip = loadAndScaleImage("./Assets/white-chip.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.circle = loadAndScaleImage("./Assets/circle.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.width = n * cls._instance.tileSize
            cls._instance.height = n * cls._instance.tileSize
            cls._instance.background = pg.Surface((cls._instance.width, cls._instance.height))
        return cls._instance

def drawTable(graph,interfaceTools):
    black = pg.Color(192, 192, 192)
    white = pg.Color(105, 105, 105)
    colors = itertools.cycle((white, black))
    c = 1
    for y in range(0, interfaceTools.height, interfaceTools.tileSize):
        for x in range(0, interfaceTools.width, interfaceTools.tileSize):
            rect = (x, y, interfaceTools.tileSize, interfaceTools.tileSize)
            pg.draw.rect(interfaceTools.background, next(colors), rect)
            if (x + y) % 2 == 0:
                stackPointer = graph.nodes[c][GRAPH_STACK]  # graph[c][1]
                stackPointer.setCoordinates(x, y)
                drawChips(interfaceTools, stackPointer)
                c += 1
                # stack pointer spot
        next(colors)

def swapColor(color):
    if color == 'White':
        return 'Black'
    elif color == 'Black':
        return 'White'

def mainBoard(graph, interfaceTools, whitePlayer, blackPlayer):
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    drawTable(graph,interfaceTools)
    running = True
    clickedKey = 0
    legalMoves = {}
    color = 'White'
    isClickedState = False
    playerTurn = True # White = True | Black = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                mouse_x, mouse_y = pg.mouse.get_pos()
                c = 1
                for y in range(10, interfaceTools.height, interfaceTools.tileSize):
                    for x in range(10, interfaceTools.width, interfaceTools.tileSize):
                        if (x+y)%2==0:
                            rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)

                            stackPointer = graph.nodes[c][GRAPH_STACK]  # graph[c][1]
                            stackPointer.setCoordinates(x, y)

                            if rect.collidepoint(mouse_x, mouse_y):
                                #print("Starting coordinates:", x, y)
                                print(legalMoves)
                                print(color)
                                if isClickedState is False:
                                    if graph.nodes[c][ALLOWED_MOVES][color]:
                                        print(f"Allowed moves are : {graph.nodes[c][ALLOWED_MOVES][color]}")
                                        isClickedState = True
                                        legalMoves = graph.nodes[c][ALLOWED_MOVES][color]
                                        clickedKey = c
                                elif c in legalMoves.keys():
                                    finalElement = graph.move(clickedKey, 0, legalMoves[c][0], color)
                                    drawTable(graph,interfaceTools)
                                    isClickedState = False
                                    legalMoves = {}
                                    clickedKey = 0
                                    color = swapColor(color)
                                    if finalElement == 'White':
                                        print('White got the stack')
                                        whitePlayer.addPoints(1)
                                    elif finalElement == 'Black':
                                        print('Black got the stack')
                                        blackPlayer.addPoints(1)
                                elif c == clickedKey:
                                    isClickedState = False
                                    legalMoves = {}
                                    clickedKey = 0
                            c+=1
        if whitePlayer.isWinner():
            return 'WhiteWon'
        elif blackPlayer.isWinner():
            return 'BlackWon'
        screen.fill((60, 70, 90))
        screen.blit(interfaceTools.background, (10, 10))
        pg.display.flip()
        clock.tick(60)
        playerTurn = not playerTurn
    pg.quit()
    sys.exit()