# conda create -n rl -env python=3.7
# conda activate rl
# pip install torch torchvision
# pip install pg

import pygame as pg
from random import randint
from enum import Enum
from collections import namedtuple
# add numpy
import numpy as np

pg.init()
font = pg.font.SysFont('arial', 25)


# reset
# reward
# play(action) -> direction
# is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Coord = namedtuple('Coord', 'x,y')
BLOCK_SIZE = 20
SPEED = 2
# rgb colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class SnakeGameRL:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption('Snake Game')
        self.clock = pg.time.Clock()
        self.reset()
        # remove direction to reset()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Coord(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Coord(self.head.x - BLOCK_SIZE, self.head.y),
                      Coord(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        # keep track of game iteration
        self.frame_iteration = 0

    # randomly place food
    def _place_food(self):
        x = randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Coord(x, y)
        if self.food in self.snake:
            self._place_food()

    # change play step for frame iteration
    def play_step(self, action):
        """collect user input ,
        move,
        check if game over,
         place new food or move,
          update ui and clock
        :return game over and score"""
        # user input
        # add iteration +=1
        self.frame_iteration += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pg.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pg.K_UP:
            #         self.direction = Direction.UP
            #     elif event.key == pg.K_DOWN:
            #         self.direction = Direction.DOWN
        # move


        self._move(action)
        # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        # add reward eat food: +10 , game over: -10 else 0
        reward = 0
        gameover = False
        # if self._is_collision():
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            gameover = True
            reward += 10
            # update return to: return reward, gameover, self.score
            return reward, gameover, self.score

        # 4 .place new food of just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # return game over snd score
        return gameover, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for p in self.snake:
            # draw snake
            pg.draw.rect(self.display, BLUE, pg.Rect(p.x, p.y, BLOCK_SIZE, BLOCK_SIZE))
            pg.draw.rect(self.display, GREEN, pg.Rect(p.x + 1, p.y + 1, 12, 12))

        # draw food
        pg.draw.rect(self.display, RED, pg.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pg.display.flip()

    # change to public
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or \
                pt.x < 0 or pt.y > self.h - BLOCK_SIZE or \
                pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

    # change def _move(self, direction) --> def _move(self, action)

    # action
    # [1,0,0] -> straight
    # [0,1,0] -> right turn
    # [0,0,1] -> left turn
    def _move(self, action):

        # add directions
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            # prevent out of list
            next_idx = (idx + 1) % 4
            # right turn r -> d -> l -> u
            new_direction = clock_wise[next_idx]
        else:  # [0,0,1]
            next_idx = (idx - 1) % 4
            # left turn r -> u -> l -> d
            new_direction = clock_wise[next_idx]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Coord(x, y)

# if __name__ == "__main__":
#     game = SnakeGame()
#     # game run
#     while True:
#         gameover, score = game.play_step()
#         if gameover == True:
#             break
#     print(score)
#     pg.quit()
