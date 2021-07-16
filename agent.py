import torch
from random import sample, randint
import numpy as np

from collections import deque
from snake_game_rl import SnakeGameRL, Direction, Coord, BLOCK_SIZE

# need to get state where we are aware of the current environment: state=get_state(game)
# calculate the next move from the state: action = get_move(state) ,model.predict()
# update to the next state and call reward, gameover, score = game.play_step(action)
# calculate the new state again : new_state = get_state(game)
# store everything in cache
# train our model
# we need to store the game and model in this class

MAX_CACHE = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.num_games = 0
        self.epsilon = 0 # to control randomness
        self.gamma = 0
        self.memory = deque(maxlen=MAX_CACHE) # popleft()
        self.model = None
        self.trainer = None

    def get_state(self, game):
        head = game.snake[0]
        point_l = Coord(head.x - BLOCK_SIZE, head.y)
        point_r = Coord(head.x + BLOCK_SIZE, head.y)
        point_u = Coord(head.x, head.y - BLOCK_SIZE)
        point_d = Coord(head.x, head.y + BLOCK_SIZE)

        # current direction is bool
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            # dependent on cur direction
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
        ]
        # convert ro 0 1
        return np.array(state, dtype=int)
    # done is current gameover state
    def remember(self, state, action, reward, next_state, done ):
        # store in tuple format
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        # fetch 1000 batch to memory ,
        # check it first
        if len(self.memory) > BATCH_SIZE:
            mini_sample = sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory

        # unpack mini_sample
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward , next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self):
        # random moves: tradeoff exploration / explotation
        self.epsilon = 80 - self.num_games
        final_move = []
        if randint(0, 200) < self.epsilon:
            move = randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move





def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameRL()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        # ------------------------------
        reward, done, score = game.play_step((final_move))
        state_new = agent.get_state(game)
        # ------------------------------

        # train short memory (only for one step)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            # train long memory
            # replay memory
            game.reset()
            agent.num_games += 1

            if score > record:
                record = score
                # agent.model.save()


            print(f"Game: {agent.num_games}")
            print(f"Score: {score}")
            print(f"Record: {record}")








if __name__ == '__main__':
    train()





