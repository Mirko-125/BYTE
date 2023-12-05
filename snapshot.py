import itertools
import pygame as pg
import sys
from graphConstants import graphStack
import random

def drawChips(interfaceTools,stack):
    offset = 0
    for element in stack.list:
        drawChip(interfaceTools,stack.x+random.randint(-2, 2),stack.y-offset,element)
        offset += 13
def drawChip(interfaceTools,x,y,element):
    print(element)
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
            cls._instance.width = n * cls._instance.tileSize
            cls._instance.height = n * cls._instance.tileSize
            cls._instance.background = pg.Surface((cls._instance.width, cls._instance.height))
        return cls._instance

def mainBoard(graph, interfaceTools):
    pg.init()

    rectangleInfo = {}

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
                stackPointer = graph[c][graphStack]  # graph[c][1]
                stackPointer.setCoordinates(x,y)
                print(c)
                print(stackPointer)
                drawChips(interfaceTools,stackPointer)
                c += 1
                # stack pointer spot
        next(colors)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                mouse_x, mouse_y = pg.mouse.get_pos()
                c = 1

                for y in range(10, interfaceTools.height, interfaceTools.tileSize):
                    for x in range(10, interfaceTools.width, interfaceTools.tileSize):
                        rectInfo = {}
                        rect = pg.Rect(x, y, interfaceTools.tileSize, interfaceTools.tileSize)
                        rectInfo["rect"] = rect
                        rectInfo["nodeKey"] = c

                        if rectInfo["rect"].collidepoint(mouse_x, mouse_y):
                            # Rect clicked
                            print("Rect clicked at:", x, y)
                            print(f"Key being {rectInfo['nodeKey']}")


        screen.fill((60, 70, 90))
        screen.blit(interfaceTools.background, (10, 10))
        
        pg.display.flip()
        clock.tick(60)

    pg.quit()