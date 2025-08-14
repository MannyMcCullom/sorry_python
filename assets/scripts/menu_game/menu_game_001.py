import pygame, os, sys, time

file_name = os.path.basename(__file__)
print("Importing: " + file_name)

scripts_path = (sys.path[0] + '\\assets\\scripts')

# Import modules from specific folders
sys.path.insert(1, "")

menu_button_path = (scripts_path + "\\menu_button")
sys.path[1] = menu_button_path
import menu_button_001 as menu_button # menu_button module

deck_path = (scripts_path + "\\deck")
sys.path[1] = deck_path
import deck_001 as deck # deck module

colors_path = (scripts_path + "\\colors")
sys.path[1] = colors_path
import colors_001 as colors # colors module

player_path = (scripts_path + "\\player")
sys.path[1] = player_path
import player_001 as player # player module

sys.path.pop(1)

# Constants
DEBUG = True
TESTING = False

CLICK_TIMER = 0.2
RECT_LEFT_QUIT = 700
RECT_TOP_QUIT = 50
RECT_LEFT_PLAY_BUTTON_START = 50
RECT_TOP_PLAY_BUTTON_START = 800
PLAYER_COLORS = ["GREEN", "RED", "BLUE", "YELLOW"]
OPTION_SELECTION = ["OPTION_ONE", "OPTION_TWO", "FORFEIT"]
PAWNS = ["PAWN_ZERO", "PAWN_ONE", "PAWN_TWO", "PAWN_THREE"]
MIN_NUM_OF_PLAYERS = 2
MAX_NUM_OF_PLAYERS = 4
MAX_NUM_OF_PAWNS = 4
MIN_BOARD_POSITION = 0
MAX_BOARD_POSITION = 59
MIN_SAFETY_ZONE_POSITION = 0
MAX_SAFETY_ZONE_POSITION = 5
SLIDE_POSITION_SHORT = [1, 16, 31, 46]
SLIDE_POSITION_LONG = [9, 24, 9, 54]
START_POSITION = [4, 19, 34, 49]
HOME_POSITION = [2, 17, 32, 47]

NUM_CARD_TYPE = 11
MAX_NUM_OF_CARD_OPTIONS = 3

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

# Class
class menu_game:
    def __init__(self):
        # etc
        self.mouse_pressed = True
        self.debug_message = ""
        #self.menu_hide = False

        # Screen
        self.set_screen()
        self.board_rect = pygame.Rect(0, 0, 900, 900)
        self.menu_rect = pygame.Rect(0, 800, 900, 200)
        self.menu_start_rect = pygame.Rect(0, 0, 200, 900)
        self.menu_play_rect = pygame.Rect(0, 800, 900, 200)
        
        # Menu booleans
        self.all_menus_off()
        
        # Start Game
        self.menu_start()
    
    def initialize_players(self):
            self.current_player_turn = 0
            self.num_of_players = 4
            self.players = []

            player_index = 0
            while player_index < self.num_of_players:
                new_player = player.player(PLAYER_COLORS[player_index], START_POSITION[player_index], HOME_POSITION[player_index])
                self.players.append(new_player)
                player_index += 1

    def set_screen(self, width = 900, height = 900):
            self.screen = pygame.display.set_mode((width, height))

    def draw_board(self): # Draw board, and pawns
        pygame.draw.rect(self.screen, colors.colors().board_color, self.board_rect)

    def menu_start_panel(self):
        pygame.draw.rect(self.screen, (colors.colors().primary_color), self.menu_start_rect)

    def menu_play_panel(self):
        pygame.draw.rect(self.screen, (colors.colors().primary_color), self.menu_play_rect)

    def button_close_corner(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP: 
                self.mouse_pressed = False

    def button_menu_start(self):
        button_menu_start = menu_button.menu_button("Start Menu", RECT_LEFT_QUIT, RECT_TOP_QUIT).draw(self.screen, self.mouse_pos)

        while button_menu_start:
            if not self.mouse_pressed:
                time.sleep(CLICK_TIMER)
                self.all_menus_off()
                self.in_menu_start = True
            break

    def all_menus_off(self):
        self.in_menu_start = False
        self.in_menu_play = False
        self.in_select_pawn = False
        self.in_select_option = False
        self.in_select_pawn_other_players = False
        self.in_split_option = False
        self.in_validating_option = False
        self.in_validating_pawn = False
        self.in_player_action = False

    def black_screen(self):
        self.screen.fill(colors.colors().black)

# Menus (Top) ----------------------------------------------------------------------------------------------
    def menu_start(self):
        self.in_menu_start = True
        while self.in_menu_start:
            x_pos = 50
            y_pos = 50
            self.mouse_pos = pygame.mouse.get_pos()
            
            self.black_screen()
            self.menu_start_panel()
            self.button_close_corner()

            button_play = menu_button.menu_button("Play", x_pos, y_pos).draw(self.screen, self.mouse_pos)

            while button_play:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    time.sleep(CLICK_TIMER)
                    self.menu_play()
                break
            
            y_pos += 100

            button_exit = menu_button.menu_button("Exit", x_pos, y_pos).draw(self.screen, self.mouse_pos)

            while button_exit:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    time.sleep(CLICK_TIMER)
                    self.in_menu_start = False
                break
        
            pygame.display.flip()

    def menu_play(self):
        self.mouse_pressed = True
        self.card_num = 0

        self.deck = deck.deck()
        self.deck.set_deck() # Makes Deck Unshuffled
        #self.deck.shuffle_deck_card_11() # DEBUG For test 11 Card

        self.deck.print_deck()
        
        self.initialize_players()

        self.in_menu_play = True
        while self.in_menu_play:
            self.mouse_pos = pygame.mouse.get_pos()
            self.check_card_num()
                
            self.black_screen()
            self.button_close_corner()
            self.draw_board()
            self.button_menu_start()

            x_pos = RECT_LEFT_PLAY_BUTTON_START
            y_pos = RECT_TOP_PLAY_BUTTON_START
            self.menu_play_panel()

            draw_card_button = menu_button.menu_button("Draw Card", x_pos, y_pos).draw(self.screen, self.mouse_pos)

            while draw_card_button:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    time.sleep(CLICK_TIMER)

                    selected_option = -1
                    selected_pawn = -1
                    selected_moves = -1
                    selected_pawn_two = -1
                    other_player_pawn = -1
                    other_player_index = -1
                    valid = False
                    drawn_card = self.deck.deck[self.card_num].label
                    
                    print("\n" + "Drawn Card: " + drawn_card + "\n")
                    self.player_status_all()

                    self.in_validating_option = True
                    while self.in_validating_option == True:
                        self.check_all_options()

                        selected_option = self.select_option()
                        valid = self.validate_selected_option(selected_option)

                        if valid == True:
                            if selected_option != OPTION_SELECTION.index("FORFEIT"):
                                selected_pawn = self.select_pawn()
                                valid = self.validate_selected_pawn(selected_pawn, selected_option)

                                if drawn_card == "7" and selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                                    selected_moves = self.select_moves()
                                    selected_pawn_two = self.select_pawn()
                                    valid = self.validate_selected_moves(selected_pawn, selected_moves, selected_pawn_two)
                                
                                elif drawn_card == "11" and selected_option == OPTION_SELECTION.index("OPTION_TWO"): # Manny is Really Here 8/14/2025 *Current Project
                                    other_player_index, selected_pawn_two = self.select_other_player_pawn() # Create Method
                                    valid = self.validate_selected_other_player_pawn(selected_pawn, selected_pawn_two, other_player_index) # Create Method
                        if valid == True:
                            self.in_validating_option = False

                    if valid == True:
                        self.player_action(selected_option, selected_pawn, selected_moves, selected_pawn_two, other_player_index)
                    
                        self.card_num += 1 # Change top card
                        self.current_player_turn += 1 # Change current player

                        if self.current_player_turn >= self.num_of_players:
                            self.current_player_turn = 0

                break
            
            pygame.display.flip()

    def select_option(self):
        print("Selecting Option")

        self.mouse_pressed = True
        option = -1

        self.in_select_option = True
        while self.in_select_option:
            self.mouse_pos = pygame.mouse.get_pos()

            self.black_screen()
            self.button_close_corner()
            self.draw_board()
            self.button_menu_start()

            self.menu_play_panel()

            # Display
            x_pos_options = 50
            y_pos_options = 50

            display_player = menu_button.menu_button("Player: " + str(self.current_player_turn), x_pos_options, y_pos_options).display(self.screen)
            y_pos_options += 200
            
            display_card = menu_button.menu_button("Card: " + self.deck.deck[self.card_num].label, x_pos_options, y_pos_options).display(self.screen)
            y_pos_options += 200
            
            display_option_one = menu_button.menu_button("Option 1: " + self.deck.deck[self.card_num].option_one, x_pos_options, y_pos_options).display(self.screen)
            y_pos_options += 200
            
            display_option_two = menu_button.menu_button("Option 2: " + self.deck.deck[self.card_num].option_two, x_pos_options, y_pos_options).display(self.screen)
            y_pos_options += 200

            # Buttons
            x_pos_button = 50
            y_pos_button = 800

            button_option_one = menu_button.menu_button("Option 1", x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)
            x_pos_button += 200

            while button_option_one:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    self.in_select_option = False
                    option = OPTION_SELECTION.index("OPTION_ONE")
                    time.sleep(CLICK_TIMER)
                break

            button_option_two = menu_button.menu_button("Option 2", x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)
            x_pos_button += 200

            while button_option_two:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    self.in_select_option = False
                    option = OPTION_SELECTION.index("OPTION_TWO")
                    time.sleep(CLICK_TIMER)
                break

            button_forfeit = menu_button.menu_button("Forfeit Turn", x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)

            while button_forfeit:
                if not self.mouse_pressed:
                    self.mouse_pressed = True
                    self.in_select_option = False
                    option = OPTION_SELECTION.index("FORFEIT")
                    time.sleep(CLICK_TIMER)
                break

            pygame.display.flip()
        
        print("Selected: " + OPTION_SELECTION[option])
        return option
            
    def select_pawn(self):
        print("Selecting pawn")
        selected_pawn = -1
        
        self.in_select_pawn = True
        while self.in_select_pawn:
            self.mouse_pos = pygame.mouse.get_pos()

            self.black_screen()
            self.button_close_corner()
            self.draw_board()
            self.button_menu_start()

            # Buttons
            x_pos_button = RECT_LEFT_PLAY_BUTTON_START
            y_pos_button = RECT_TOP_PLAY_BUTTON_START
            self.menu_play_panel()

            pawn_index = 0
            while pawn_index < MAX_NUM_OF_PAWNS:
                button_pawn = menu_button.menu_button("Pawn " + str(pawn_index), x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)
                while button_pawn:
                    if not self.mouse_pressed:
                        self.mouse_pressed = True
                        self.in_select_pawn = False
                        selected_pawn = pawn_index
                        print("Selected Pawn " + str(pawn_index))
                        time.sleep(CLICK_TIMER)
                    break
                
                x_pos_button += 200
                pawn_index += 1

            pygame.display.flip()

        return selected_pawn
    
    def select_other_player_pawn(self):
        print("Selecting pawn")
        selected_pawn = -1
        selected_player = -1
        
        self.in_select_pawn = True
        while self.in_select_pawn:
            self.mouse_pos = pygame.mouse.get_pos()

            self.black_screen()
            self.button_close_corner()
            self.draw_board()
            self.button_menu_start()

            # Buttons
            x_pos_button = RECT_LEFT_PLAY_BUTTON_START
            y_pos_button = RECT_TOP_PLAY_BUTTON_START
            self.menu_play_panel()

            player_index = 0
            while player_index < MAX_NUM_OF_PLAYERS:
                if player_index != self.current_player_turn:
                    x_pos_button = RECT_LEFT_PLAY_BUTTON_START

                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        button_pawn = menu_button.menu_button(str(player_index) + str(pawn_index), x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)
                        while button_pawn:
                            if not self.mouse_pressed:
                                self.mouse_pressed = True
                                self.in_select_pawn = False
                                selected_pawn = pawn_index
                                selected_player = player_index
                                print("Selected Player " + str(player_index) + " Pawn " + str(pawn_index))
                                time.sleep(CLICK_TIMER)
                            break
                        
                        x_pos_button += 50
                        pawn_index += 1
                    
                    y_pos_button += 50

                player_index += 1

            pygame.display.flip()

        return selected_player, selected_pawn
    
    def select_moves(self):
        print("Selecting Moves")
        selected_moves = -1
        
        self.in_select_moves = True
        while self.in_select_moves:
            self.mouse_pos = pygame.mouse.get_pos()

            self.black_screen()
            self.button_close_corner()
            self.draw_board()
            self.button_menu_start()

            # Buttons
            x_pos_button = RECT_LEFT_PLAY_BUTTON_START
            y_pos_button = RECT_TOP_PLAY_BUTTON_START
            self.menu_play_panel()

            moves_index = 1
            while moves_index <= 7:
                button_pawn = menu_button.menu_button(str(moves_index), x_pos_button, y_pos_button).draw(self.screen, self.mouse_pos)
                while button_pawn:
                    if not self.mouse_pressed:
                        self.mouse_pressed = True
                        self.in_select_moves = False
                        selected_moves = moves_index
                        print("Selected Move " + str(moves_index))
                        time.sleep(CLICK_TIMER)
                    break
                
                x_pos_button += 50
                moves_index += 1

            pygame.display.flip()

        return selected_moves
    
# Menus (Bottom) ----------------------------------------------------------------------------------------------

    def check_card_num(self):
        if self.card_num > 44 or self.card_num < 0:
            self.card_num = 0
            self.deck.shuffle_deck()

    def add_debug_message(self, message = "n/a", type = "general"):
        if type == "general":
            self.debug_message += "DEBUG: " + message + "\n"

        if type == "not_valid":
            self.debug_message += "=== Option Not Valid === \nReason: " + message + "\n"

    def print_temp_debug_message(self, message):
        if DEBUG == True:
            print("DEBUG: " + message)

    def print_debug_message(self):
        print(self.debug_message)
        self.clear_debug_message()

    def clear_debug_message(self):
        self.debug_message = ""

    def copy_players(self, players):
        players_copy = []

        player_index = 0
        while player_index < MAX_NUM_OF_PLAYERS:
            players_copy.append(0)
            players_copy[player_index] = players[player_index].copy_player()
            player_index += 1

        return players_copy
    
    def pawn_checks(self, players, pawn, pawn_option_valid = False, option_index = -1):
        if option_index == -1:
            pawn.check_home_postion()
            pawn = self.check_slide_position(players, pawn)
            self.take_over_position(players, pawn)
        else:
            pawn_option_valid = self.check_end_position_valid(pawn, option_index)

            if pawn_option_valid == True:
                pawn.check_home_postion()
                pawn = self.check_slide_position(players, pawn)
                pawn_option_valid = self.check_end_position_occupied(pawn, option_index)

            return pawn_option_valid

# Card Option Actions (Top) ------------------------------------------------------------------------------
    def card_1_option_1_action(self, pawn): # Move one of your pawns forward one from START.
        pawn.reset()
        pawn.at_start = False

    def card_1_option_2_action(self, pawn): # If in play, move forward one space."
        pawn = self.move_forward(pawn)

    def card_2_option_1_action(self, pawn): # Move one of your pawns forward two from START.
        pawn.reset()
        pawn.at_start = False
        pawn = self.move_forward(pawn)

    def card_2_option_2_action(self, pawn): # If in play, move forward two spaces.
        pawn = self.move_forward(pawn, 2)
    
    def card_3_option_1_action(self, pawn): # Move one of your pawns forward three spaces.
        pawn = self.move_forward(pawn, 3)

    def card_4_option_1_action(self, pawn): # Move one of your pawns backward four spaces.
        pawn = self.move_backward(pawn, 4)

    def card_5_option_1_action(self, pawn): # Move one of your pawns forward five spaces.
        pawn = self.move_forward(pawn, 5)

    def card_7_option_1_action(self, pawn): # Move one of your pawns forward seven spaces.
        pawn = self.move_forward(pawn, 7)

    def card_7_option_2_action(self, pawn_one, pawn_two, moves_selection): # Split seven forward moves between two of your pawns.
        moves = 7
        pawn_one = self.move_forward(pawn_one, moves_selection)
        moves -= moves_selection
        if moves > 0:
            pawn_two = self.move_forward(pawn_two, moves)

    def card_8_option_1_action(self, pawn): # Move one of your pawns forward eight spaces.
        pawn = self.move_forward(pawn, 8)

    def card_10_option_1_action(self, pawn): # Move one of your pawns forward ten spaces.
        pawn = self.move_forward(pawn, 10)

    def card_10_option_2_action(self, pawn): # Move one of your pawns backward one space.
        pawn = self.move_backward(pawn)

    def card_11_option_1_action(self, pawn): # Move one of your pawns forward eleven spaces.
        pawn = self.move_forward(pawn, 11)

    def card_11_option_2_action(self, pawn, other_player_pawn): # Switch any one of your pawns with an opponent's.
        temp_board_position = pawn.board_position
        pawn.board_position = other_player_pawn.board_position
        other_player_pawn.board_position = temp_board_position

    def card_12_option_1_action(self, pawn): # Move one of your pawns forward twelve spaces.
        pawn = self.move_forward(pawn, 12)

    def card_sorry_option_1_action(self, players, pawn): # Move a pawn from your start area to take the place of another player's pawn, which must return to its own start area.
        i = 0

    def card_sorry_option_2_action(self, pawn): # Move one of your pawns forward four spaces.
        pawn = self.move_forward(pawn, 4)

# Card Option Actions (Bottom) ------------------------------------------------------------------------------

    def print_all_options(self):
        card_index = 0
        print("\nCard\tOption One\tOption Two\tForfeit")
        while card_index < NUM_CARD_TYPE:
            stat_string = CARD_LABEL[card_index] + "\t"
            stat_string += str(self.all_options[card_index][OPTION_SELECTION.index("OPTION_ONE")]) + "\t\t"
            stat_string += str(self.all_options[card_index][OPTION_SELECTION.index("OPTION_TWO")]) + "\t\t"
            stat_string += str(self.all_options[card_index][OPTION_SELECTION.index("FORFEIT")]) + "\t\t"
            print(stat_string)

            card_index += 1
        
        print()

# Check Card Options (Top) ------------------------------------------------------------------------------
    def check_options_card_1(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "1":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.at_start == True:
                            self.card_1_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't at START. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_1_option_2_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " isn't available because of PLAYER " + str(current_player_turn) + "'s PAWN " + str(pawn_index) + " isn't on the open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_2(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "2":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.at_start == True:
                            self.card_2_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't at START. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_2_option_2_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " isn't available because of PLAYER " + str(current_player_turn) + "'s PAWN " + str(pawn_index) + " isn't on the open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_3(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "3":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_3_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_4(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "4":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_4_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_5(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "5":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_5_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_7(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "7":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_7_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_7_option_two_choices = [] # 3D Array

                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        moves_choice = []

                        moves_index = 0
                        while moves_index < 7:
                            pawn_choice = [False, False, False, False]
                            moves_choice.append(pawn_choice)

                            moves_index += 1

                        self.card_7_option_two_choices.append(moves_choice)

                        pawn_index += 1

                    pawn_index_one = 0
                    while pawn_index_one < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn_one = current_player.pawns[pawn_index_one].copy_pawn()

                        if current_pawn_one.on_open_board() == True:
                            moves_index = 0
                            while moves_index < 7:
                                pawn_index_two = 0
                                while pawn_index_two < MAX_NUM_OF_PAWNS:
                                    temp_current_players = self.copy_players(temp_players)
                                    temp_current_player = temp_current_players[current_player_turn].copy_player()
                                    temp_current_pawn_one = temp_current_player.pawns[pawn_index_one].copy_pawn()
                                    temp_current_pawn_two = temp_current_player.pawns[pawn_index_two].copy_pawn()

                                    self.card_7_option_2_action(temp_current_pawn_one, temp_current_pawn_two, moves_index + 1)

                                    valid = False
                                    valid = self.pawn_checks(temp_current_players, temp_current_pawn_one, valid, option_index)
                                    print("DEBUG: After first check, valid = " + str(valid))


                                    if valid == True:
                                        valid = self.pawn_checks(temp_current_players, temp_current_pawn_two, valid, option_index)
                                        print("DEBUG: After second check, valid = " + str(valid))

                                    self.card_7_option_two_choices[pawn_index_one][moves_index][pawn_index_two] = valid

                                    pawn_index_two += 1

                                moves_index += 1
                        else:
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index_one += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                # Split moves logic
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_8(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "8":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_8_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_10(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "10":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_10_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_10_option_2_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_11(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "11":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_11_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    print("DEBUG: HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    temp_players = self.copy_players(players)
                    self.all_swap_pawn_options = []
                    
                    player_index = 0
                    while player_index < MAX_NUM_OF_PLAYERS:
                        player_options = []

                        pawn_index = 0
                        while pawn_index < MAX_NUM_OF_PAWNS:
                            if temp_players[player_index].pawns[pawn_index].board_position_swappable() == True:
                                player_options.append(True)
                            else:
                                player_options.append(False)

                            pawn_index += 1

                        self.all_swap_pawn_options.append(player_options)

                        player_index += 1

                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()
                        #pawn_option_valid[pawn_index] = False

                        if current_pawn.board_position_swappable() == True:
                            player_index = 0
                            while player_index < MAX_NUM_OF_PLAYERS:
                                if player_index != self.current_player_turn:
                                    other_player_pawn_index = 0
                                    while other_player_pawn_index < MAX_NUM_OF_PAWNS:
                                        if temp_players[player_index].pawns[other_player_pawn_index].board_position_swappable() == True:
                                            pawn_option_valid[pawn_index] = True
                                            break
                                        
                                        other_player_pawn_index += 1

                                if pawn_option_valid[pawn_index] == True:
                                    break

                                player_index += 1
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                    if self.all_options[card_index][OPTION_SELECTION.index("OPTION_ONE")] == False:
                        self.all_options[card_index][OPTION_SELECTION.index("FORFEIT")] = True
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_12(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "12":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_12_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

    def check_options_card_sorry(self, card_index, current_player_turn, players): # Manny is Here --------------------------------------------------------------------------------------------------------------------------------------
        if CARD_LABEL[card_index] == "SORRY":
            self.print_temp_debug_message("Checking Card: " + CARD_LABEL[card_index])

            option_index = 0
            while option_index < MAX_NUM_OF_CARD_OPTIONS:
                self.print_temp_debug_message("Checking Choice: " + OPTION_SELECTION[option_index])

                pawn_option_valid = [True, True, True, True]

                if option_index == OPTION_SELECTION.index("OPTION_ONE"):
                    pawn_index = 999999 # Bypass loop
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_sorry_option_1_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)

                if option_index == OPTION_SELECTION.index("OPTION_TWO"):
                    pawn_index = 0
                    while pawn_index < MAX_NUM_OF_PAWNS:
                        temp_players = self.copy_players(players)
                        current_player = temp_players[current_player_turn]
                        current_pawn = current_player.pawns[pawn_index].copy_pawn()

                        if current_pawn.on_open_board() == True:
                            self.card_sorry_option_2_action(current_pawn)
                            self.pawn_checks(temp_players, current_pawn, pawn_option_valid[pawn_index], option_index)
                        else:
                            pawn_option_valid[pawn_index] = False
                            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(current_player_turn) + " PAWN " + str(pawn_index) + " because PAWN isn't on open board. ")

                        pawn_index += 1
                    
                    self.validate_all_options(pawn_option_valid, card_index, option_index)
                    
                self.print_temp_debug_message("Done Checking Choice: " + OPTION_SELECTION[option_index])
                option_index += 1
            
            self.print_temp_debug_message("Done Checking Card: " + CARD_LABEL[card_index])

# Check Card Options (Bottom) ------------------------------------------------------------------------------
    
    def validate_all_options(self, pawn_option_valid, card_index, option_index):
        if CARD_LABEL[card_index] == "7" and option_index == OPTION_SELECTION.index("OPTION_TWO"):
            pawn_index_one = 0
            while pawn_index_one < MAX_NUM_OF_PAWNS:
                moves_index = 0
                while moves_index < 7:
                    pawn_index_two = 0
                    while pawn_index_two < MAX_NUM_OF_PAWNS:
                        if self.card_7_option_two_choices[pawn_index_one][moves_index][pawn_index_two] == True:
                            self.all_options_pawns[card_index][option_index][pawn_index_one] = True
                            self.all_options[card_index][option_index] = True

                        pawn_index_two += 1

                    moves_index += 1

                pawn_index_one += 1
        else:
            pawn_index = 0
            while pawn_index < MAX_NUM_OF_PAWNS:
                if pawn_option_valid[pawn_index] == True:
                    self.all_options_pawns[card_index][option_index][pawn_index] = True
                    self.all_options[card_index][option_index] = True
                pawn_index += 1

    def check_all_options(self): # """Manny is here"""
        self.print_temp_debug_message("Entered check_all_options()")

        current_player_turn = self.current_player_turn
        players = self.players

        all_options = []
        all_options_pawns = []

        card_index = 0
        while card_index < NUM_CARD_TYPE:
            all_options.append(0)
            all_options[card_index] = [False, False, False]
            all_options_pawns.append([])

            option_index = 0
            while option_index < OPTION_SELECTION.index("FORFEIT"):
                all_options_pawns[card_index].append(0)
                all_options_pawns[card_index][option_index] = [False, False, False, False]
                option_index += 1

            card_index += 1
        
        self.all_options = all_options
        self.all_options_pawns = all_options_pawns

        card_index = 0
        while card_index < NUM_CARD_TYPE:
            self.check_options_card_1(card_index, current_player_turn, players)
            self.check_options_card_2(card_index, current_player_turn, players)
            self.check_options_card_3(card_index, current_player_turn, players)
            self.check_options_card_4(card_index, current_player_turn, players)
            self.check_options_card_5(card_index, current_player_turn, players)
            self.check_options_card_7(card_index, current_player_turn, players)
            self.check_options_card_8(card_index, current_player_turn, players)
            self.check_options_card_10(card_index, current_player_turn, players)
            self.check_options_card_11(card_index, current_player_turn, players)
            self.check_options_card_12(card_index, current_player_turn, players)
            self.check_options_card_sorry(card_index, current_player_turn, players)

            # Makes forfeiting turn a valid option if allowed
            if self.all_options[card_index][OPTION_SELECTION.index("OPTION_ONE")] == False:
                if self.all_options[card_index][OPTION_SELECTION.index("OPTION_TWO")] == False:
                    self.all_options[card_index][OPTION_SELECTION.index("FORFEIT")] = True

            card_index += 1
        
        self.print_all_options()

        self.print_temp_debug_message("DEBUG: Exiting check_all_options()\n")

    def validate_selected_option(self, selected_option):
        self.print_temp_debug_message("DEBUG: Entering vaildate_selected_option()\n")

        valid = False
        all_options = self.all_options

        if selected_option >= OPTION_SELECTION.index("OPTION_ONE") and selected_option <= OPTION_SELECTION.index("FORFEIT"):
            card_index = 0
            while card_index < NUM_CARD_TYPE:
                if self.deck.deck[self.card_num].label == CARD_LABEL[card_index]:
                    valid = all_options[card_index][selected_option]
                    break

                card_index += 1
        
        if valid == False:
            self.player_status(self.current_player_turn)
            self.print_debug_message()
        
        self.print_temp_debug_message("DEBUG: Exiting vaildate_selected_option()\n")
        return valid
    
    def take_over_position(self, players, current_pawn):
        player_index = 0
        while player_index < MAX_NUM_OF_PLAYERS:
            pawn_index = 0
            while pawn_index < MAX_NUM_OF_PAWNS:
                other_pawn = players[player_index].pawns[pawn_index]

                if current_pawn.is_same_as(other_pawn) == False:
                    if current_pawn.has_same_position_as(other_pawn):
                        other_pawn.reset()

                pawn_index += 1

            player_index += 1
        
    def validate_selected_pawn(self, selected_pawn, selected_option):
        self.print_temp_debug_message("DEBUG: Entering vaildate_selected_pawn()\n")

        valid = False
        all_options = self.all_options

        current_card = self.deck.deck[self.card_num]
        valid = self.all_options_pawns[CARD_LABEL.index(current_card.label)][selected_option][selected_pawn]
        
        if valid == False:
            self.player_status(self.current_player_turn)
            self.print_debug_message()
        
        self.print_temp_debug_message("DEBUG: Exiting vaildate_selected_pawn()\n")
        return valid
    
    def validate_selected_moves(self, selected_pawn, selected_moves, selected_pawn_two):
        self.print_temp_debug_message("DEBUG: Entering vaildate_selected_moves()\n")

        valid = False
        all_options = self.card_7_option_two_choices

        pawn_index = 0
        while pawn_index < MAX_NUM_OF_PAWNS:
            valid = all_options[selected_pawn][selected_moves][selected_pawn_two]
            if valid == True:
                break

            pawn_index += 1
        
        if valid == False:
            self.player_status(self.current_player_turn)
            self.print_debug_message()
        
        self.print_temp_debug_message("DEBUG: Exiting vaildate_selected_moves()\n")
        return valid
    
    def validate_selected_other_player_pawn(self, selected_pawn, selected_pawn_two, other_player_index):
        self.print_temp_debug_message("DEBUG: Entering validate_selected_other_player_pawn()\n")

        valid = self.players[self.current_player_turn].pawns[selected_pawn].board_position_swappable()
        if valid == True:
            valid = self.players[other_player_index].pawns[selected_pawn_two].board_position_swappable()
        
        self.print_temp_debug_message("DEBUG: Exiting validate_selected_other_player_pawn()\n")
        return valid
    
    def slide_foward(self, players, pawn, moves = 1):
        while moves > 0:
            pawn.board_position += 1
            self.take_over_position(players, pawn)
            moves -= 1

        return pawn
        
    def move_forward(self, pawn, spaces = 1):
        while spaces > 0:
            if pawn.board_position == pawn.home_position:
                if pawn.in_safety_zone == False:
                    pawn.in_safety_zone = True
                else:
                    pawn.safety_zone_position += 1
            else:
                pawn.board_position += 1

                if pawn.board_position > MAX_BOARD_POSITION:
                    pawn.board_position = MIN_BOARD_POSITION

            spaces -= 1
        
        return pawn
                
    def move_backward(self, pawn, spaces = 1):
        while spaces > 0:
            if pawn.at_start == False:
                if pawn.at_home == False:
                    if pawn.in_safety_zone == True:
                        if pawn.safety_zone_position == MIN_SAFETY_ZONE_POSITION:
                            pawn.in_safety_zone = False
                        else:
                            pawn.safety_zone_position -= 1
                    else:
                        pawn.board_position -= 1

                        if pawn.board_position < MIN_BOARD_POSITION:
                            pawn.board_position = MAX_BOARD_POSITION

            spaces -= 1

        return pawn

    def player_action(self, selected_option, selected_pawn, selected_moves = -1, selected_pawn_two = -1, other_player_index = -1):
        self.clear_debug_message()
        self.print_temp_debug_message("DEBUG: Entering player_action()\n")

        current_card = self.deck.deck[self.card_num].label
        players = self.players
        current_player_turn = self.current_player_turn
        current_player = players[current_player_turn]
        current_pawn = current_player.pawns[selected_pawn]

        if selected_pawn_two > -1:
            current_pawn_two = current_player.pawns[selected_pawn_two]

        if other_player_index > -1:
            other_player_pawn = players[other_player_index].pawns[selected_pawn_two]

        self.in_player_action = True
        while self.in_player_action == True:
            if selected_option not in [OPTION_SELECTION.index("OPTION_ONE"), OPTION_SELECTION.index("OPTION_TWO"), OPTION_SELECTION.index("FORFEIT")]:
                break

            if selected_option == OPTION_SELECTION.index("FORFEIT"):
                break

            if current_card == "1":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_1_option_1_action(current_pawn)

                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_1_option_2_action(current_pawn)

                self.in_player_action = False

            elif current_card == "2":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_2_option_1_action(current_pawn)

                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_2_option_2_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "3":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_3_option_1_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "4":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_4_option_1_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "5":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_5_option_1_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "7":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_7_option_1_action(current_pawn)

                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_7_option_2_action(current_pawn, current_pawn_two, selected_moves)
                    self.pawn_checks(players, current_pawn_two)
                
                self.in_player_action = False

            elif current_card == "8":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_8_option_1_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "10":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_10_option_1_action(current_pawn)

                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_10_option_2_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "11":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_11_option_1_action(current_pawn)

                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_11_option_2_action(current_pawn, other_player_pawn)
                    self.pawn_checks(players, other_player_pawn)
                
                self.in_player_action = False

            elif current_card == "12":
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    self.card_12_option_1_action(current_pawn)
                
                self.in_player_action = False

            elif current_card == "SORRY":
                #if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    #self.card_sorry_option_1_action(current_pawn)

                if selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    self.card_sorry_option_2_action(current_pawn)
                
                self.in_player_action = False
            
            self.pawn_checks(players, current_pawn)

            DO_NOT_RUN_BLOCK = True
            if DO_NOT_RUN_BLOCK == False:
                print("DEBUG: Card Label: " + str(self.deck.deck[self.card_num].label))
                
                # Option One
                if selected_option == OPTION_SELECTION.index("OPTION_ONE"):
                    if self.deck.deck[self.card_num].label == "SORRY!":
                        print("SORRY!")
                                
                # Option Two
                elif selected_option == OPTION_SELECTION.index("OPTION_TWO"):
                    
                    if self.deck.deck[self.card_num].label == "7":
                        self.split_pawn()

                    elif self.deck.deck[self.card_num].label == "10":
                        moves = 1
                        pawn = self.select_pawn()

                        if self.players[self.current_player_turn].pawns[pawn].at_start == False:
                            index = 0
                            while index < moves:
                                if self.players[self.current_player_turn].pawns[pawn].at_start == False:
                                    self.move_backward(pawn)

                                index += 1
                        
                    elif self.deck.deck[self.card_num].label == "11":
                            self.swap_pawn()
                            
                #Forfeit
                elif selected_option == OPTION_SELECTION.index("FORFEIT"):
                    i = 0
        
        self.print_temp_debug_message("DEBUG: Exiting player_action()\n")

    def check_end_position_valid(self, current_pawn, option_index):
        valid = True

        if current_pawn.valid_position() == False:
            valid = False
            self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID because PLAYER " + str(self.current_player_turn) + " PAWN " + str(current_pawn.pawn_num) + "'s END board_position NOT VALID. ")
        
        return valid

    def check_end_position_occupied(self, current_pawn, option_index):
        valid = True

        temp_pawn_index = 0
        while temp_pawn_index < MAX_NUM_OF_PAWNS:
            if temp_pawn_index != current_pawn.pawn_num:
                temp_pawn = self.players[self.current_player_turn].pawns[temp_pawn_index]

                if current_pawn.has_same_position_as(temp_pawn) == True:
                    valid = False
                    self.add_debug_message(OPTION_SELECTION[option_index] + " is NOT VALID for PLAYER " + str(self.current_player_turn) + " PAWN " + str(current_pawn.pawn_num) + "'s END POSITION is occupied by PAWN " + str(temp_pawn_index) + ". ")
                    break

            temp_pawn_index += 1
        
        return valid

    def check_slide_position(self, players, pawn):
        if pawn.board_position in SLIDE_POSITION_SHORT:
            short_slide_index = 0
            while short_slide_index < MAX_NUM_OF_PLAYERS:
                if self.current_player_turn != short_slide_index:
                    if pawn.board_position == SLIDE_POSITION_SHORT[short_slide_index]:
                        pawn = self.slide_foward(players, pawn, 3)
                        break
                
                short_slide_index += 1
        
        if pawn.board_position in SLIDE_POSITION_LONG:
            long_slide_index = 0
            while long_slide_index < MAX_NUM_OF_PLAYERS:
                if self.current_player_turn != long_slide_index:
                    if pawn.board_position == SLIDE_POSITION_SHORT[long_slide_index]:
                        pawn = self.slide_foward(players, pawn, 4)
                        break

                long_slide_index += 1

        return pawn
            
    def swap_pawn(self):
        pawn = -1
        target_player = -1
        target_pawn = -1

        while pawn == -1:
            pawn = self.select_pawn()

            if self.players[self.current_player_turn].pawns[pawn].board_position_swappable() == True:
                target_player, target_pawn = self.select_pawn_other_players() # select other player pawn to swap position
                temp_board_location = self.players[self.current_player_turn].pawns[pawn].board_position
                self.players[self.current_player_turn].pawns[pawn].board_position = self.players[target_player].pawns[target_pawn].board_position
                self.players[target_player].pawns[target_pawn].board_position = temp_board_location
                print("Swap Made")

            else:
                print("invalid move")
                pawn = -1

    def select_pawn_other_players(self):
        print("DEBUG: HERE")
        in_select_pawn_other_players = True
        self.mouse_pressed = True
        pawn_options = []
        moves_first = 0

        while in_select_pawn_other_players:
            mouse_pos = pygame.mouse.get_pos()

            x_pos_options = 50
            y_pos_options = 600
            button_width = 50
            button_height = 50
            
            self.black_screen()
            self.draw_board()
            self.menu_play_panel()
            self.button_menu_start()

            index = 0
            while index < MAX_NUM_OF_PLAYERS:
                if index != self.current_player_turn:
                    x_pos_options = 50
                    index1 = 0
                    while index1 < MAX_NUM_OF_PAWNS:
                        if self.players[index].pawns[index1].board_position_swappable() == True:
                            #
                            pawn_selection = menu_button.menu_button(str(index) + str(index1), x_pos_options, y_pos_options, button_width, button_height).draw(self.screen, mouse_pos)
                            while pawn_selection:
                                return index, index1
                            
                            pawn_options.append(pawn_selection)
                            x_pos_options += button_width * 2
                        index1 += 1
                        
                    y_pos_options += button_height
                index += 1
                
            self.button_close_corner()
                    
            pygame.display.flip()
            
    def split_pawn(self):
        moves = 7
        pawn = self.select_pawn()
        moves = self.split_option(moves, pawn)

    def split_option(self, moves, pawn):
        self.in_split_option = True
        self.mouse_pressed = True
        option_move_spaces = []
        moves_first = 0
        
        while self.in_split_option:
            self.mouse_pos = pygame.mouse.get_pos()

            x_pos_options = 50
            y_pos_options = 800
            button_width = 50
            button_height = 50
            
            self.black_screen()
            self.draw_board()
            self.menu_play_panel()
            self.button_close_corner()

            index = 0
            while index < moves:
                option_move_spaces.append(menu_button.menu_button(str(index + 1), x_pos_options, y_pos_options, button_width, button_height).draw(self.screen, self.mouse_pos))

                while option_move_spaces[index]:
                    if not self.mouse_pressed:
                        self.mouse_pressed = True
                        self.in_split_option = False
                        moves_first = index + 1
                    break
                
                x_pos_options += button_width * 2
                index += 1
                
            self.button_close_corner()

            pygame.display.flip()

        while moves_first > 0:
            self.move_forward(pawn)
            moves_first -=1
            moves -= 1
            
        pawn = self.select_pawn()

        while moves > 0:
            self.move_forward(pawn)
            moves -= 1
    
    def player_status(self, player_index):
        print("Player: " + "\t\t" + str(player_index))
        self.players[player_index].stat()

    def player_status_all(self):
        print("Current Player: " + str(self.current_player_turn) + "\n")

        player_index = 0
        while player_index < MAX_NUM_OF_PLAYERS:
            self.player_status(player_index)
            player_index += 1
