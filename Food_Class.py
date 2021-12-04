import random
import pygame

BLOCK_SIZE = 20

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
grey = pygame.Color(149,149,149)
class Food :
    def __init__(self,w=640,h=480) -> None:
        self.food_spawn=True
        self.w=w
        self.h=h
        self.food_pos = [random.randrange(1, ((self.w-BLOCK_SIZE)//BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, ((self.h-BLOCK_SIZE)//BLOCK_SIZE)) * BLOCK_SIZE]
    def food_not_spawn(self):
        return not self.food_spawn
    def x(self):
        return self.food_pos[0]
    def y(self):
        return self.food_pos[1]
    def spawn(self):
        self.food_spawn=True
    def not_spawn(self):
        self.food_spawn=False
    def update(self):
        self.food_pos = [random.randrange(1, ((self.w-BLOCK_SIZE)//BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, ((self.h-BLOCK_SIZE)//BLOCK_SIZE)) * BLOCK_SIZE]
    def display(self,game_window):
        x = self.food_pos[0]+BLOCK_SIZE//2 
        y = self.food_pos[1]+BLOCK_SIZE//2
        pygame.draw.circle(game_window,red,(x,y),BLOCK_SIZE/2)
        #pygame.draw.rect(game_window, red, pygame.Rect(self.food_pos[0], self.food_pos[1], BLOCK_SIZE, BLOCK_SIZE))