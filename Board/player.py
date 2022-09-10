from enum import Enum

import pygame

from Board.point import Point


class Direction(Enum):
    RIGHT = Point(1, 0)
    LEFT = Point(-1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)


class Player:

    def get_input(self):
        pass

    @staticmethod
    def check_quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


class HumanPlayer(Player):

    def __init__(self):
        self.direction = Direction.RIGHT

    def get_input(self):
        input_found = False
        for event in pygame.event.get():
            super().check_quit(event)
            if (event.type == pygame.KEYDOWN) & (not input_found):
                input_found = True
                if (event.key == pygame.K_LEFT) & (self.direction != Direction.RIGHT):
                    self.direction = Direction.LEFT
                elif (event.key == pygame.K_RIGHT) & (self.direction != Direction.LEFT):
                    self.direction = Direction.RIGHT
                elif (event.key == pygame.K_UP) & (self.direction != Direction.DOWN):
                    self.direction = Direction.UP
                elif (event.key == pygame.K_DOWN) & (self.direction != Direction.UP):
                    self.direction = Direction.DOWN
                else:
                    input_found = False
        return self.direction
