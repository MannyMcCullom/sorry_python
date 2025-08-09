import pygame, os, sys, random

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

scripts_path = (sys.path[0] + '\\assets\\scripts')

# Import modules from specific folders
sys.path.insert(1, "")

'''
card_path = (scripts_path + "\\card")
sys.path[1] = card_path
import card_001 as card # menu_button module
'''

sys.path.pop(1)

class card:
    def __init__(self, label = "", option_one = "", option_two = ""):
        self.label = label
        self.option_one = option_one
        self.option_two = option_two
        
    def set_label(self, new_label):
        self.label = new_label

    def get_label(self):
        return self.label

    def set_option_one(self, new_option):
        self.option_one = new_option

    def get_option_one(self):
        return self.option_one

    def set_option_two(self, new_option):
        self.option_two = new_option

    def get_option_two(self):
        return self.option_two
