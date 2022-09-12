import time

from pyvis.network import Network
from players.genetic_algorithm import Snake_genetic_net
from selenium import webdriver
from visualisations import path_to_chromium as path

Graph = None

RED = '#9f0000'
GREEN = '#009f00'
BLUE = '#00009f'


class Snake_net_visualiser:
    # 1-11 are input nodes, 12-13 are hidden nodes for the direction of the food, 14-16 are output nodes
    # Format: n_id, label, color, x, y
    nodes = [(1, 'coll_ahead', BLUE, 100, 50),
             (2, 'coll_right', BLUE, 200, 50),
             (3, 'coll_left', BLUE, 300, 50),

             (4, 'dir_r', BLUE, 400, 50),
             (5, 'dir_l', BLUE, 500, 50),
             (6, 'dir_u', BLUE, 600, 50),
             (7, 'dir_d', BLUE, 700, 50),

             (8, 'hidden_1', GREEN, 300, 350),
             (9, 'hidden_2', GREEN, 500, 350),

             (10, 'food_r', BLUE, 100, 450),
             (11, 'food_l', BLUE, 300, 450),
             (12, 'food_u', BLUE, 500, 450),
             (13, 'food_d', BLUE, 700, 450),

             (14, 'out_ahead', RED, 300, 250),
             (15, 'out_right', RED, 400, 250),
             (16, 'out_left', RED, 500, 250)]

    def __init__(self, edges=None):
        self.edges = edges
        self.graph = None
        self.driver = webdriver.Chrome(path.Path_to_chromium)
        self.driver.maximize_window()
        if edges is not None:
            self.show_graph()

    def show_graph(self):
        self.graph = Network(width=800, height=500, heading='Neural network', bgcolor='#000000', font_color='#ffffff')
        for node in self.nodes:
            self.graph.add_node(n_id=node[0], label=node[1], color=node[2], x=node[3], y=node[4],
                                physics=False, labelHighlightBold=True, borderWidth=5)
        for edge in self.edges:
            if edge[2] < 0:
                self.graph.add_edge(edge[0], edge[1], value=abs(edge[2]) * 0.5, title=edge[2], color=RED)
            else:
                self.graph.add_edge(edge[0], edge[1], value=abs(edge[2] * 0.5), title=edge[2], color=GREEN)
        self.graph.write_html('test.html')
        self.driver.get('C:/Users/charl/PycharmProjects/SnakeAI/visualisations/test.html')

    def set_edges(self, edges):
        self.edges = edges
        for i, edge in enumerate(self.graph.get_edges()):
            new_edge = self.edges[i]
            edge['value'] = abs(new_edge[2])
            edge['title'] = new_edge[2]
            if new_edge[2] < 0:
                edge['color'] = RED
            else:
                edge['color'] = GREEN
        self.graph.write_html('test.html')
        self.driver.refresh()


if __name__ == '__main__':
    gen_map = Snake_genetic_net()
    vis = Snake_net_visualiser(gen_map.get_random_weights())
    while True:
        time.sleep(3)
        vis.set_edges(gen_map.get_random_weights())
