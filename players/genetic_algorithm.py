import random

import numpy as np


class Snake_genetic_net:

    def __init__(self, neural_net_edges=None, input_nodes=None, hidden_nodes=None, output_nodes=None):
        if neural_net_edges is None:
            raise BadEdgeException("Neural net was None")

        if (input_nodes is None) or (hidden_nodes is None) or (output_nodes is None):
            input_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            hidden_nodes = [11, 12, 13, 14]
            output_nodes = [15, 16, 17]

        # There should be some tests for if these are suitable if you want to expand this to use any network
        # E.g. input_nodes = [0..a], hidden = [b..c], output = [d..e], a+1 = b, c+1 = d, e-d = 2
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.edges = neural_net_edges

    # Called once per move
    def get_action(self, state):
        if len(state) is not len(self.input_nodes):
            raise BadStateException("Wrong length")

        outputs = []
        for v in state:
            outputs.append(v)
        for i in self.hidden_nodes + self.output_nodes:
            outputs.append(0)

        for start, end, weight in self.edges:
            outputs[end] += outputs[start] * weight

        action = [0, 0, 0]
        move = np.argmax(outputs[-3:])
        action[move] = 1
        return action

    def update_visualisations(self, visualiser):
        visualiser.set_edges(self.edges)

    def generate_new_snake(self, max_variance=None):
        new_edges = []
        for start, end, weight in self.edges:
            weight_difference = round(max_variance * random.uniform(-1, 1), 3)
            new_edges.append((start, end, weight + weight_difference))#
        np.clip(new_edges, -1, 1)
        return Snake_genetic_net(new_edges, self.input_nodes, self.hidden_nodes, self.output_nodes)


class BadStateException(Exception):
    pass


class BadEdgeException(Exception):
    pass
