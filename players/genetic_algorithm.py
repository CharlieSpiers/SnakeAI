import random as rnd
import time

from visualisations.neural_graph_visualiser import Snake_net_visualiser

SNAKES_PER_GENERATION = 10
SNAKES_ON_LOWER_RANDOMNESS = 7
LOWER_MUTATION_RANDOMNESS = 0.
HIGHER_MUTATION_RANDOMNESS = 0.05


class Snake_genetic_net:

    def __init__(self):
        # self.visualiser = Snake_net_visualiser()
        pass

    def get_action(self, state):
        pass

    def send_feedback(self, score):
        pass

    def get_random_weights(self):
        weights = None
        weights = []
        for i in range(1, 8):
            for j in range(16, 19):
                weights.append((i, j, rnd.uniform(-1, 1)))
        for i in range(8, 16):
            for j in range(4, 8):
                weights.append((i, j, rnd.uniform(-1, 1)))
        return weights


if __name__ == '__main__':
    gen_map = Snake_genetic_net()
    vis = Snake_net_visualiser(gen_map.get_random_weights())
    while True:
        time.sleep(3)
        vis.set_edges(gen_map.get_random_weights())
