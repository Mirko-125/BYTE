import itertools


def fun():
    return True, 17
def checkforwinner():
    return False

def checkfortie():
    return False

def playturn(curr):
    return "Sada igra " + str(curr)
def coordinateParse(coordinate, offsetMultiplier, multiplier = 1):
    return multiplier * (coordinate / offsetMultiplier)
def parseCoordinatesIntoKey(coordinates):
    return (coordinates.x + coordinates.y + 1) / 2
def parseCoordinates(coordinates, offsetMultiplier, N):
    return (
        coordinateParse(coordinates.x, offsetMultiplier),
        coordinateParse(coordinates.y, offsetMultiplier, N)
    )

player = itertools.cycle((1,2))


if __name__ == '__main__':# moj koncept za menjanje stanja

    curr = 1
    status = True
    while not (checkforwinner() or checkfortie()):
        if curr == 1:
            curr = 2
            print(status)
            input("continue...")
        elif curr == 2:
            curr = 1
            print(status)
            input("continue...")
        status = not status
    # num1, num2 = fun()
    # print(num2)
#211
'''
        if whitePlayer.isWinner():
            return 'WhiteWon'
        elif blackPlayer.isWinner():
            return 'BlackWon'
        screen.fill((60, 70, 90))
        screen.blit(interfaceTools.background, (10, 10))

        pg.display.flip()
        clock.tick(60)
'''