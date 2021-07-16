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
final_score = 0


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
        self.clock = pg.tiem.Clock()

        self.direction = Direction.RIGHT

        self.head = Coord([self.w/2, self.h/2])
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


        def play_step():
            """collect user input ,
            move,
            check if game over,
             place new food or move,
              update ui and clock
            :return game over and score"""

            self._update_ui()
            self.clock.tick()

        def _update_ui(self):
            self.display.fill(BLACK)

            for point in self.snake:
                #draw snake
                pg.draw.rect(self.display, BLUE, pg.Rect(point.x,point.y, BLOCK_SIZE, BLOCK_SIZE))
                pg.draw.rect(self.display, GREEN, pg.Rect(point.x+4,point.y+4, 12, 12))

            # draw food
            pg.draw(self.display, RED, pg.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

            text = font.render(f"Score: {self.score}", True, WHITE)
            self.display.blit(self, 0,0)
            pg.display.flip()

            gameover = False
            return gameover, self.score









if __name__ == "main":
    game = SnakeGame()
    # game run
    while True:
        gameover, score = game.play_step()
        if gameover == True:
            break
    print(final_score)
    pg.quit()
