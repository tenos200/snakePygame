import pygame as pg
from pygame.math import Vector2 as v2
import time
import sys
import random

#to do -
#add help menu as a class
#move graphics and ranking files to dot file format.
#move globals to another render class now when game menu class is being implemented
#make a class out of all the reading and writing to files, as DataHandler class
#make sure that the text and UI elements looks good
#remove all the magic numbers and replace with stuff that makes sense

#globals to render
pg.init()
cell_size = 40 
cell_number = 20
font = pg.font.SysFont('timesnewroman', 32)
font_menu = pg.font.SysFont('Raleway', 42, bold=True, italic=False)
font_header = pg.font.SysFont('timesnewroman', 62, bold=True, italic=False)
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
        self.menu_color = (175, 215, 75)
        self.menu_text_color = (0, 0, 0)
        self.menu_text = 'Main Menu'
        self.play_text = 'Play'
        self.leaderboard_text = 'Leaderboard'
        self.help_text = 'Help'
        self.file_name = 'rankings.txt'
        self.credits_text = 'Credits'
        self.mid = cell_number*cell_size / 2
        self.menu_cursor = font_menu.render('>', True, (0, 0, 0), self.menu_color)
        self.cursor_rect = self.menu_cursor.get_rect()
        self.cursor_rect.center = (self.cursor_x, 
                self.cursor_y)


        
    def create_file(self, file_name):
        try:
            with open(file_name) as f:
                print(f)
        except IOError:
            f = open(file_name, "w")
            f.close()


    def menu_run(self):
        self.create_file(self.file_name)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:

                    if event.key == pg.K_RETURN:
                        if self.cursor_y == self.top_cursor:
                            game = Game()
                            game.run()
                        elif self.cursor_y == self.mid_cursor:
                            leaderboard = Leaderboard()
                            leaderboard.run()
                        elif self.cursor_y == self.bottom_cursor:
                            helpmenu = HelpMenu()
                            helpmenu.run()
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


class Leaderboard:

    def __init__(self):
        self.text_color = (0, 0, 0)
        self.menu_color = (175, 215, 75)
        self.size = 42
        self.font_type = 'Raleway'
        self.font_header = 'timesnewroman'
        self.header = 'Leaderboard'
        self.apple_graphic = pg.image.load(
                'graphics/apple.png').convert_alpha()
        self.header_size = 62
        self.drawing = True
        self.x = cell_number*cell_size / 2 
        self.y = cell_number*cell_size / 2
        self.y_ranking = cell_number*cell_size / 2
        self.data_handler = DataHandler()
        board.fill(self.menu_color)


    def run(self):
        board.fill(self.menu_color)
        self.draw_header()
        while self.drawing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.drawing = False
            self.get_players()
            pg.display.update()
            

    def draw_header(self):
        fonts = pg.font.SysFont(self.font_header, self.header_size, True,
                italic=False)
        header_text = fonts.render(self.header, True, self.text_color, 
                self.menu_color)
        header_rect = header_text.get_rect()
        header_rect.center = (self.x, self.y - 200)
        board.blit(header_text, header_rect)

        
    def get_players(self):
        with open('rankings.txt') as ranking_file:
            rankings = ranking_file.readlines()
            swap = '' 
            ranking_pos = 1

            #work on better solution further on sorting
            for i in range(len(rankings)):
                name, score = rankings[i].split()
                score = int(score)
                for j in range(len(rankings)):
                    name2, score2 = rankings[j].split()
                    score2 = int(score2)
                    if (name != name2) and (score <= score2):
                        swap = rankings[i]
                        rankings[i] = rankings[j]
                        rankings[j] = swap

            rankings.reverse()

            #initalise new list to remove trailing '\n'
            rankings_display = []
            for x in rankings:
                rankings_display.append(x.replace('\n', ''))

            for text in rankings_display:
                name, score = text.split()
                self.draw_leaderboard(self.y - 100, ranking_pos, name, score)
                ranking_pos+=1
                self.y+=40

            self.y = cell_number*cell_size / 2


    def draw_leaderboard(self, position, ranking, name, score):
        #render for name
        fonts = pg.font.SysFont(self.font_type, self.size, False, italic=False)
        display_name = fonts.render(name, True, self.text_color, 
                self.menu_color)
        display_name_rect  = display_name.get_rect()
        display_name_rect.center = (self.x, position)
        #render for score
        fonts = pg.font.SysFont(self.font_type, self.size, False, italic=False)
        display_score = fonts.render(score, True, self.text_color, 
                self.menu_color)
        display_score_rect  = display_score.get_rect()
        display_score_rect.center = (self.x + 200, position)
        #render for ranking
        ranking = str(ranking) + '.'
        display_ranking = fonts.render(ranking, True, self.text_color, 
                self.menu_color)
        display_ranking_rect = display_ranking.get_rect()
        display_ranking_rect.center = (self.x - 280, position)
        #render for apple icon
        apple_score_rect = pg.Rect(self.x + 220, position - 20, 
                cell_size, cell_size)

        board.blit(display_name, display_name_rect)
        board.blit(display_score, display_score_rect)
        board.blit(self.apple_graphic, apple_score_rect)
        board.blit(display_ranking, display_ranking_rect)


class HelpMenu:

    def __init__(self):
        self.text_color = (0, 0, 0)
        self.menu_color = (175, 215, 75)
        self.size = 42
        self.font_type = 'Raleway'
        self.font_header = 'timesnewroman'
        self.header = 'Controls'
        self.arrow_up = pg.image.load(
                'graphics/up_arrow.png').convert_alpha()
        self.arrow_down = pg.image.load(
                'graphics/down_arrow.png').convert_alpha()
        self.arrow_right = pg.image.load(
                'graphics/right_arrow.png').convert_alpha()
        self.arrow_left = pg.image.load(
                'graphics/left_arrow.png').convert_alpha()
        self.header_size = 62
        self.drawing = True
        self.x = cell_number*cell_size / 2 
        self.y = cell_number*cell_size / 2
        self.y_ranking = cell_number*cell_size / 2

    def run(self):
        board.fill(self.menu_color)
        self.draw_header()
        while self.drawing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.drawing = False
            self.test_draw()
            pg.display.update()
    

    #sort these methods to display all controls
    def draw_header(self):
        fonts = pg.font.SysFont(self.font_header, self.header_size, True,
                italic=False)
        header_text = fonts.render(self.header, True, self.text_color, 
                self.menu_color)
        header_rect = header_text.get_rect()
        header_rect.center = (self.x, self.y - 200)
        board.blit(header_text, header_rect)
    
    def test_draw(self):
        right_arrow_rect = pg.Rect(self.x + 220, self.y - 20, 
                cell_size, cell_size)
        board.blit(self.arrow_up, right_arrow_rect)



class Snake:

    def __init__(self):
        self.body = [v2(6, 10), v2(5, 10), v2(4, 10)]
        self.movement = v2(1, 0)
        self.grow = False

        #graphics from clear code tutorial
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
        self.update_tail_graphics()

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
                    #print(f'{previous_block.x} {previous_block.y} {next_block.x} {next_block.y}')
                    if previous_block.x == -1 and next_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.y == -1 and next_block.x == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.y == 19 and next_block.x == 19:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 19:
                        board.blit(self.body_tl, snake_rect)
                    elif next_block.x == 19 and previous_block.y == -1:
                        board.blit(self.body_tl, snake_rect)
                    elif next_block.x == -1 and previous_block.y == 19:
                        board.blit(self.body_tl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == 19:
                        board.blit(self.body_tl, snake_rect)

                    elif previous_block.y == 1 and next_block.x == -1:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.y == -19 and next_block.x == 19:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == -19:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == -19:
                        board.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 19 and next_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif next_block.x == 19 and previous_block.y == 1:
                        board.blit(self.body_bl, snake_rect)
                    elif next_block.x == -1 and previous_block.y == -19:
                        board.blit(self.body_bl, snake_rect)
                    
                    elif previous_block.y == -1 and next_block.x == 1:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.y == 19 and next_block.x == -19:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 19:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == -19 and next_block.y == 19:
                        board.blit(self.body_tr, snake_rect)
                    elif previous_block.x == -19 and next_block.y == -1:
                        board.blit(self.body_tr, snake_rect)
                    elif next_block.x == 1 and previous_block.y == 19:
                        board.blit(self.body_tr, snake_rect)
                    elif next_block.x == -19 and previous_block.y == -1:
                        board.blit(self.body_tr, snake_rect)

                    elif previous_block.y == 1 and next_block.x == 1:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.y == -19 and next_block.x == -19:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -19:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == -19 and next_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif next_block.x == -19 and previous_block.y == 1:
                        board.blit(self.body_br, snake_rect)
                    elif previous_block.x == -19 and next_block.y == -19:
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


    def update_tail_graphics(self):
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
        self.body = [v2(6, 10), v2(5, 10), v2(4, 10)]
        self.movement = v2(1, 0)
        

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


class DataHandler:
    
    def check_name(self, name):
        #first check if player has not been entered into file
        with open('rankings.txt') as f:
            rankings = f.readlines()
        for i in range(len(rankings)):
            player, score = rankings[i].split()
            if player == name:
                return True 

        return False

    def save_player(self, name, score):
        player_stats = name + ' '  + str(score) + '\n'
        file1 = open('rankings.txt', "a")
        file1.write(player_stats)
        file1.close()



class Game:

    def __init__(self):
        self.game_over_msg = ''
        self.game_over_msg2 = 'Press R to play again or Q to quit to menu'
        self.framerate = 60
        self.max_characters = 12
        self.game_over_color = (0, 0, 0)
        self.text_color = (255, 0, 0)
        self.bg_color = (175, 215, 75)
        self.midpoint = cell_number*cell_size
        self.score = 0
        self.snake = Snake()
        self.food = Food()
        self.data_handler = DataHandler()
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
        if self.score == 0:
            board.fill(self.game_over_color)
            self.display_message(f'Game over!', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint-200)
            self.display_message('Press R to play again', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint)
            self.display_message('Press Q to quit.', 
                    self.text_color, self.game_over_color, 
                self.midpoint,self.midpoint+150)
        else:
            board.fill(self.game_over_color)
            self.display_message(f'Game over! Score: {self.score}', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint-200)
            self.display_message('Press R to play again', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint)
            self.display_message('Press S to save player', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint+150)
            self.display_message('Press Q to quit.', 
                    self.text_color, self.game_over_color, 
                    self.midpoint,self.midpoint+300)


    def update_score(self):
        self.score+=1

    def display_message(self, msg, text_color, bg_color, x, y):
        text = font.render(msg, True, text_color, bg_color)
        textRect = text.get_rect()
        textRect.center = (x / 2, y / 2)
        board.blit(text, textRect)

    
    def enter_name(self):
        name = ''
        writing = True
        #need to find a better solution for updating this value at first
        board.fill(self.game_over_color)
        self.display_message('Save as:',
                self.text_color, self.game_over_color,
                self.midpoint, self.midpoint)
        pg.display.update()

        while writing:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and name != '':
                        name_exists = self.data_handler.check_name(name)
                        if name_exists:
                            self.display_message('That name has already been saved.',
                                    self.text_color, self.game_over_color,
                                    self.midpoint, self.midpoint)
                            pg.display.update()
                            name = ''
                            time.sleep(2)
                            board.fill(self.game_over_color)
                            self.display_message('Save as:',
                                    self.text_color, self.game_over_color,
                                    self.midpoint, self.midpoint)

                        else:
                            self.display_message(f'{name} was saved to the leaderboard',
                                    self.text_color, self.game_over_color,
                                    self.midpoint, self.midpoint)
                            self.display_message('Press R to play again or Q to quit to menu.', 
                                    self.text_color, self.game_over_color, 
                                    self.midpoint+60,self.midpoint+200)
                            writing = False
                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                        board.fill(self.game_over_color)
                        pg.display.update()
                        self.display_message(f'Save as: {name}',
                                self.text_color, self.game_over_color,
                                self.midpoint, self.midpoint)
                    elif len(name) >= self.max_characters:
                        self.display_message(f'Save as: {name}',
                                self.text_color, self.game_over_color,
                                self.midpoint, self.midpoint)
                    elif event.key >= 48 and event.key <= 57:
                        name = name + chr(event.key)
                        self.display_message(f'Save as: {name}',
                                self.text_color, self.game_over_color,
                                self.midpoint, self.midpoint)
                    elif event.key >= 65 and event.key <= 90:
                        name = name + chr(event.key)
                        self.display_message(f'Save as: {name}',
                                self.text_color, self.game_over_color,
                                self.midpoint, self.midpoint)
                    elif event.key >= 97 and event.key <= 122:
                        name = name + chr(event.key)
                        self.display_message(f'Save as: {name}',
                                self.text_color, self.game_over_color,
                                self.midpoint, self.midpoint)

                pg.display.update()

        return name

    def run(self):
        while self.game_run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    self.update()
                if event.type == pg.KEYDOWN:
                    if self.game_over_menu:
                        if event.key == pg.K_q:
                            self.game_run = False
                        if event.key == pg.K_r:
                            self.game_over_menu = False
                            self.snake.reset()
                        if event.key == pg.K_s and self.score > 0:
                            saved_name = self.enter_name()
                            self.data_handler.save_player(saved_name, self.score)
                            self.score = 0
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
