import pygame, os, sys

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

scripts_path = (sys.path[0] + '\\assets\\scripts')

# Import modules from specific folders
sys.path.insert(1, "")

pawn_path = (scripts_path + "\\pawn")
sys.path[1] = pawn_path
import pawn_001 as pawn # pawn module

colors_path = (scripts_path + "\\colors")
sys.path[1] = colors_path
import colors_001 as colors # colors module

sys.path.pop(1)

# Constants
NUM_OF_PAWNS = 4

# Class
class player:
    def __init__(self, color = "", start_position = 0, home_position = 0):
        self.color = color
        self.start_position = start_position
        self.home_position = home_position
        self.pawns = []
        self.initialize_pawns()

    def initialize_pawns(self):
        self.pawns = []
        index = 0
        while index < NUM_OF_PAWNS:
            self.pawns.append(pawn.pawn(index, self.color, self.start_position, self.home_position))
            index += 1
            
    def stat(self):
        string_status = "Pawn: " + "\t\t\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(pawn_index) + "\t\t"
            pawn_index += 1

        string_status = string_status + "\n"
        string_status = string_status + "At Home: " + "\t\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].at_home) + "\t\t"
            pawn_index += 1

        string_status = string_status + "\n"
        string_status = string_status + "At Start: " + "\t\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].at_start) + "\t\t"
            pawn_index += 1

        string_status = string_status + "\n"
        string_status = string_status + "In Safe Zone: " + "\t\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].in_safety_zone) + "\t\t"
            pawn_index += 1
        
        string_status = string_status + "\n"
        string_status = string_status + "Board Position: " + "\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].board_position) + "\t\t"
            pawn_index += 1
        
        string_status = string_status + "\n"
        string_status = string_status + "Safety Zone Position: " + "\t"
        
        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].safety_zone_position) + "\t\t"
            pawn_index += 1

        string_status = string_status + "\n"
        string_status = string_status + "Start Position: " + "\t"

        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].start_position) + "\t\t"
            pawn_index += 1
        
        string_status = string_status + "\n"
        string_status = string_status + "Home Position: " + "\t\t"

        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            string_status = string_status + str(self.pawns[pawn_index].home_position) + "\t\t"
            pawn_index += 1

        print(string_status + "\n")

    def copy_player(self):
        new_player = player()
        new_player.color = self.color
        new_player.start_position = self.start_position
        new_player.home_position = self.home_position

        new_player.pawns = []

        pawn_index = 0
        while pawn_index < NUM_OF_PAWNS:
            original_pawn = self.pawns[pawn_index]
            new_pawn = original_pawn.copy_pawn()
            new_player.pawns.append(new_pawn)
            pawn_index += 1

        return new_player