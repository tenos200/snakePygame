import pygame as pg
import sys

bg_color = (175, 215, 75)
window_height = 600
window_width = 600
x = 50
y = 50
velocity = 2


def main():
    pg.init()
    board = pg.display.set_mode((window_width, window_height))
    clock = pg.time.Clock()
    board.fill(bg_color)
    pg.display.set_caption('Snake')
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        clock.tick(60)

    return board 

if __name__ == "__main__":
    main()
    
