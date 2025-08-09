import os

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

# Colors
black = (0, 0, 0)

primary_color = (0, 0, 255)
secondary_color = (0, 0, 0)

text_color = (100, 0, 0)
text_color_hover = (255, 215, 0)
board_color = (255, 50, 200)
board_menu_color = (155, 50, 200)

# Class
class colors:
    def __init__(self):
        self.black = black
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.board_color = board_color
        self.board_menu_color = board_menu_color
        self.text_color = text_color
        self.text_color_hover = text_color_hover
