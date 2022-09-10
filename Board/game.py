import pygame

from MachineLearning.player import HumanPlayer, AIPlayer
from Board.point import Point, pt_add, pt_random, pt_rect, pt_not_in_bounds

pygame.init()
font = pygame.font.Font('../arial.ttf', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:
    score = None
    food = None
    head = None
    snake = None
    game_turns = None

    def __init__(self, w=32, h=32, player=HumanPlayer()):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w * BLOCK_SIZE, self.h * BLOCK_SIZE))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.player = player
        self.reset()

    def reset(self):
        self.score = 0
        self.food = None
        self.game_turns = 0
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, pt_add(self.head, (-1, 0)), pt_add(self.head, (-2, 0))]

        self._place_food()

    def _place_food(self):
        self.food = pt_random(self.w, self.h)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input and move
        self.game_turns += 1
        self.head = pt_add(self.head, self.player.get_direction().value)
        self.snake.insert(0, self.head)

        # 2. check if game over
        snake_reward = 0
        if self._is_collision() or self.game_turns > 1000*len(self.snake):
            snake_reward = -10
            return snake_reward, True, self.score

        # 3. place new food or just move
        if self.head == self.food:
            self.score += 1
            snake_reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 4. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 5. return game over and score
        return snake_reward, False, self.score

    def _is_collision(self, pt=None):
        if not pt:
            pt = self.head
        # Check if in bounds and not inside itself
        return pt_not_in_bounds(self.w, self.h, pt) or pt in self.snake[1:]

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            outer, inner = pt_rect(BLOCK_SIZE, pt)
            pygame.draw.rect(self.display, BLUE1, outer)
            pygame.draw.rect(self.display, BLUE2, inner)

        pygame.draw.rect(self.display, RED, pt_rect(BLOCK_SIZE, self.food)[0])

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        reward, game_over, score = game.play_step()
        game.player.send_feedback(reward, game.get_state())

        if game_over:
            game.reset()
