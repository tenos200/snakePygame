import pygame as pg
import time
import sys


bg_color = (175, 215, 75)
game_over_color = (0, 0, 0) 
window_height = 30
window_width = 20
height = 20
width = 20
x = 50
y = 50
velocity = 3 


def main():
    x = 50
    y = 50
    height = 20
    width = 20
    pg.init()
    board = pg.display.set_mode((window_width * window_height, window_height * window_width))
    clock = pg.time.Clock()
    clock.tick(60)
    pg.display.set_caption('Snake')

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if x > 580 or x < 0 or y > 580 or y < 0:
            gameOver(board)

        if keys[pg.K_LEFT]:
            x-=velocity
        elif keys[pg.K_RIGHT]:
            x+=velocity
        elif keys[pg.K_UP]:
            y-=velocity
        elif keys[pg.K_DOWN]:
            y+=velocity

        board.fill(bg_color)
        pg.draw.rect(board, (0, 0, 0), (x, y, height, width))
        clock.tick(60)
        pg.display.update()


def gameOver(board):
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render('Game over!', False, (255, 0, 0))
        board.fill(game_over_color)
        board.blit(text, (200, 300))
        pg.display.update()

if __name__ == "__main__":
    main()
    

