import pygame, sys, time, random

from pygame.constants import KEYDOWN

from Snake_class import Snake
from Food_Class import Food

class Game:
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    def __init__(self) -> None:
        self.snake = Snake()
        self.food = Food()
        self.difficulty = 25
        self.frame_size_x = 720
        self.frame_size_y = 480
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        self.fps_controller = pygame.time.Clock()
        self.iteration =0
    def play(self):
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
        
    def play_step(self,action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        reward = 0
        self.snake.set_next_move(action)
        self.snake.set_direction()
        self.snake.move()
        self.snake.snake_add()
        self.snake.eat_food(self.food)
        # Spawning food on the screen
        if self.food.food_not_spawn():
            self.food.update()
            reward = 10
        self.food.spawn()
        collision = self.snake.check_for_collision()
        self.game_window.fill(self.black)
        self.snake.display(self.game_window)

        # self.Snake food
        self.food.display(self.game_window)

         # Game Over conditions
        # Getting out of bounds

        self.snake.show_score(1, self.white, 'consolas', 20,self.game_window)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(self.difficulty)
        self.iteration+=1
        if collision or self.iteration > 100 * len (self.snake.snake_body):
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
            print(reward)
            if gameover :
                self.__init__()
        