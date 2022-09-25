from players.genetic_algorithm import Snake_genetic_net
from players.network_file_parser import parse_edges_from_file, ParserException, EmptyEdgeListException
import random as rnd

from visualisations.neural_graph_visualiser import Snake_net_visualiser
from visualisations.paths import Default_network_file_path as Default_path

SNAKES_PER_GENERATION = 10
SNAKES_ON_HIGHER_VARIANCE = 4
# bounds for how much the snake's network weights can change
LOWER_MUTATION_VARIANCE_MAX = 0.2
HIGHER_MUTATION_VARIANCE_MAX = 0.5


class AI_generation_handler:

    # Create a set of snakes depending on the data provided in the file and the snakes per generation
    def __init__(self, file_path=Default_path):
        self.file_path = file_path
        self.current_snake_index = 0
        self.completed_snakes = []
        self.visualiser = Snake_net_visualiser(self.get_random_weights())
        self.high_score = 0
        self.last_average_score = 0

        self.snakes = []
        for edge in self.get_edges_list():
            self.snakes.append(Snake_genetic_net(edge))

    def get_action(self, state):
        return self.snakes[self.current_snake_index].get_action(state)

    def send_feedback(self, score):
        self.completed_snakes.append((self.current_snake_index, score))
        self.current_snake_index += 1

        if self.current_snake_index != SNAKES_PER_GENERATION:
            self.snakes[self.current_snake_index].update_visualisations(self.visualiser)
        else:  # End of generation
            self.completed_snakes.sort(key=lambda x: x[1])
            self.completed_snakes.reverse()
            self.update_view_scores()
            self.create_new_generation()

    def get_edges_list(self):
        edge_array = []
        try:
            parsed_edges = parse_edges_from_file(self.file_path)
            edge_array = parsed_edges[0:10]
        except ParserException:
            print("There was a exception parsing the file, using random weights")
        except EmptyEdgeListException:
            print("There were no edges in the file, using random weights")
        finally:
            for i in range(SNAKES_PER_GENERATION - len(edge_array)):
                edge_array.append(self.get_random_weights())
            return edge_array

    def update_view_scores(self):
        print(self.completed_snakes)
        gen_high_score = self.completed_snakes[0][1]
        if gen_high_score > self.high_score:
            self.high_score = gen_high_score

        gen_average_score = sum(x for (_, x) in self.completed_snakes)/SNAKES_PER_GENERATION
        self.visualiser.update_scores(self.high_score, self.last_average_score, gen_average_score)
        self.last_average_score = gen_average_score

    def create_new_generation(self):
        first_snake = self.snakes[self.completed_snakes[0][0]]
        second_snake = self.snakes[self.completed_snakes[1][0]]

        self.current_snake_index = 0
        self.completed_snakes = []
        self.snakes = []

        for i in range(0, int((SNAKES_PER_GENERATION-SNAKES_ON_HIGHER_VARIANCE)/2)):
            self.snakes.append(first_snake.generate_new_snake(LOWER_MUTATION_VARIANCE_MAX))
            self.snakes.append(second_snake.generate_new_snake(LOWER_MUTATION_VARIANCE_MAX))

        for i in range(0, int(SNAKES_ON_HIGHER_VARIANCE/2)):
            self.snakes.append(first_snake.generate_new_snake(HIGHER_MUTATION_VARIANCE_MAX))
            self.snakes.append(second_snake.generate_new_snake(HIGHER_MUTATION_VARIANCE_MAX))

    @staticmethod
    def get_random_weights():
        weights = []
        for i in [0, 1, 2, 11, 12, 13, 14]:
            for j in [15, 16, 17]:
                weights.append((i, j, round(rnd.uniform(-1, 1), 3)))
        for i in [3, 4, 5, 6, 7, 8, 9, 10]:
            for j in [11, 12, 13, 14]:
                weights.append((i, j, round(rnd.uniform(-1, 1), 3)))
        return weights
