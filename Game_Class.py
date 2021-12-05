import pygame, sys, time, random

from pygame.constants import KEYDOWN

from Snake_class import Snake
from Food_Class import Food
pygame.init()

class Game:
    score_font = pygame.font.SysFont('consolas', 20)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    def __init__(self,difficulty,w=640,h=480) -> None:
        self.snake = Snake()
        self.food = Food()
        self.difficulty = difficulty
        self.frame_size_x = w
        self.frame_size_y = h
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        self.fps_controller = pygame.time.Clock()
        self.iteration =0
        self.score_surface = None
        self.score_rect = None
    def restart(self):
        diff = self.difficulty
        self.__init__(diff)
    def play(self):
        i = 0
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.snake.set_next_move ('UP')
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.snake.set_next_move('DOWN')
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.snake.set_next_move('LEFT')
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.snake.set_next_move('RIGHT')
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            self.snake.set_direction()

            # Moving the self.snake
            self.snake.move()
            # self.Snake body growing mechanism
            self.snake.snake_add()
            self.snake.eat_food(self.food)
            # Spawning food on the screen
            if self.food.food_not_spawn():
                self.food.update()
            self.food.spawn()
            # GFX
            self.game_window.fill(self.black)
            self.snake.display(self.game_window)

            # self.Snake food
            self.food.display(self.game_window)

            # Game Over conditions
            # Getting out of bounds
            self.snake.check_for_gameover(self.game_window)

            self.snake.show_score(1, self.white, 'consolas', 20,self.game_window)
            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            self.fps_controller.tick(self.difficulty)
        
    def play_step(self,action,generation=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        reward = 0
        self.snake.move(action)
        self.snake.snake_add()
        self.snake.eat_food(self.food)
        # Spawning food on the screen
        if self.food.food_not_spawn():
            self.food.update()
            #print(reward)
            reward = 10
        self.food.spawn()
        collision = self.snake.check_for_collision()
        self.game_window.fill(self.black)
        self.snake.display(self.game_window)

        # display food
        self.food.display(self.game_window)

         # Game Over conditions
        # Getting out of bounds

        self.snake.show_score(1, self.white, 'consolas', 20,self.game_window)
        self.score_surface = self.score_font.render('Generation : ' + str(generation), True, self.white)
        self.score_rect = self.score_surface.get_rect()
        self.score_rect.midtop = (640/10+ 180, 15)
        self.game_window.blit(self.score_surface,self.score_rect)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(self.difficulty)
        self.iteration+=1
        if collision or self.iteration > 100 * (self.snake.score +1):
            reward = -10
            return reward,True,self.snake.score
        else :
            return reward ,False,self.snake.score
    def ai_play(self):
        pygame.init()
        while True:
            key =""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        key ='UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        key ='DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        key = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        key = 'RIGHT'
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            reward,gameover,score = self.play_step(key)
            #print(self.snake.snake_body)
            #print(reward)
            if gameover :
                self.__init__(25)
        