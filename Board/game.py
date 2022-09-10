import pygame

from Board.player import HumanPlayer
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

    def __init__(self, w=32, h=32):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w * BLOCK_SIZE, self.h * BLOCK_SIZE))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.player = HumanPlayer()

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, pt_add(self.head, (-1, 0)), pt_add(self.head, (-2, 0))]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        self.food = pt_random(self.w, self.h)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        direction = self.player.get_input()

        # 2. move
        self.head = pt_add(self.head, direction.value)
        self.snake.insert(0, self.head)

        # 3. check if game over
        if self._is_collision():
            return True, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return False, self.score

    def _is_collision(self, pt=None):
        if not pt:
            pt = self.head
        # Check if in bounds and not inside itself
        return pt_not_in_bounds(self.w, self.h, pt) or self.head in self.snake[1:]

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
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()
