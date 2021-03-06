from random import randint, sample
import random
import numpy as np
import pygame
import torch
import pickle


from collections import deque
from Game_Class import Game
from Models import Linear_Qnet,Q_trainer

white = pygame.Color(255, 255, 255)
pygame.init()
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
BLOCK_SIZE = 20

DIFFICULTY = 30

class Player :
    def __init__(self) -> None:
        self.number_of_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_Qnet(13,256,3)
        self.trainer = Q_trainer(model=self.model,learning_rate=LEARNING_RATE,gamma=self.gamma)

        
    def get_state(self,game):
        head = game.snake.snake_pos
        point_l =[head[0] - BLOCK_SIZE, head[1]]
        point_r = [head[0] + BLOCK_SIZE, head[1]]
        point_u = [head[0], head[1] - BLOCK_SIZE]
        point_d = [head[0], head[1] + BLOCK_SIZE]

        dir_l = game.snake.direction == "LEFT"
        dir_r = game.snake.direction == "RIGHT"
        dir_u = game.snake.direction == "UP"
        dir_d = game.snake.direction == "DOWN"


        state = [
            # Danger straight
            (dir_r and game.snake.check_for_collision(point_r)) or 
            (dir_l and game.snake.check_for_collision(point_l)) or 
            (dir_u and game.snake.check_for_collision(point_u)) or 
            (dir_d and game.snake.check_for_collision(point_d)),

            # Danger right
            (dir_u and game.snake.check_for_collision(point_r)) or 
            (dir_d and game.snake.check_for_collision(point_l)) or 
            (dir_l and game.snake.check_for_collision(point_u)) or 
            (dir_r and game.snake.check_for_collision(point_d)),

            # Danger left
            (dir_d and game.snake.check_for_collision(point_r)) or 
            (dir_u and game.snake.check_for_collision(point_l)) or 
            (dir_r and game.snake.check_for_collision(point_u)) or 
            (dir_l and game.snake.check_for_collision(point_d)),

            # block left
            game.snake.block_left(),
            #block right
            game.snake.block_right(),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.food_pos[0] < head[0],  # food left
            game.food.food_pos[0] > head[0],  # food right
            game.food.food_pos[1] < head[1],  # food up
            game.food.food_pos[1]> head[1]  # food down
            ]
        return np.array(state, dtype=int)
    def ramemeber(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            samples = random.sample(self.memory,BATCH_SIZE)
        else:
            samples = self.memory
        states,actions,rewards,next_states,dones = zip(*samples)
        self.trainer.train_step(states,actions,rewards,next_states,dones)
    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    def get_action(self,state):
        self.epsilon = 80 -self.number_of_games
        action =[0,0,0]
        if random.randint(1,200) < self.epsilon :
            next_move = random.randint(0,2)
            action[next_move]=1
        else :
            tensor_state = torch.tensor(state,dtype=torch.float)
            prediction = self.model(tensor_state)
            next_move = torch.argmax(prediction).item()
            action[next_move]=1
        return action

def play():
    best_score = 0
    player =Player()
    game =Game(DIFFICULTY)
    with open('data/max_score', 'rb') as score_file : 
        saved_score = pickle.load(score_file) 
    while True:
        old_state = player.get_state(game)
        final_move = player.get_action(old_state)
        #print(final_move)
        reward, done ,score =game.play_step(action=final_move,generation=player.number_of_games)
        new_state = player.get_state(game)

        player.train_short_memory(old_state,final_move,reward,new_state,done)
        player.ramemeber(old_state,final_move,reward,new_state,done)

        if done:
            game.restart()
            player.number_of_games+=1
            player.train_long_memory()

            if score > best_score:
                best_score = score
                if best_score > saved_score:
                    with open('data/max_score', 'wb') as score_file :
                        pickle.dump(best_score,score_file)
                    player.model.save()

            
            print("Gen: :",player.number_of_games,"|score : ",score,"|best score :",best_score)

if __name__ == "__main__":
    play()