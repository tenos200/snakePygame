import pygame as pg
import sys

bg_color = (0, 255, 0)
window_height = 600
window_width = 600
x = 50
y = 50
velocity = 2


def main():
    pg.init()
    board = pg.display.set_mode((window_width, window_height))
    board.fill(bg_color)
    pg.display.set_caption('Snake')
    pg.display.flip()

    game = True
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False;
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and x < window_width - x:
            x+=velocity
        if keys[pg.K_LEFT] and x > 0:
            x+-velocity

        pg.draw.rect(board, (0, 0, 0), (x, y, 20, 20))
        move(x, y)
        pg.display.update()

    return board 

if __name__ == "__main__":
    main()
    
