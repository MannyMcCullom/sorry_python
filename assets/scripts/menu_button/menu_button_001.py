import pygame, os, sys

scripts_path = (sys.path[0] + "\\assets\\scripts")

fileName = os.path.basename(__file__)
print("Importing: " + fileName)

# Import modules from specific folders
sys.path.insert(1, "")

fonts_path = (sys.path[0] + "\\assets\\fonts")
font = pygame.font.Font(fonts_path + "\\Bitrimus-BLAPB.ttf", 38)

colors_path = (scripts_path + "\\colors")
sys.path[1] = colors_path
import colors_001 as colors # colors module

sys.path.pop(1)

# Class
class menu_button:
    def __init__(self, text = "", x = 0, y = 0, width = 200, height = 50):
        self.set_text(text)
        self.set_coordanates(x, y, width, height)
        
    def draw(self, screen, mouse_pos):
        is_hovering = self.button_rect.collidepoint(mouse_pos)
        
        if is_hovering == True:
            pygame.draw.rect(screen, colors.colors().text_color_hover, self.text_rect)
            
        screen.blit(self.text, self.button_rect)

        if pygame.mouse.get_pressed()[0] and is_hovering:
            return True
        
    def display(self, screen):
        screen.blit(self.text, self.button_rect)

    def set_text(self, text = ""):
        self.text = text
        self.text = font.render(self.text, True, colors.colors().text_color)
        self.text_hover = text
        self.text_hover = font.render(self.text_hover, True, colors.colors().text_color_hover)
        
    def set_coordanates(self, x, y, width, height):
        self.x = x
        self.y = y
        self.button_rect = pygame.Rect(self.x, self.y, width, height)
        self.text_rect = pygame.Rect(self.x, self.y, width, height)
                
