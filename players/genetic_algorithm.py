import random as rnd

from visualisations.paths import Default_network_file_path as Default_path
from visualisations.neural_graph_visualiser import Snake_net_visualiser
from players.network_file_parser import parse_edges_from_file, ParserException, EmptyEdgeListException

SNAKES_PER_GENERATION = 10
SNAKES_ON_LOWER_VARIANCE = 7
# bounds for how much the snake's network weights can change
LOWER_MUTATION_VARIANCE = 0.05
HIGHER_MUTATION_VARIANCE = 0.20


class Snake_genetic_net:
    snake_nets = None

    def __init__(self, file_path=Default_path):
        self.file_path = file_path
        self.edges = self.get_edges()

        print(self.edges)
        self.visualiser = Snake_net_visualiser()
        pass

    def get_action(self, state):
        pass

    def send_feedback(self, score):
        pass

    def get_edges(self):
        edge_array = []
        try:
            parsed_edges = parse_edges_from_file(self.file_path)
            edge_array = parsed_edges[0:10]
        except ParserException:
            print("There was a exception parsing the file, resorting to random edge weights")
        except EmptyEdgeListException:
            print("There were no edges in the file, using random weights")
        finally:
            for i in range(SNAKES_PER_GENERATION - len(edge_array)):
                edge_array.append(self.get_random_weights())
            return edge_array

    @staticmethod
    def get_random_weights():
        weights = []
        for i in range(1, 8):
            for j in range(16, 19):
                weights.append((i, j, rnd.uniform(-1, 1)))
        for i in range(8, 16):
            for j in range(4, 8):
                weights.append((i, j, rnd.uniform(-1, 1)))
        return weights


if __name__ == '__main__':
    Snake_genetic_net()
    # gen_map = Snake_genetic_net()
    # vis = Snake_net_visualiser(gen_map.get_random_weights())
    # while True:
    #     time.sleep(3)
    #     vis.set_edges(gen_map.get_random_weights())
