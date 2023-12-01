import itertools
import pygame as pg
import sys
from graphConstants import graphStack

'''
beta function
def drawPieces(background, white, black, coordinates, stack):
    for element in stack:
        #cord.z += 0
        if (element.color == "White"):
            background.blit(white, coordinates)
        else:
            background.blit(black, coordinates)
'''
def drawChip(background,black,white,x,y,stack):
    if not stack.list:
        pass
    elif stack.list[-1] == 'Black':
        background.blit(black, (x,y))
    elif stack.list[-1] == 'White':
        background.blit(white, (x, y))

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


def mainBoard(graph, n):
    pg.init()

    black = pg.Color(192, 192, 192)
    white = pg.Color(105, 105, 105)

    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()

    colors = itertools.cycle((white, black))
    tileSize = 75

    width, height = n * tileSize, n * tileSize
    background = pg.Surface((width, height))

    blackChip = loadAndScaleImage("./Assets/black-chip.png", (tileSize, tileSize))
    whiteChip = loadAndScaleImage("./Assets/white-chip.png", (tileSize, tileSize))

    c = 1
    for y in range(0, height, tileSize):
        for x in range(0, width, tileSize):
            rect = (x, y, tileSize, tileSize)
            pg.draw.rect(background, next(colors), rect)
            if (x + y) % 2 == 0:
                stackPointer = graph[c][graphStack]  # graph[c][1]
                print(c)
                print(stackPointer) #drawPieces(background,whiteChip,blackChip,(x,y),stackPointer)
                drawChip(background,blackChip,whiteChip,x,y,stackPointer)
                c += 1
                # stack pointer spot

        next(colors)

    gameExit = False
    while not gameExit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit = True

        screen.fill((60, 70, 90))
        screen.blit(background, (300, 80))

        pg.display.flip()
        clock.tick(30)

    pg.quit()