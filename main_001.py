# Example file showing a basic pygame "game loop"
import sys, pygame
pygame.init()

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
pygame.display.set_caption("Dude I'm so Sorry!")
print()

scripts_path = (sys.path[0] + '\\assets\\scripts')

# Import modules from specific folders
sys.path.insert(1, "")

menu_game_path = (scripts_path + "\\menu_game")
sys.path[1] = menu_game_path
import menu_game_001 as menu_game # menu_game module

sys.path.pop(1)

################################ Program Starts here ################################

menu_game.menu_game()
