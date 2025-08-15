import pygame, os, sys, random

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

scripts_path = (sys.path[0] + '\\assets\\scripts')

# Import modules from specific folders
sys.path.insert(1, "")

card_path = (scripts_path + "\\card")
sys.path[1] = card_path
import card_001 as card # card module

sys.path.pop(1)

NUM_CARD_TYPE = 11
NUM_OF_CARDS = 45

CARD_LABEL = ["1",
              "2",
              "3",
              "4",
              "5",
              "7",
              "8",
              "10",
              "11",
              "12",
              "SORRY"]

CARD_OPTION_ONE = ["Move one of your pawns forward one from START.", # 1
                   "Move one of your pawns forward two from START.", # 2
                   "Move one of your pawns forward three spaces.", # 3
                   "Move one of your pawns backward four spaces.", # 4
                   "Move one of your pawns forward five spaces.", # 5
                   "Move one of your pawns forward seven spaces.", # 7
                   "Move one of your pawns forward eight spaces.", # 8
                   "Move one of your pawns forward ten spaces.", # 10
                   "Move one of your pawns forward eleven spaces.", # 11
                   "Move one of your pawns forward twelve spaces.", # 12
                   "Move a pawn from your start area to take the place of another player's pawn, which must return to its own start area."] # Sorry!

CARD_OPTION_TWO = ["If in play, move forward one space.", # 1
                   "If in play, move forward two spaces.", # 2
                   "n/a", # 3
                   "n/a", # 4
                   "n/a", # 5
                   "Split seven forward moves between two of your pawns.", # 7
                   "n/a", # 8
                   "Move one of your pawns backward one space.", # 10
                   "Switch any one of your pawns with an opponent's.", # 11
                   "n/a", # 12
                   "Move one of your pawns forward four spaces."] # SORRY!
# Class
class deck:
    def __init__(self):
        self.cards = []
        self.deck = []
        
        index = 0
        while index < NUM_CARD_TYPE:
            self.cards.append("")
            index += 1

        index = 0
        while index < NUM_OF_CARDS:
            self.deck.append("")
            index += 1
            
        self.set_cards()
        self.set_deck()
        self.print_deck()
        self.shuffle_deck()
        self.print_deck()

    def set_cards(self):
        index = 0
        while index < NUM_CARD_TYPE:
            self.cards[index] = card.card(CARD_LABEL[index], CARD_OPTION_ONE[index], CARD_OPTION_TWO[index])
            index += 1

    def get_card(self, card_num):
        return self.deck[card_num]

    def set_deck(self):
        print("STATUS: deck initiating")
        card_num = 0
        index = 0
        while index < NUM_OF_CARDS:
            if index >= 0 and index < 5:
                card_num = 0
            elif index >= 5 and index < 9:
                card_num = 1
            elif index >= 9 and index < 13:
                card_num = 2
            elif index >= 13 and index < 17:
                card_num = 3
            elif index >= 17 and index < 21:
                card_num = 4
            elif index >= 21 and index < 25:
                card_num = 5
            elif index >= 25 and index < 29:
                card_num = 6
            elif index >= 29 and index < 33:
                card_num = 7
            elif index >= 33 and index < 37:
                card_num = 8
            elif index >= 37 and index < 41:
                card_num = 9
            elif index >= 41 and index < 45:
                card_num = 10
                
            # print("Index: " + str(index))
            self.deck[index] = self.cards[card_num]
            index += 1

        print("STATUS: deck initiated")

    def print_deck(self):
        print("STATUS: deck printing")
        index = 0
        while index < NUM_OF_CARDS:
            print(self.deck[index].label)
            index += 1

        print("STATUS: deck printed")

    def shuffle_deck(self):
        print("STATUS: deck shuffling")
        card_track = []
        new_deck = []

        index = 0
        while index < NUM_OF_CARDS:
            new_deck.append("")
            card_track.append(0)
            index += 1

        index = 0
        while index < NUM_OF_CARDS:
            switched = False
            while switched == False:
                random_card = random.randint(0, NUM_OF_CARDS - 1)
                
                if card_track[random_card] == 0:
                    new_deck[index] = self.deck[random_card]
                    card_track[random_card] = 1
                    switched = True
                    
            index += 1
                    
        self.deck = new_deck
        print("STATUS: deck shuffled")

    def shuffle_deck_card_11(self):
        print("STATUS: deck shuffling for card 11")
        card_track = []
        new_deck = []

        index = 0
        while index < NUM_OF_CARDS:
            new_deck.append("")
            card_track.append(0)
            index += 1

        index = 0
        while index < NUM_OF_CARDS:
            switched = False
            while switched == False:
                random_card = random.randint(0, NUM_OF_CARDS - 1)

                if card_track[random_card] == 0:
                    if index < 5:
                        if self.deck[random_card].label == "1":
                            new_deck[index] = self.deck[random_card]
                            card_track[random_card] = 1
                            switched = True
                    elif index >= 5 and index < 9:
                        if self.deck[random_card].label == "11":
                            new_deck[index] = self.deck[random_card]
                            card_track[random_card] = 1
                            switched = True
                    else:    
                        new_deck[index] = self.deck[random_card]
                        card_track[random_card] = 1
                        switched = True
                        
            index += 1
                    
        self.deck = new_deck
        print("STATUS: deck shuffled")
        self.print_deck()

    def shuffle_deck_card_sorry(self):
        print("STATUS: deck shuffling for card SORRY")
        card_track = []
        new_deck = []

        index = 0
        while index < NUM_OF_CARDS:
            new_deck.append("")
            card_track.append(0)
            index += 1

        index = 0
        while index < NUM_OF_CARDS:
            switched = False
            while switched == False:
                random_card = random.randint(0, NUM_OF_CARDS - 1)

                if card_track[random_card] == 0:
                    if index < 5:
                        if self.deck[random_card].label == "1":
                            new_deck[index] = self.deck[random_card]
                            card_track[random_card] = 1
                            switched = True
                    elif index >= 5 and index < 9:
                        if self.deck[random_card].label == "SORRY":
                            new_deck[index] = self.deck[random_card]
                            card_track[random_card] = 1
                            switched = True
                    else:    
                        new_deck[index] = self.deck[random_card]
                        card_track[random_card] = 1
                        switched = True
                        
            index += 1
                    
        self.deck = new_deck
        print("STATUS: deck shuffled")
        self.print_deck()
