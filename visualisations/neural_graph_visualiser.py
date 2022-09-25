from pyvis.network import Network
import selenium.common.exceptions
from selenium import webdriver

from visualisations import paths

Graph = None

RED = '#9f0000'
GREEN = '#009f00'
BLUE = '#00009f'


class Snake_net_visualiser:
    # 1-11 are input nodes, 12-13 are hidden nodes for the direction of the food, 14-16 are output nodes
    # Format: n_id, label, color, x, y
    nodes = [(0, 'coll_ahead', BLUE, 300, 50),
             (1, 'coll_right', BLUE, 400, 50),
             (2, 'coll_left', BLUE, 500, 50),

             (3, 'dir_r', BLUE, 50, 450),
             (4, 'dir_l', BLUE, 150, 450),
             (5, 'dir_u', BLUE, 250, 450),
             (6, 'dir_d', BLUE, 350, 450),

             (7, 'food_r', BLUE, 450, 450),
             (8, 'food_l', BLUE, 550, 450),
             (9, 'food_u', BLUE, 650, 450),
             (10, 'food_d', BLUE, 750, 450),

             (11, 'hidden_1', GREEN, 250, 250),
             (12, 'hidden_2', GREEN, 350, 250),
             (13, 'hidden_3', GREEN, 450, 250),
             (14, 'hidden_4', GREEN, 550, 250),

             (15, 'out_ahead', RED, 300, 150),
             (16, 'out_right', RED, 400, 150),
             (17, 'out_left', RED, 500, 150)]

    def __init__(self, edges=None):
        self.edges = edges
        self.graph = None
        self.driver = webdriver.Chrome(executable_path=paths.Path_to_chromium)
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
        self.graph.write_html(paths.Path_to_html)
        self.driver.get(paths.Path_to_html)

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
        self.graph.write_html(paths.Path_to_html)
        try:
            self.driver.refresh()
        except selenium.common.exceptions.WebDriverException:
            print("There was an exception reaching chrome, it was likely closed")
            quit(1)
