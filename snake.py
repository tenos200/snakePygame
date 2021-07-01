import pygame as pg
from pygame.math import Vector2 as v2
import time
import sys
import random

#to do -
#fix bug where you can exit game and get back to menu but not enter game again
#fix uncentered text in game over menu
#fix cursor in menu
#fix so you can start from menu
#fix case for animation when in top right and left screen
#add score, allow high score to be stored and loaded
#move globals to another render class now when game menu class is being implemented

#globals to render
pg.init()
cell_size = 40 
cell_number = 20
font = pg.font.SysFont('timesnewroman', 32)
font_menu = pg.font.SysFont('Raleway', 42, bold=True, italic=False)
font_header = pg.font.SysFont('timesnewroman', 62, bold=True, italic=False)
game_over_msg = f''
game_over_msg2 = f'Press R to play again or Q to quit'
text = font.render(game_over_msg, True, 
    (255, 0, 0), (0, 0, 0))
text2 = font.render(game_over_msg2, True, 
        (255, 0, 0), (0, 0, 0))
textRect = text.get_rect()
textRect.center = (cell_number*cell_size / 2, cell_number*cell_size / 2)
textRect2 = text.get_rect()
textRect2.midright= (cell_number*cell_size / 2 + 60, 
        cell_number*cell_size / 2 + 100)
board = pg.display.set_mode((cell_size * cell_number, 
    cell_size * cell_number))
pg.display.set_caption('Snake by Tenos200')
clock = pg.time.Clock()
SCREEN_UPDATE = pg.USEREVENT
speed = 120
pg.time.set_timer(SCREEN_UPDATE, speed)


class Menu:

    def __init__(self):
        self.cursor_x = cell_number*cell_size / 2 - 160
        self.cursor_y = cell_number*cell_size / 2
        self.top_cursor = cell_number*cell_size / 2  
        self.bottom_cursor = cell_number*cell_size / 2 + 120
        self.mid_cursor = cell_number*cell_size / 2 + 60
        self.move_down = 60
        self.move_up = -60
        self.game = Game()
        self.menu_color = (175, 215, 75)
        self.menu_text_color = (0, 0, 0)
        self.menu_text = 'Main Menu'
        self.play_text = 'Play'
        self.leaderboard_text = 'Leaderboard'
        self.help_text = 'Help'
        self.credits_text = 'Credits'
        self.mid = cell_number*cell_size / 2
        self.menu_cursor = font_menu.render('>', True, (0, 0, 0), self.menu_color)
        self.cursor_rect = self.menu_cursor.get_rect()
        self.cursor_rect.center = (self.cursor_x, 
                self.cursor_y)

    def menu_run(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:

                    if event.key == pg.K_RETURN:
                        if self.cursor_y == self.top_cursor:
                            self.game.run()
                        elif self.cursor_y == self.mid_cursor:
                            #add feature here
                            print('leaderboard')
                        elif self.cursor_y == self.bottom_cursor:
                            #add feature here
                            print('Help')
                    elif event.key == pg.K_UP:
                        if self.cursor_y == self.top_cursor:
                            self.cursor_y = self.bottom_cursor
                        else:
                            self.cursor_y+=self.move_up
                    elif event.key == pg.K_DOWN:
                        if self.cursor_y == self.bottom_cursor:
                            self.cursor_y = self.top_cursor
                        else:
                            self.cursor_y+=self.move_down

            self.draw_elements()
            self.draw_cursor()
            pg.display.update()


    def draw_cursor(self):
        self.draw_text(">", 'Raleway', True, 42, self.cursor_x, self.cursor_y)

    def draw_text(self, text, font_type, bold, size, x, y):
        fonts = pg.font.SysFont(font_type, size, bold, italic=False)
        display = fonts.render(text, True, (0, 0, 0), 
                self.menu_color)
        display_rect  = display.get_rect()
        display_rect.center = (x, y)
        board.blit(display, display_rect)

    def draw_elements(self):
            board.fill(self.menu_color)
            self.draw_text(self.menu_text,'timesnewroman', True, 62, self.mid,
                    self.mid - 180)
            self.draw_text(self.play_text,'Raleway', True, 42, 
                    self.mid, self.mid)
            self.draw_text(self.leaderboard_text,'Raleway', True, 42, 
                self.mid, self.mid + 60)
            self.draw_text(self.help_text,'Raleway', True, 42, 
                self.mid, self.mid + 120)


class Snake:

    def __init__(self):
        self.body = [v2(6, 10), v2(5, 10), v2(4, 10)]
        self.movement = v2(1, 0)
        self.grow = False

        #grahpics from clear code tutorial
        self.head_up = pg.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pg.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pg.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pg.image.load('graphics/head_left.png').convert_alpha()

        self.tail_up = pg.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pg.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pg.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pg.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pg.image.load(
                'graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pg.image.load(
                'graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pg.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pg.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pg.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pg.image.load('graphics/body_bl.png').convert_alpha()



    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_grahpics()

        for index, block in enumerate(self.body):
            snake_rect = pg.Rect(block.x * cell_size, block.y * cell_size, 
                    cell_size, cell_size)
            pg.draw.rect(board, (0, 0, 0), snake_rect)
            if index == 0:
                board.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                board.blit(self.tail, snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    board.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    board.blit(self.body_horizontal, snake_rect)
                else:
                    #print(f'{previous_block.x} 
                    #{previous_block.y} {next_block.x} {next_block.y}')
                    if previous_block.x == -1 and next_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.y == -1 and next_block.x == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 19:
                        board.blit(self.body_tl, snake_rect)
                    elif next_block.x == 19 and previous_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif next_block.x == -1 and previous_block.y == 19:
                        board.blit(self.body_tl, snake_rect)

                    elif previous_block.x == -1 and next_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.y == 1 and next_block.x == -1:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == -19:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif next_block.x == 19 and previous_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif next_block.x == -1 and previous_block.y == -19:
                        board.blit(self.body_bl, snake_rect)

                    elif previous_block.x == 1 and next_block.y == -1:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.y == -1 and next_block.x == 1:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 19:
                        board.blit(self.body_tr, snake_rect)
                    elif next_block.x == 1 and previous_block.y == 19:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == -19 and next_block.y == -1:
                        board.blit(self.body_tr, snake_rect)
                    elif next_block.x == -19 and previous_block.y == -1:
                        board.blit(self.body_tr, snake_rect)
                    
                    elif previous_block.x == 1 and next_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.y == 1 and next_block.x == 1:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -19:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == -19 and next_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif next_block.x == -19 and previous_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif next_block.x == 1 and previous_block.y == -19:
                        board.blit(self.body_br, snake_rect)


    def move_snake(self):
        if self.grow == True:
            copy_body = self.body[:]
            copy_body.insert(0, copy_body[0] + self.movement)
            self.body = copy_body
            self.grow = False
        else:
            copy_body = self.body[:-1]
            copy_body.insert(0, copy_body[0] + self.movement)
            self.body = copy_body


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        #cases for once snake goes outside box and appears on other side
        if head_relation == v2(-19, 0):
            self.head = self.head_left
        elif head_relation == v2(19, 0):
            self.head = self.head_right
        elif head_relation == v2(0, 19):
            self.head = self.head_down
        elif head_relation == v2(0, -19):
            self.head = self.head_up
        elif head_relation == v2(1, 0):
            self.head = self.head_left
        elif head_relation == v2(-1, 0):
            self.head = self.head_right
        elif head_relation == v2(0, -1):
            self.head = self.head_down
        elif head_relation == v2(0, 1):
            self.head = self.head_up


    def update_tail_grahpics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == v2(0, 19):
            self.tail = self.tail_down
        elif tail_relation == v2(0, -19):
            self.tail = self.tail_up
        elif tail_relation == v2(19, 0):
            self.tail = self.tail_right
        elif tail_relation == v2(-19, 0):
            self.tail = self.tail_left
        elif tail_relation == v2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == v2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == v2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == v2(0, 1):
            self.tail = self.tail_up

    def grow_snake(self):
        self.grow = True

    def reset(self):
        self.body = [v2(6, 10), v2(5, 10)]
        self.movement = v2(0, 0)
        game = Game()
        game.run()
        


class Food:

    def __init__(self):
        self.new_position()
        self.apple_graphic = pg.image.load(
                'graphics/apple.png').convert_alpha()

    def place_food(self):
        food_rect = pg.Rect(self.vector.x * cell_size, 
                self.vector.y * cell_size, cell_size, cell_size)
        board.blit(self.apple_graphic, food_rect)

    def new_position(self):
        self.x = random.randint(0, cell_number - 1) 
        self.y = random.randint(0, cell_number - 1) 
        self.vector = v2(self.x, self.y)



class Game:

    def __init__(self):
        self.framerate = 60
        self.game_over_color = (0, 0, 0)
        self.bg_color = (175, 215, 75)
        self.score = 0
        self.snake = Snake()
        self.food = Food()
        self.game_over_menu = False 
        self.game_run = True

    def update(self):
        self.snake.move_snake()
        self.check_boundary()
    
    def draw_elements(self):
        self.snake.draw_snake()
        self.food.place_food()

    def check_position(self):
        if self.food.vector == self.snake.body[0]:
            self.food.new_position()
            self.snake.grow_snake()
            self.update_score()

        for block in self.snake.body[1:]:
            if block == self.food.vector:
                self.food.place_food()

    def check_boundary(self):
        if self.snake.body[0].x >= cell_number:
            self.snake.body[0].x = 0
        if self.snake.body[0].x < 0:
            self.snake.body[0].x = cell_number - 1

        if self.snake.body[0].y >= cell_number:
            self.snake.body[0].y = 0
        if self.snake.body[0].y < 0:
            self.snake.body[0].y = cell_number - 1 

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: 
                self.game_over()

    def game_over(self):
        self.game_over_menu = True
        self.display_message()

    def update_score(self):
        self.score+=1

    def display_message(self):
        game_over_msg = f'Game over! Score: {self.score}'
        text = font.render(game_over_msg, True, 
            (255, 0, 0), (0, 0, 0))
        board.fill(self.game_over_color)
        board.blit(text, textRect)
        board.blit(text2, textRect2)
        self.score = 0
    
    def run(self):

        while self.game_run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_run = False
                if event.type == SCREEN_UPDATE:
                    self.update()
                if event.type == pg.KEYDOWN:
                    if self.game_over_menu:
                        if event.key == pg.K_q:
                            self.game_run = False
                        if event.key == pg.K_r:
                            self.game_over_menu = False
                            self.snake.reset()
                    if event.key == pg.K_RIGHT:
                        if self.snake.movement.x != -1:
                            self.snake.movement = v2(1, 0)
                    if event.key == pg.K_LEFT:
                        if self.snake.movement.x != 1:
                            self.snake.movement = v2(-1, 0)
                    if event.key == pg.K_UP:
                        if self.snake.movement.y != 1:
                            self.snake.movement = v2(0, -1)
                    if event.key == pg.K_DOWN:
                        if self.snake.movement.y != -1:
                            self.snake.movement = v2(0, 1)
            
            if not self.game_over_menu:
                board.fill(self.bg_color)
                self.draw_elements()
                self.check_position()

            pg.display.update()
            clock.tick(self.framerate)

menu = Menu()
menu.menu_run()
