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

def parseCoordinates(coordinates, offsetMultiplier, N):
    return (
        coordinateParse(coordinates.x, offsetMultiplier),
        coordinateParse(coordinates.y, offsetMultiplier, N)
    )

def coordinateParse(coordinate, offsetMultiplier, multiplier = 1):
    return multiplier * (coordinate / offsetMultiplier)

def parseCoordinatesIntoKey(coordinates):
    return (coordinates.x + coordinates.y + 1) / 2

def getEvenPositiveInput():
    pg.init()

    # Set up the window
    windowSize = (400, 200)
    screen = pg.display.set_mode(windowSize)
    pg.display.set_caption("BYTE | Set your dimensions")

    # Set up fonts
    font = pg.font.Font(None, 36)
    inputText = ""

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # If Enter key is pressed, check if the input is a valid even positive number
                    try:
                        number = int(inputText)
                        if number > 0 and number % 2 == 0:
                            pg.quit()
                            return number
                        else:
                            # If not a valid input, clear the inputText
                            inputText = ""
                    except ValueError:
                        # If not a valid integer, clear the inputText
                        inputText = ""
                elif event.key == pg.K_BACKSPACE:
                    # If Backspace key is pressed, remove the last character
                    inputText = inputText[:-1]
                else:
                    # Append other keypresses to the inputText
                    inputText += event.unicode

        # Draw the input prompt
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
                stackPointer = graph.nodes[c][graphStack]  # graph[c][1]
                stackPointer.setCoordinates(x, y)
                drawChips(interfaceTools, stackPointer)
                c += 1
                # stack pointer spot
        next(colors)

def movementHandle(cRect, stack, graph, state, interfaceTools):
    if not stack.isEmpty() and state:
        # Use legalMoves to return all keys with valid places to move
        # Use those keys to highlight appropriate rectangles on the field
        state = False
        while state is False:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    b = 1

                    for y in range(10, interfaceTools.height, interfaceTools.tileSize):
                        for x in range(10, interfaceTools.width, interfaceTools.tileSize):
                            if (x + y) % 2 == 0:
                                bRect = {}
                                rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)  # Maybe

                                bRect["rect"] = rect
                                bRect["nodeKey"] = b

                                bRect["x"] = x
                                bRect["y"] = y

                                b += 1

                                for n in graph.nodes[cRect['nodeKey']]['neighborNodes']:
                                    drawPossibleMove(n,bRect,interfaceTools)  # ne znam kako da pristupim grafu preko keya

                                if bRect["rect"].collidepoint(mouse_x, mouse_y):
                                    #print("Starting coordinates:", x, y)
                                    print(f"B is {bRect['nodeKey']}")
                                    if cRect['nodeKey'] == bRect['nodeKey']:
                                        print("you can exit the program.")
                                        return
                                    else:
                                        if graph.nodes[cRect['nodeKey']]['neighborNodes'][0] == bRect['nodeKey'] and not None:
                                            graph.move(cRect['nodeKey'],1,graph.UR)
                                            return
                                        elif graph.nodes[cRect['nodeKey']]['neighborNodes'][1] == bRect['nodeKey'] and not None:
                                            graph.move(cRect['nodeKey'], 1, graph.UL)
                                            return
                                        elif graph.nodes[cRect['nodeKey']]['neighborNodes'][2] == bRect['nodeKey'] and not None:
                                            graph.move(cRect['nodeKey'],1,graph.DL)
                                            return
                                        elif graph.nodes[cRect['nodeKey']]['neighborNodes'][3] == bRect['nodeKey'] and not None:
                                            graph.move(cRect['nodeKey'],1,graph.DR)
                                            return
                                        '''
                                        for x in graph.nodes[cRect['nodeKey']]['neighborNodes']:
                                            if x == bRect['nodeKey']:
                                                
                                        pass # prodjes kroz petlju bRecta i ako je b == susedu c onda je potez dozvoljen
                                        '''
        print(graph.nodes[cRect['nodeKey']])
        #graph.move(c['nodeKey'],1,graph.DR)

    print("goodbye.")
    pass

def drawPossibleMove(n,bRect,interfaceTools):
    print("##START##")
    print(n)
    print(bRect['nodeKey'])
    if bRect['nodeKey']!=n:
        interfaceTools.background.blit(interfaceTools.circle, (bRect['x'],bRect['y']))
    else:
        pass

    print("##END##")
def mainBoard(graph, interfaceTools):
    pg.init()

    black = pg.Color(192, 192, 192)
    white = pg.Color(105, 105, 105)

    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()

    colors = itertools.cycle((white, black))

    c = 1
    for y in range(0, interfaceTools.height, interfaceTools.tileSize):
        for x in range(0, interfaceTools.width, interfaceTools.tileSize):
            rect = (x, y, interfaceTools.tileSize, interfaceTools.tileSize)
            pg.draw.rect(interfaceTools.background, next(colors), rect)
            if (x + y) % 2 == 0:
                stackPointer = graph.nodes[c][graphStack]  # graph[c][1]
                stackPointer.setCoordinates(x,y)
                drawChips(interfaceTools,stackPointer)
                c += 1
                # stack pointer spot
        next(colors)

    running = True
    clickedKey = 0
    legalMoves = {}
    isClickedState = False
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
                            rectInfo = {}
                            rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)

                            stackPointer = graph.nodes[c][graphStack]  # graph[c][1]
                            stackPointer.setCoordinates(x, y)

                            #rectInfo["rect"] = rect
                            #rectInfo["nodeKey"] = c

                            rectInfo["x"] = x
                            rectInfo["y"] = y

                            
                            if rect.collidepoint(mouse_x, mouse_y):
                                print("Starting coordinates:", x, y)
                                print(f"Key is {c}") #rectInfo['nodeKey']
                                print(clickedKey)
                                print(legalMoves)
                                if isClickedState is False:
                                    if not stackPointer.isEmpty():
                                        print(f"Allowed moves are : {graph.nodes[c][allowedMoves]}")
                                        isClickedState = True
                                        legalMoves = graph.nodes[c][allowedMoves]
                                        clickedKey = c
                                elif c in legalMoves.keys():
                                    graph.move(clickedKey, len(graph.nodes[clickedKey][graphStack].list), legalMoves[c])
                                    drawTable(graph,interfaceTools)
                                    isClickedState = False
                                    legalMoves = {}
                                    clickedKey = 0
                                elif c == clickedKey:
                                    isClickedState = False
                                    legalMoves = {}
                                    clickedKey = 0
                                #movementHandle(rectInfo, stackPointer,graph, isClickedState, interfaceTools)
                            c+=1

        screen.fill((60, 70, 90))
        screen.blit(interfaceTools.background, (10, 10))
        
        pg.display.flip()
        clock.tick(60)

    pg.quit()