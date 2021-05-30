import pygame as pg
import time
import sys
import random


bg_color = (175, 215, 75)
game_over_color = (0, 0, 0) 
window_height = 30
window_width = 20
height = 20
width = 20
x = 50
y = 50
velocity = 2 


def main():
    x = 50
    y = 50
    x_change = 0
    y_change = 0
    height = 20
    width = 20
    rand_x = random.randint(1, window_width*window_height - width)
    rand_y = random.randint(1, window_height*window_width - height)
    pg.init()
    board = pg.display.set_mode((window_width * window_height, window_height * window_width))
    clock = pg.time.Clock()
    clock.tick(60)
    pg.display.set_caption('Snake')

    game = True
    game_over = False

    while game:
        while game_over:
            font = pg.font.Font('freesansbold.ttf', 22)
            msg = font.render("Game over! Press P to play again or Q to quit", True, (255, 0, 0))
            board.fill(game_over_color)
            board.blit(msg, (80, 250))
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_p:
                        main()




            
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
        pg.draw.rect(board, (255, 0, 0), (rand_x, rand_y, height, width))
        clock.tick(60)
        pg.display.update()

        if x >= 580 or x < 0 or y >= 580 or y < 0:
            x_change = 0
            y_change = 0
            game_over = True
        if x == rand_x and y == rand_y:
            print("Yummy!")

def quit():
    print("quitting")
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
