import time
from tkinter import Tk, Frame, Text, TOP

import bs4
from tkinterhtml import HtmlFrame
from paths import Path_to_html


NUMBER = 1

class html_renderer:

    def __init__(self):
        root = Tk()

        neural_net_frame = HtmlFrame(root, horizontal_scrollbar="auto")
        neural_net_frame.set_content(self.write_html())

        root.mainloop()
        # root.update_idletasks()
        # root.update()


    def write_html(self):
        # https://stackoverflow.com/questions/35355225/edit-and-create-html-file-using-python
        with open(Path_to_html) as file:
            soup = bs4.BeautifulSoup(file.read(), features="html.parser")

        new_text = soup.new_tag('div', **{"style": "font-size: xx-large"})
        contents = soup.new_tag('p', **{"style": "white-space: pre-line"})
        contents.append(f'Generation number: {NUMBER}\n'
                        f'High score: {NUMBER}\n'
                        f'Last gen average score: {NUMBER}\n'
                        f'Ths gen average score: {NUMBER}')
        new_text.append(contents)
        soup.body.append(new_text)

        return str(soup)


if __name__ == "__main__":
    html_renderer()
