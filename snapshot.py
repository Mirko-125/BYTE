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


import pygame as pg
import sys

def prompt():
    pg.init()
    windowSize = (835, 400)
    screen = pg.display.set_mode(windowSize)
    pg.display.set_caption("BYTE | Set your dimensions")
    regular_font = pg.font.Font(None, 36)
    techy_font = pg.font.Font(None, 24)
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
                        if number in [8, 10, 16]:
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
        inputRect = pg.Rect(50, 100, 200, 40)
        pg.draw.rect(screen, (255, 255, 255), inputRect, 2)

        # Render and display input prompt with a default font
        promptText = regular_font.render("Board size NxN, N is:", True, (255, 255, 255))
        inputPrompt = regular_font.render(inputText, True, (255, 255, 255))
        screen.blit(promptText, (50, 50))
        screen.blit(inputPrompt, (55, 105))
        techyText = techy_font.render("Made by: Mirko Bojanić 18087, Miloš Miljković 19040, Nemanja Stanković 18391", True, (80, 90, 110))
        screen.blit(techyText, (20, windowSize[1] - 40))

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
            cls._instance.highlighter = loadAndScaleImage("./Assets/green.png", (cls._instance.tileSize, cls._instance.tileSize))
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
                stackPointer = graph.nodes[c][graphStack]  # graph[c][1]
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
    #highlighter = pg.Surface((interfaceTools.tileSize, interfaceTools.tileSize), pg.SRCALPHA)
    #highlighter.fill((0, 255, 0, 64))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                drawTable(graph, interfaceTools)
                mouse_x, mouse_y = pg.mouse.get_pos()
                c = 1
                for y in range(0, interfaceTools.height, interfaceTools.tileSize):
                    for x in range(0, interfaceTools.width, interfaceTools.tileSize):
                        if (x+y) % 2 == 0:
                            rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)

                            stackPointer = graph.nodes[c][graphStack]  # graph[c][1]
                            stackPointer.setCoordinates(x, y)

                            if rect.collidepoint(mouse_x, mouse_y):
                                #print("Starting coordinates:", x, y)
                                #interfaceTools.background.blit(highlighter, (x - 10, y - 10), special_flags=pg.BLEND_RGBA_SUB)
                                print(legalMoves)
                                print(color)
                                for n in graph.nodes[c][allowedMoves][color].keys():
                                    interfaceTools.background.blit(interfaceTools.highlighter, (graph.nodes[n][graphStack].x, graph.nodes[n][graphStack].y))
                                if isClickedState is False:
                                    if graph.nodes[c][allowedMoves][color]:
                                        print(f"Allowed moves are : {graph.nodes[c][allowedMoves][color]}")
                                        isClickedState = True
                                        legalMoves = graph.nodes[c][allowedMoves][color]
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
        screen.blit(interfaceTools.background, (0, 0))
        pg.display.flip()
        clock.tick(60)
        playerTurn = not playerTurn
    pg.quit()
    sys.exit()