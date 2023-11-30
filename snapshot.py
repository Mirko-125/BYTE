import itertools
import pygame as pg
import sys

def get_even_positive_input():
    pg.init()

    # Set up the window
    window_size = (400, 200)
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("BYTE | Set your dimensions")

    # Set up fonts
    font = pg.font.Font(None, 36)
    input_text = ""

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # If Enter key is pressed, check if the input is a valid even positive number
                    try:
                        number = int(input_text)
                        if number > 0 and number % 2 == 0:
                            pg.quit()
                            return number
                        else:
                            # If not a valid input, clear the input_text
                            input_text = ""
                    except ValueError:
                        # If not a valid integer, clear the input_text
                        input_text = ""
                elif event.key == pg.K_BACKSPACE:
                    # If Backspace key is pressed, remove the last character
                    input_text = input_text[:-1]
                else:
                    # Append other keypresses to the input_text
                    input_text += event.unicode

        # Draw the input prompt
        screen.fill((60, 70, 90))
        prompt_text = font.render("Board size NxN, N is:", True, (200, 200, 200))
        input_prompt = font.render(input_text, True, (220, 220, 220))
        screen.blit(prompt_text, (50, 50))
        screen.blit(input_prompt, (50, 100))

        pg.display.flip()

if __name__ == '__main__':

    n = get_even_positive_input()

    pg.init()

    BLACK = pg.Color(192, 192, 192)
    WHITE = pg.Color(105, 105, 105)

    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()

    colors = itertools.cycle((WHITE, BLACK))
    tile_size = 75

    width, height = n * tile_size, n * tile_size
    background = pg.Surface((width, height))

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            rect = (x, y, tile_size, tile_size)
            pg.draw.rect(background, next(colors), rect)
        next(colors)

    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True

        screen.fill((60, 70, 90))
        screen.blit(background, (300, 80))

        pg.display.flip()
        clock.tick(30)

    pg.quit()
