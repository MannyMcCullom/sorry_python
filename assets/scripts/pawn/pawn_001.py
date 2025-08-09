import os, sys

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

MIN_BOARD_POSITION = 0
MAX_BOARD_POSITION = 59
MIN_SAFETY_ZONE_POSITION = 0
MAX_SAFETY_ZONE_POSITION = 5

# Class
class pawn:
    def __init__(self, pawn_num = 0, color = "no_color", start_position = 0, home_position = 0):
        self.pawn_num = pawn_num
        self.board_position = start_position
        self.start_position = start_position
        self.home_position = home_position
        self.safety_zone_position = 0
        self.color = color
        self.at_start = True
        self.at_home = False
        self.in_safety_zone = False

    def stat(self):
        print("Pawn Number: " + str(self.pawn_num))
        print("At Start: " + str(self.at_start))
        print("At Home: " + str(self.at_home))
        print("In Safe Zone: " + str(self.in_safe_zone))
        print("Board Position: " + str(self.board_position))
        print("Safety Zone Position: " + str(self.safety_zone_position))
        print("Start Position: " + str(self.start_position))
        print("Home Position: " + str(self.home_position))

    def reset(self):
        self.board_position = self.start_position
        self.safety_zone_position = 0
        self.at_start = True
        self.at_home = False
        self.in_safety_zone = False

    def board_position_swappable(self):
        swappable = True
        
        if self.at_start == True:
            swappable = False

        if self.at_home == True:
            swappable = False

        if self.in_safety_zone == True:
            swappable = False

        return swappable

    def on_open_board(self):
        on_board = True
        
        if self.at_start == True:
            on_board = False

        if self.at_home == True:
            on_board = False

        return on_board

    def is_same_as(self, other_pawn):
        same = True

        if self.pawn_num != other_pawn.pawn_num:
            same = False

        if self.at_start != other_pawn.at_start:
            same = False

        if self.at_home != other_pawn.at_home:
            same = False

        if self.board_position != other_pawn.board_position:
            same = False

        if self.safety_zone_position != other_pawn.safety_zone_position:
            same = False

        if self.in_safety_zone != other_pawn.in_safety_zone:
            same = False
        
        return same
    
    def has_same_position_as(self, other_pawn):
        same = True

        if other_pawn.at_start == True or other_pawn.at_home == True:
            same = False

        if self.board_position != other_pawn.board_position:
            same = False

        if self.safety_zone_position != other_pawn.safety_zone_position:
            same = False

        if self.in_safety_zone != other_pawn.in_safety_zone:
            same = False
        
        return same

    def valid_position(self):
        valid = True

        if self.board_position < MIN_BOARD_POSITION or self.board_position > MAX_BOARD_POSITION:
            valid = False
        
        if self.safety_zone_position < MIN_SAFETY_ZONE_POSITION or self.safety_zone_position > MAX_SAFETY_ZONE_POSITION:
            valid = False

        return valid
    
    def copy_pawn(self):
        new_pawn = pawn()
        new_pawn.pawn_num = self.pawn_num
        new_pawn.color = self.color
        new_pawn.start_position = self.start_position
        new_pawn.home_position = self.home_position
        new_pawn.board_position = self.board_position
        new_pawn.safety_zone_position = self.safety_zone_position
        new_pawn.at_start = self.at_start
        new_pawn.at_home = self.at_home
        new_pawn.in_safety_zone = self.in_safety_zone

        return new_pawn
    
    def check_home_postion(self):
        if self.safety_zone_position == MAX_SAFETY_ZONE_POSITION:
            self.at_home = True
