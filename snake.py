import pygame as pg
from pygame.math import Vector2 as v2
import time
import sys
import random


class Snake:
    def __init__(self):
        self.body = [v2(5, 10), v2(6, 10), v2(7, 10)]
    def draw_snake(self):
        for block in self.body:
            snake_rect = pg.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pg.draw.rect(board, (0, 0, 0), snake_rect)
        

class Food:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1) 
        self.y = random.randint(0, cell_number - 1) 
        self.vector = v2(self.x, self.y)

    def place_food(self):
        food_rect = pg.Rect(self.vector.x * cell_size, self.vector.y * cell_size, cell_size, cell_size)
        pg.draw.rect(board, (255, 0, 0), food_rect)




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

fruit = Food()
snake = Snake()

while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False

    board.fill(bg_color)
    snake.draw_snake()
    fruit.place_food()
    pg.display.update()
    clock.tick(framerate)
    
