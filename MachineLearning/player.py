from enum import Enum
import random

import numpy as np
import pygame

from Board.point import Point


class Direction(Enum):
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP = Point(0, -1)


class Player:

    def __init__(self):
        self.direction = Direction.RIGHT

    def get_direction(self):
        pass

    def send_feedback(self, reward, state, done):
        pass

    @staticmethod
    def check_quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


class HumanPlayer(Player):

    def get_direction(self):
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


class AIPlayer(Player):

    def get_direction(self):
        for event in pygame.event.get():
            super().check_quit(event)

        action = self.random_action()  # TODO: model.get_action
        dirs_clockwise = list(Direction)
        curr_index = dirs_clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            return self.direction
        elif np.array_equal(action, [0, 1, 0]):
            self.direction = dirs_clockwise[(curr_index+1) % 4]
            return self.direction
        elif np.array_equal(action, [0, 0, 1]):
            self.direction = dirs_clockwise[(curr_index-1) % 4]
            return self.direction
        else:
            raise BadAIArrayError

    @staticmethod
    def random_action():
        rnd_int = random.randint(0, 2)
        action = [0, 0, 0]
        action[rnd_int] = 1
        return action


class BadAIArrayError(Exception):
    pass
