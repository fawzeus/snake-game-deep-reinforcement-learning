import pygame, sys, time, random

from Snake_class import Snake
from Food_Class import Food



# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

pygame.init()


# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

snake = Snake()
food = Food()


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                snake.set_next_move ('UP')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                snake.set_next_move('DOWN')
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                snake.set_next_move('LEFT')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                snake.set_next_move('RIGHT')
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    snake.set_direction()

    # Moving the snake
    if snake.direction == 'UP':
        snake.move_up()
    if snake.direction == 'DOWN':
       snake.move_down()
    if snake.direction == 'LEFT':
        snake.move_left()
    if snake.direction == 'RIGHT':
        snake.move_right()

    # Snake body growing mechanism
    snake.snake_add()
    snake.eat_food(food)
    # Spawning food on the screen
    if food.food_not_spawn():
        food.update()
    food.spawn()

    # GFX
    game_window.fill(black)
    snake.display(game_window)

    # Snake food
    food.display(game_window)

    # Game Over conditions
    # Getting out of bounds
    snake.check_for_gameover(game_window)

    snake.show_score(1, white, 'consolas', 20,game_window)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)