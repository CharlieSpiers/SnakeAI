import numpy as np
import pygame

from players.genetic_algorithm import Snake_genetic_net
from game_logic.point import Direction


class Player:

    def __init__(self):
        self.direction = Direction.RIGHT

    def get_direction(self, state=None):
        pass

    def send_feedback(self, score):
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

    def __init__(self):
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

    def send_feedback(self, score):
        self.ai.send_feedback(score)


class BadAIArrayError(Exception):
    pass


class BadStateError(Exception):
    pass
