import random as rnd


class Snake_genetic_net:

    def __init__(self):
        # self.visualiser = Snake_net_visualiser()
        pass

    def get_action(self, state):
        pass

    def send_feedback(self, score):
        pass

    def get_random_weights(self):
        weights = []
        for i in range(1, 10):
            for j in range(14, 17):
                weights.append((i, j, rnd.uniform(-1, 1)))
        for i in range(10, 15):
            for j in range(8, 10):
                weights.append((i, j, rnd.uniform(-1, 1)))
        return weights