import itertools
import pygame as pg
import sys
import time
from graphConstants import * 
from graph import *

def drawChips(interfaceTools,stack, coloredIndex = None):
    offset = 0
    for index, element in enumerate(stack.list):
        if coloredIndex is None or index < coloredIndex:
            if len(stack.list) == 1:
                drawChip(interfaceTools, stack.x, stack.y - offset, element)
            else:
                drawChip(interfaceTools,stack.x,stack.y - offset,element)
        else:
            if len(stack.list) == 1:
                drawSelectedChip(interfaceTools, stack.x, stack.y - offset, element)
            else:
                drawSelectedChip(interfaceTools, stack.x, stack.y - offset, element)
        offset += 13
        
def drawChip(interfaceTools, x, y, element):
    if element == 'Black':
        interfaceTools.background.blit(interfaceTools.blackChip, (x, y))
    else:
        interfaceTools.background.blit(interfaceTools.whiteChip, (x, y))

def drawSelectedChip(interfaceTools, x, y, element):
    if element == 'Black':
        interfaceTools.background.blit(interfaceTools.blackChipSelected, (x, y))
    else:
        interfaceTools.background.blit(interfaceTools.whiteChipSelected, (x, y))

def prompt():
    pg.init()
    windowSize = (835, 400)
    screen = pg.display.set_mode(windowSize)
    pg.display.set_caption("BYTE | Set your dimensions")
    regular_font = pg.font.Font(None, 36)
    techy_font = pg.font.Font(None, 24)
    checkbox_font = pg.font.Font(None, 24)

    inputText = ""
    checkbox_checked = True  # Default to checked

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
                            return number, checkbox_checked
                        else:
                            inputText = ""
                    except ValueError:
                        inputText = ""
                elif event.key == pg.K_BACKSPACE:
                    inputText = inputText[:-1]
            elif event.type == pg.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 270 and 150 <= event.pos[1] <= 170:
                    checkbox_checked = not checkbox_checked
            elif event.type == pg.TEXTINPUT:
                inputText += event.text

        screen.fill((60, 70, 90))
        inputRect = pg.Rect(50, 100, 250, 40)
        pg.draw.rect(screen, (255, 255, 255), inputRect, 2)

        promptText = regular_font.render("Board size NxN, N is:", True, (255, 255, 255))
        inputPrompt = regular_font.render(inputText, True, (255, 255, 255))
        screen.blit(promptText, (50, 50))
        screen.blit(inputPrompt, (55, 105))

        checkbox_rect = pg.Rect(250, 150, 20, 20) 
        pg.draw.rect(screen, (255, 255, 255), checkbox_rect, 2)
        if checkbox_checked:
            pg.draw.line(screen, (255, 255, 255), (250, 150), (270, 170), 2)
            pg.draw.line(screen, (255, 255, 255), (270, 150), (250, 170), 2)

        checkbox_label = checkbox_font.render("Do you want to play first?", True, (255, 255, 255))
        screen.blit(checkbox_label, (50, 150))

        techyText = techy_font.render("Made by: Mirko Bojanić 18087, Miloš Miljković 19040, Nemanja Stanković 18391", True,
                                      (80, 90, 110))
        screen.blit(techyText, (20, windowSize[1] - 40))

        pg.display.flip()

def loadAndScaleImage(imagePath, targetSize):
    image = pg.image.load(imagePath)
    return pg.transform.scale(image, targetSize)

class InterfaceTools:
    _instance = None  
    def __new__(cls, n):
        if cls._instance is None:
            cls._instance = super(InterfaceTools, cls).__new__(cls)
            cls._instance.tileSize = 75
            cls._instance.blackChip = loadAndScaleImage("./Assets/black-chip.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.whiteChip = loadAndScaleImage("./Assets/white-chip.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.blackChipSelected = loadAndScaleImage("./Assets/black-chip-selected.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.whiteChipSelected = loadAndScaleImage("./Assets/white-chip-selected.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.highlighter = loadAndScaleImage("./Assets/green.png", (cls._instance.tileSize, cls._instance.tileSize))
            cls._instance.width = n * cls._instance.tileSize
            cls._instance.height = n * cls._instance.tileSize
            cls._instance.background = pg.Surface((cls._instance.width, cls._instance.height))
        return cls._instance

def drawTable(graph,interfaceTools, specialChip = (0, None)):
    black = pg.Color(192, 192, 192)
    white = pg.Color(105, 105, 105)
    colors = itertools.cycle((white, black))
    key = 1
    for y in range(0, interfaceTools.height, interfaceTools.tileSize):
        for x in range(0, interfaceTools.width, interfaceTools.tileSize):
            rect = (x, y, interfaceTools.tileSize, interfaceTools.tileSize)
            pg.draw.rect(interfaceTools.background, next(colors), rect)
            if (x + y) % 2 == 0:
                stackPointer = graph.nodes[key][GRAPH_STACK]  
                stackPointer.setCoordinates(x, y)
                if specialChip[0] == key:
                    drawChips(interfaceTools, stackPointer, specialChip[1])
                else:
                    drawChips(interfaceTools, stackPointer)
                key += 1
        next(colors)

def swapColor(color):
    if color == 'White':
        return 'Black'
    elif color == 'Black':
        return 'White'
    
def cycleIndex(index, list):
    if index+1 == len(list):
        return 0
    return index + 1

def formSet(values):
    indexSet = set()
    for value in values:
        for index in value[1][1]:
            indexSet.add(index)
    return list(indexSet)

def indexInKeys(index, validMoves):
    return index in validMoves[1]

def mainBoard(SIZE, graph, interfaceTools, whitePlayer, blackPlayer, playerFirst):
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    drawTable(graph,interfaceTools)
    running = True
    clickedKey = 0
    validMoves = {}
    validIndexes = []
    color = 'White'
    selectedIndex = 0
    isClickedState = False
    font = pg.font.Font("./Assets/bahnschrift.ttf", 20)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                
                mouse_x, mouse_y = pg.mouse.get_pos()
                key = 1
                for y in range(0, interfaceTools.height, interfaceTools.tileSize):
                    for x in range(0, interfaceTools.width, interfaceTools.tileSize):
                        if (x+y) % 2 == 0:
                            rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)
                            stackPointer = graph.nodes[key][GRAPH_STACK] 
                            stackPointer.setCoordinates(x, y)

                            if rect.collidepoint(mouse_x, mouse_y):
                                if isClickedState is False:
                                    if graph.nodes[key][ALLOWED_MOVES][color]:
                                        #print(f"Allowed moves are : {graph.nodes[key][ALLOWED_MOVES][color]}")
                                        isClickedState = True
                                        validMoves = graph.nodes[key][ALLOWED_MOVES][color]
                                        validIndexes = formSet(validMoves.items())
                                        selectedIndex = 0
                                        clickedKey = key
                                        drawTable(graph, interfaceTools, (clickedKey, validIndexes[selectedIndex]))
                                        for n in graph.nodes[key][ALLOWED_MOVES][color].keys():
                                            interfaceTools.background.blit(interfaceTools.highlighter, (graph.nodes[n][GRAPH_STACK].x, graph.nodes[n][GRAPH_STACK].y))

                                elif key in validMoves.keys() and indexInKeys(validIndexes[selectedIndex], validMoves[key]):
                                    finalElement = graph.move(clickedKey, validIndexes[selectedIndex], validMoves[key][0], color)
                                    
                                    drawTable(graph,interfaceTools)
                                    time.sleep(1)
                                    isClickedState = False
                                    validMoves = {}
                                    validIndexes = []
                                    clickedKey = 0
                                    
                                    if graph.getMovesForPlayer(swapColor(color)):
                                        color = swapColor(color)
                                    elif not graph.getMovesForPlayer(color):
                                        print("NO VALID MOVES REMAIN, GAME CLOSING")
                                        pg.quit()
                                        sys.exit()

                                    if finalElement == 'White':
                                        print('White got the stack')
                                        whitePlayer.addPoints(1)
                                        print("White player: ")
                                        print(whitePlayer.points)
                                    elif finalElement == 'Black':
                                        print('Black got the stack')
                                        blackPlayer.addPoints(1)
                                        print("Black player: ")
                                        print(blackPlayer.points)

                                    AIkey, AIindex, AIdirection, AIcolor = graph.bestMove(color)
                                    graph.move(AIkey, AIindex, AIdirection, AIcolor)
                                    drawTable(graph,interfaceTools)
                                    color = swapColor(color)

                                elif key == clickedKey:
                                    isClickedState = False
                                    validMoves = {}
                                    validIndexes = []
                                    clickedKey = 0
                                    drawTable(graph, interfaceTools)
                            key+=1
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and isClickedState:
                selectedIndex = cycleIndex(selectedIndex, validIndexes)
                drawTable(graph,interfaceTools, (clickedKey, validIndexes[selectedIndex]))
                for n in graph.nodes[clickedKey][ALLOWED_MOVES][color].keys():
                    if indexInKeys(validIndexes[selectedIndex], validMoves[n]):
                        interfaceTools.background.blit(interfaceTools.highlighter, (graph.nodes[n][GRAPH_STACK].x, graph.nodes[n][GRAPH_STACK].y))
                
        if whitePlayer.isWinner(SIZE):
            return 'WhiteWon'
        elif blackPlayer.isWinner(SIZE):
            return 'BlackWon'
        screen.fill((60, 70, 90))
        screen.blit(interfaceTools.background, (0, 0))
        whiteScore = font.render(f"White: {whitePlayer.points}", True, (255, 255, 255))
        blackScore = font.render(f"Black: {blackPlayer.points}", True, (255, 255, 255))
        onTheMove = font.render(f"{color} player is on the move.", True, (255, 255, 255))
        screen.blit(onTheMove, (interfaceTools.width + 100, 100))
        screen.blit(whiteScore, (interfaceTools.width + 100, 10))
        screen.blit(blackScore, (interfaceTools.width + 100, 50))
        onTheMove = font.render(f"{color} player is on the move.", True, (255, 255, 255))
        screen.blit(onTheMove, (interfaceTools.width + 100, 100))
        pg.display.flip()
        clock.tick(60)
    pg.quit()
    sys.exit()