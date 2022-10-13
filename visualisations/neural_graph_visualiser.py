from pyvis.network import Network
import selenium.common.exceptions
from selenium import webdriver
import bs4

from visualisations import paths

Graph = None

RED = '#9f0000'
GREEN = '#009f00'
BLUE = '#00009f'


class Snake_net_visualiser:
    # 1-11 are input nodes, 12-13 are hidden nodes for the direction of the food, 14-16 are output nodes
    # Format: n_id, label, color, x, y
    nodes = [(0, 'coll_ahead', BLUE, 50, 50),
             (1, 'coll_right', BLUE, 50, 150),
             (2, 'coll_left', BLUE, 50, 250),

             (3, 'dir_r', BLUE, 50, 350),
             (4, 'dir_l', BLUE, 50, 450),
             (5, 'dir_u', BLUE, 50, 550),
             (6, 'dir_d', BLUE, 50, 650),
             (7, 'food_r', BLUE, 50, 750),
             (8, 'food_l', BLUE, 50, 850),
             (9, 'food_u', BLUE, 50, 950),
             (10, 'food_d', BLUE, 50, 1050),

             (11, 'hidden_1', GREEN, 250, 200),
             (12, 'hidden_2', GREEN, 250, 300),
             (13, 'hidden_3', GREEN, 250, 400),
             (14, 'hidden_4', GREEN, 250, 500),
             (15, 'hidden_5', GREEN, 250, 600),
             (16, 'hidden_6', GREEN, 250, 700),
             (17, 'hidden_7', GREEN, 250, 800),
             (18, 'hidden_8', GREEN, 250, 900),

             (19, 'out_ahead', RED, 450, 200),
             (20, 'out_right', RED, 450, 550),
             (21, 'out_left', RED, 450, 900)]

    def __init__(self, edges=None):
        self.high_score = 0
        self.average_score = 0
        self.last_average_score = 0
        self.generation = 0

        self.edges = edges
        self.graph = None
        self.driver = webdriver.Chrome(executable_path=paths.Path_to_chromium)
        self.driver.maximize_window()
        if edges is not None:
            self.show_graph()

    def show_graph(self):
        self.graph = Network(width=500, height=1100, heading='Neural network', bgcolor='#000000', font_color='#ffffff')
        for node in self.nodes:
            self.graph.add_node(n_id=node[0], label=node[1], color=node[2], x=node[3], y=node[4],
                                physics=False, labelHighlightBold=True, borderWidth=5)
        for edge in self.edges:
            if edge[2] < 0:
                self.graph.add_edge(edge[0], edge[1], value=abs(edge[2]) * 0.5, title=edge[2], color=RED)
            else:
                self.graph.add_edge(edge[0], edge[1], value=abs(edge[2] * 0.5), title=edge[2], color=GREEN)
        self.write_html(first_load=True)

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
        self.write_html()

    def update_scores(self, high_score, last_average_score, average_score):
        self.high_score = high_score
        self.last_average_score = last_average_score
        self.average_score = average_score
        self.generation += 1

    def write_html(self, first_load=False):
        # https://stackoverflow.com/questions/35355225/edit-and-create-html-file-using-python
        soup = bs4.BeautifulSoup(self.graph.generate_html(), features="html.parser")

        new_text = soup.new_tag('div', **{"style": "font-size: xx-large"})
        contents = soup.new_tag('p', **{"style": "white-space: pre-line"})
        contents.append(f'Generation number: {self.generation}\n'
                        f'High score: {self.high_score}\n'
                        f'Last gen average score: {self.last_average_score}\n'
                        f'This gen average score: {self.average_score}')
        new_text.append(contents)
        soup.body.append(new_text)

        with open(paths.Path_to_html, "w") as file_out:
            file_out.write(str(soup))

        try:
            if first_load:
                self.driver.get(paths.Path_to_html)
            else:
                self.driver.refresh()
        except selenium.common.exceptions.WebDriverException:
            print("There was an exception reaching chrome, it was likely closed")
            self.driver.quit()
            quit(1)
