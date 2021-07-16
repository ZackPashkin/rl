# conda create -n rl -env python=3.7
# conda activate rl
# pip install torch torchvision
# pip install pg

import pygame as pg
from random import randint
from enum import Enum
from collections import namedtuple

pg.init()
font = pg.font.SysFont('arial', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4



Coord = namedtuple('Coordinates','x,y')

BLOCK_SIZE = 20
SPEED = 20



# rgb colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)



class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Coord(self.w/2, self.h/2)
        self.snake = [self.head,
                      Coord(self.head.x-BLOCK_SIZE, self.head.y),
                      Coord(self.head.x-2*BLOCK_SIZE, self.head.y)]



        self.score = 0
        self.food = None
        self._place_food()



    # randomly place food
    def _place_food(self):
        x = randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Coord(x,y)
        if self.food in self.snake:
            self._place_food()



    def play_step(self):
        """collect user input ,
        move,
        check if game over,
         place new food or move,
          update ui and clock
        :return game over and score"""
        # user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.direction == Direction.LEFT
                elif event.key == pg.K_RIGHT:
                    self.direction == Direction.RIGHT
                elif event.key == pg.K_UP:
                    self.direction == Direction.K_UP
                elif event.key == pg.K_DOWN:
                    self.direction == Direction.K_DOWN
        # move
        # update the head
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # check if game over
        gameover = False
        if self._is_collision():
            gameover = True
            return gameover, self.score

        # place new food of just move
        if self.head == self.food:
            self.score +=1
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

        for point in self.snake:
            #draw snake
            pg.draw.rect(self.display, BLUE, pg.Rect(point.x,point.y, BLOCK_SIZE, BLOCK_SIZE))
            pg.draw.rect(self.display, GREEN, pg.Rect(point.x+4,point.y+4, 12, 12))

        # draw food
        pg.draw.rect(self.display, RED, pg.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(self, [0,0])
        pg.display.flip()


    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or \
        self.head.x < 0  or self.head.y > self.h - BLOCK_SIZE or \
        self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        return False

    def _move(self,direction):
        y = self.head.x
        x = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            x += BLOCK_SIZE
        elif direction == Direction.UP:
            x -= BLOCK_SIZE

        self.head = Coord(x,y)




if __name__ == "main":
    game = SnakeGame()
    # game run
    while True:
        gameover, score = game.play_step()
        if gameover == True:
            break
    print(score)
    pg.quit()
