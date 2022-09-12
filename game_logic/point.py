from collections import namedtuple
import random

import pygame

# pure
Point = namedtuple('point', 'x, y')


# pure
def pt_random(width, height):
    x = random.randint(0, (width - 1))
    y = random.randint(0, (height - 1))
    return Point(x, y)


# applicative instance
def pt_add(point, point2):
    (x, y) = point
    (x2, y2) = point2
    return Point(x + x2, y + y2)


# functor
def pt_fmap(point, f):
    return Point(f(point.x), f(point.y))


def pt_not_in_bounds(x_bound, y_bound, point):
    return not (0 <= point.x <= x_bound-1 and 0 <= point.y <= y_bound-1)


def pt_rect(block_size, point=Point(0, 0)):
    x, y = pt_fmap(point, lambda a: a * block_size)
    rect1 = pygame.Rect(x, y, block_size, block_size)
    rect2 = pygame.Rect(x + block_size / 5, y + block_size / 5, block_size * 3 / 5, block_size * 3 / 5)
    return rect1, rect2
