import random
import pygame
frame_size_x = 720
frame_size_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class Food :
    def __init__(self) -> None:
        self.food_spawn=True
        self.food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        while self.food_pos in [[100, 50], [100-10, 50], [100-(2*10), 50]]:
            self.food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
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
        self.food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    def display(self,game_window):
        pygame.draw.rect(game_window, red, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))