import pygame
import time
import sys
import numpy as np
from pygame.event import set_blocked


BLOCK_SIZE = 20

class Snake:
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    grey = pygame.Color(149,149,149)
    def __init__(self,w=640,h=480) -> None:
        self.h =h
        self.w = w
        self.snake_pos = [self.w//2,self.h//2]
        self.snake_body = [[self.w//2, self.h//2], [self.w//2-BLOCK_SIZE, self.h//2], [self.w//2-(2*BLOCK_SIZE), self.h//2]]
        self.snake_pos = [self.w/2, self.h/2]
        self.snake = [self.snake_pos,
                      [self.snake_pos[0]-BLOCK_SIZE, self.snake_pos[1]],
                      [self.snake_pos[0]-(2*BLOCK_SIZE), self.snake_pos[1]]]
        self.direction = "RIGHT"
        self.next_move = self.direction
        self.score = 0
    def draw_eyes(self,x,y,game_window):
        if self.direction == "LEFT":
            pygame.draw.circle(game_window,self.white,(x+2*BLOCK_SIZE/5,y+BLOCK_SIZE/8),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x+2*BLOCK_SIZE/5,y+BLOCK_SIZE/8),BLOCK_SIZE/20)
            pygame.draw.circle(game_window,self.white,(x+2*BLOCK_SIZE/5,y-BLOCK_SIZE/8),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x+2*BLOCK_SIZE/5,y-BLOCK_SIZE/8),BLOCK_SIZE/20)
        elif self.direction == "RIGHT":
            pygame.draw.circle(game_window,self.white,(x-2*BLOCK_SIZE/5,y+BLOCK_SIZE/8),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x-2*BLOCK_SIZE/5,y+BLOCK_SIZE/8),BLOCK_SIZE/20)
            pygame.draw.circle(game_window,self.white,(x-2*BLOCK_SIZE/5,y-BLOCK_SIZE/8),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x-2*BLOCK_SIZE/5,y-BLOCK_SIZE/8),BLOCK_SIZE/20)
        elif self.direction == "UP":
            pygame.draw.circle(game_window,self.white,(x+BLOCK_SIZE/8,y+2*BLOCK_SIZE/5),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x+BLOCK_SIZE/8,y+2*BLOCK_SIZE/5),BLOCK_SIZE/20)
            pygame.draw.circle(game_window,self.white,(x-BLOCK_SIZE/8,y+2*BLOCK_SIZE/5),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x-BLOCK_SIZE/8,y+2*BLOCK_SIZE/5),BLOCK_SIZE/20)
        else:
            pygame.draw.circle(game_window,self.white,(x+BLOCK_SIZE/8,y-2*BLOCK_SIZE/5),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x+BLOCK_SIZE/8,y-2*BLOCK_SIZE/5),BLOCK_SIZE/20)
            pygame.draw.circle(game_window,self.white,(x-BLOCK_SIZE/8,y-2*BLOCK_SIZE/5),BLOCK_SIZE/6)
            pygame.draw.circle(game_window,self.black,(x-BLOCK_SIZE/8,y-2*BLOCK_SIZE/5),BLOCK_SIZE/20)

    def game_over(self,game_window):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, self.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.w/2, self.h/4)
        game_window.fill(self.black)
        game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, self.red, 'times', 20,game_window)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    def show_score(self,choice, color, font, size,game_window):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.w/10, 15)
        else:
            score_rect.midtop = (self.w/2, self.h/1.25)
        game_window.blit(score_surface, score_rect)
    def move(self,action=None):
        if action :
            moves = ["RIGHT","DOWN","LEFT","UP"]
            idx = moves.index(self.direction)
            if np.array_equal(action,[1,0,0]):
                nex_dir = moves[idx]
            elif np.array_equal(action,[0,1,0]):
                idx+=1
                idx%=4
                nex_dir = moves[idx]
            else :
                idx-=1
                if idx < 0:
                    idx = 3
                nex_dir = moves[idx]
            self.next_move = nex_dir
        self.set_direction()
        if self.direction == 'UP':
            self.move_up()
        if self.direction == 'DOWN':
            self.move_down()
        if self.direction == 'LEFT':
            self.move_left()
        if self.direction == 'RIGHT':
            self.move_right()
    def move_up(self):
        self.snake_pos[1] -= BLOCK_SIZE
    def move_down(self):
        self.snake_pos[1] += BLOCK_SIZE
    def move_right(self):
        self.snake_pos[0] += BLOCK_SIZE
    def move_left(self):
        self.snake_pos[0] -= BLOCK_SIZE
    def set_direction(self):
        # Making sure the snake cannot move in the opposite snake.direction instantaneously
        if self.next_move == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.next_move == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.next_move == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.next_move == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    def x(self):
        return self.pos[0]
    def y(self):
        return self.pos[1]
    def check_for_gameover(self,game_window):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.w-BLOCK_SIZE:
            self.game_over(game_window)
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.h-BLOCK_SIZE:
            self.game_over(game_window)
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over(game_window)
    def check_for_collision(self,pt=None):
        if pt is None:
            pt =self.snake_pos
        if pt[0] < 0 or pt[0] > self.w-BLOCK_SIZE:
            return True
        if pt[1] < 0 or pt[1] > self.h-BLOCK_SIZE:
            return True
        # Touching the snake body
        for block in self.snake_body[1:]:
            if pt[0] == block[0] and pt[1] == block[1]:
                return True
        return False
    def set_next_move(self,move):
        self.next_move=move
    def display(self,game_window):
        #print("display")
        #print(self.snake_body)
        #pygame.draw.rect(game_window, self.green, pygame.Rect(self.snake_pos[0], self.snake_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        x = self.snake_pos[0]+BLOCK_SIZE//2 
        y = self.snake_pos[1]+BLOCK_SIZE//2
        pygame.draw.circle(game_window,self.green,(x,y),BLOCK_SIZE/2)
        self.draw_eyes(x,y,game_window)
        for pos in self.snake_body[1:]:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            x = pos[0]+BLOCK_SIZE//2 
            y = pos[1]+BLOCK_SIZE//2
            pygame.draw.circle(game_window,self.green,(x,y),BLOCK_SIZE/2)
            #pygame.draw.rect(game_window, self.blue, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    def snake_add(self):
        self.snake_body.insert(0, list(self.snake_pos))

    def block_left(self):
        if self.direction == "RIGHT" :
            for point in self.snake_body[1:]:
                if self.snake_pos[0] == point[0] and self.snake_pos[1] > point[1]:
                    return True
            return False
        elif self.direction =="LEFT" :
            for point in self.snake_body[1:]:
                if self.snake_pos[0] == point[0] and self.snake_pos[1] < point[1] :
                    return True
            return False
        elif self.direction == "UP":
            for point in self.snake_body[1:]:
                if self.snake_pos[1] == point[1] and self.snake_pos[0] > point[0]:
                    return True
            return False
        elif self.direction == "DOWN" :
            for point in self.snake_body[1:]:
                if self.snake_pos[1] == point[1] and self.snake_pos[0] < point[0]:
                    return True
            return False
        return False
    def block_right(self):
        if self.direction == "RIGHT" :
            for point in self.snake_body[1:]:
                if self.snake_pos[0] == point[0] and self.snake_pos[1] < point[1]:
                    return True
            return False
        elif self.direction =="LEFT" :
            for point in self.snake_body[1:]:
                if self.snake_pos[0] == point[0] and self.snake_pos[1] > point[1] :
                    return True
            return False
        elif self.direction == "UP":
            for point in self.snake_body[1:]:
                if self.snake_pos[1] == point[1] and self.snake_pos[0] < point[0]:
                    return True
            return False
        elif self.direction == "DOWN" :
            for point in self.snake_body[1:]:
                if self.snake_pos[1] == point[1] and self.snake_pos[0] > point[0]:
                    return True
            return False
        return False
    def snake_remove(self):
        self.snake_body.pop()
    def eat_food(self,food):
        if self.snake_pos[0] == food.x() and self.snake_pos[1] == food.y():
            self.score += 1
            food.not_spawn()
        else:
            self.snake_remove()