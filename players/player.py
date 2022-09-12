from enum import Enum

import numpy as np
import pygame

from Board.point import Point
from visualisations.neural_graph_visualiser import Snake_genetic_net


class Direction(Enum):
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP = Point(0, -1)


class Player:

    def __init__(self):
        self.direction = Direction.RIGHT

    def get_direction(self, state=None):
        pass

    def send_feedback(self, reward, state, done, score):
        pass

    @staticmethod
    def check_quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


class HumanPlayer(Player):

    def get_direction(self, state=None):
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
    ai = None

    def __init__(self, state):
        super().__init__()
        self.ai = Snake_genetic_net()

    def get_direction(self, state=None):
        if state is None:
            raise BadStateError

        for event in pygame.event.get():
            super().check_quit(event)

        action = self.ai.get_action(state)
        dirs_clockwise = list(Direction)
        curr_index = dirs_clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            return self.direction
        elif np.array_equal(action, [0, 1, 0]):
            self.direction = dirs_clockwise[(curr_index + 1) % 4]
            return self.direction
        elif np.array_equal(action, [0, 0, 1]):
            self.direction = dirs_clockwise[(curr_index - 1) % 4]
            return self.direction
        else:
            raise BadAIArrayError

    # def send_feedback(self, reward, new_state, done, score):
    #     self.ag.train_short_memory(self.old_state, self.last_action, reward, new_state, done)
    #     self.ag.remember(self.old_state, self.last_action, reward, new_state, done)
    #     if done:
    #         self.ag.do_done(score)
    #     self.old_state = new_state


class BadAIArrayError(Exception):
    pass


class BadStateError(Exception):
    pass
