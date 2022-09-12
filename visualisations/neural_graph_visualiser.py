from pyvis.network import Network

Graph = None

RED = '#9f0000'
GREEN = '#009f00'
BLUE = '#00009f'


class Snake_genetic_net:
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
        self.edges = edges()

    def get_action(self, state):
        pass

    def get_graph(self):
        g = Network(width=800, height=500, heading='Neural network', bgcolor='#000000', font_color='#ffffff')
        for node in self.nodes:
            g.add_node(n_id=node[0], label=node[1], color=node[2], x=node[3], y=node[4],
                       physics=False, labelHighlightBold=True, borderWidth=5)
        for edge in self.edges:
            if edge[2] < 0:
                g.add_edge(edge[0], edge[1], value=abs(edge[2])*0.5, title=edge[2], color=RED)
            else:
                g.add_edge(edge[0], edge[1], value=abs(edge[2]*0.5), title=edge[2], color=GREEN)
        g.show('graphs/test.html')


if __name__ == '__main__':
    genetic = Snake_genetic_net()
    genetic.get_graph()
