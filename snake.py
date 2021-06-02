import pygame as pg
from pygame.math import Vector2 as v2
import time
import sys
import random


class Snake:
    def __init__(self):
        self.body = [v2(5, 10), v2(6, 10)]
        self.movement = v2(1, 0)

    def draw_snake(self):
        for block in self.body:
            snake_rect = pg.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pg.draw.rect(board, (0, 0, 0), snake_rect)

    def move_snake(self):
        copy_body = self.body[:-1]
        copy_body.insert(0, copy_body[0] + self.movement)
        self.body = copy_body



class Food:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1) 
        self.y = random.randint(0, cell_number - 1) 
        self.vector = v2(self.x, self.y)

    def place_food(self):
        food_rect = pg.Rect(self.vector.x * cell_size, self.vector.y * cell_size, cell_size, cell_size)
        pg.draw.rect(board, (255, 0, 0), food_rect)




class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
    def update(self):
        self.snake.move_snake()
    def draw_elements(self):
        self.snake.draw_snake()
        self.food.place_food()
    def check_position(self):
        if self.food.vector == self.snake.body[0]:
            print("Test")
            self.food = Food()
            #reposition the fruit
            # add another block to the snake




pg.init()
clock = pg.time.Clock()
framerate = 60
bg_color = (175, 215, 75)
cell_size = 40 
cell_number = 20
window_width = 800 
game = True
board = pg.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pg.display.set_caption('Snake by Tenos200')



SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

game = Main()

while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                game.snake.movement = (1, 0)
            if event.key == pg.K_LEFT:
                game.snake.movement = (-1, 0)
            if event.key == pg.K_UP:
                game.snake.movement = (0, -1)
            if event.key == pg.K_DOWN:
                game.snake.movement = (0, 1)


    board.fill(bg_color)
    game.draw_elements()
    game.check_position()
    pg.display.update()
    clock.tick(framerate)
    
