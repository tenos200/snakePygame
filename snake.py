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
    x_change = 0
    y_change = 0
    height = 20
    width = 20
    pg.init()
    board = pg.display.set_mode((window_width * window_height, window_height * window_width))
    clock = pg.time.Clock()
    clock.tick(60)
    pg.display.set_caption('Snake')

    game = True

    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_LEFT:
                    x_change = -velocity
                    y_change = 0
                elif event.key == pg.K_RIGHT:
                    x_change = velocity
                    y_change = 0
                elif event.key == pg.K_UP:
                    y_change = -velocity
                    x_change = 0
                elif event.key == pg.K_DOWN:
                    y_change = velocity
                    x_change = 0  

        y+=y_change
        x+=x_change
        board.fill(bg_color)

        pg.draw.rect(board, (0, 0, 0), (x, y, height, width))
        clock.tick(60)
        pg.display.update()

        if x > 580 or x < 0 or y > 580 or y < 0:
            x_change = 0
            y_change = 0
            game = gameOver(board)


def gameOver(board):
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render('Game over!', False, (255, 0, 0))
        board.fill(game_over_color)
        board.blit(text, (200, 300))
        pg.display.update()
        time.sleep(2)
        return False

if __name__ == "__main__":
    main()
    

