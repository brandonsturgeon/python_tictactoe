#!/usr/bin/env python

import os
import random

####################
#    PycTacToe     #
# Brandon Sturgeon #
####################

# Things I would do if I spent more time on this:
#
# - Improve efficiency of victory conditions (Check based on last move)
#   - Also ensure that there isn't a checking priority (eg: check horizontal before vertical, etc.)
#     to avoid awarding the win to the wrong player
#
# - Improve user interface
#   - O's look a bit like 0's which is confusing when using number placeholders
#   - I would also replace all of the numbers with "_" instead. It looks much better.
#   - "Invalid Command" error should be improved to reflect the multiple error states (can't place in an already used square, or unrecognized command)
#   - Maybe I could reformat the numbers so they mimic the keyboard's numpad, making the play experience more intuitive
#
# - Add tests
#
# - Add 'Play again?' functionality
#
# - I don't like how both turns happen seemingly simultaneously,
#   I would find some way (perhaps a delay or something) to make it appear more interactive
#
# - Refine the victory conditions, they're a little messy right now.

class BoardRow:
    def __init__(self, defaults):
        self.left = defaults["left"]
        self.middle = defaults["middle"]
        self.right = defaults["right"]

    def set_left(self, new_value):
        self.left = new_value

    def set_middle(self, new_value):
        self.middle = new_value

    def set_right(self, new_value):
        self.right = new_value

    def get_values(self):
        return [self.left, self.middle, self.right]

    def render(self):
        return "|{}|{}|{}|".format(self.left, self.middle, self.right)

class Board:
    def __init__(self, player_letters):

        # I opted to use a class system instead of the traditional array
        # of strings because it feels much cleaner to me

        self.letters = player_letters

        self.top    = BoardRow({ "left": "1", "middle": "2", "right": "3" })
        self.middle = BoardRow({ "left": "4", "middle": "5", "right": "6" })
        self.bottom = BoardRow({ "left": "7", "middle": "8", "right": "9" })

        self.rows = [
            self.top,
            self.middle,
            self.bottom
        ]

        self.set_square = {
            "1": self.top.set_left,
            "2": self.top.set_middle,
            "3": self.top.set_right,

            "4": self.middle.set_left,
            "5": self.middle.set_middle,
            "6": self.middle.set_right,

            "7": self.bottom.set_left,
            "8": self.bottom.set_middle,
            "9": self.bottom.set_right
        }
    
    def get_board_data(self):
        return [row.get_values() for row in self.rows]

    def get_diagonals(self):
        top_to_bottom = [self.top.left, self.middle.middle, self.bottom.right] 
        bottom_to_top = [self.bottom.left, self.middle.middle, self.top.right]

        diagonals = [top_to_bottom, bottom_to_top]

        return diagonals

    def get_horizontals(self):
        return self.get_board_data()

    def get_unplayed_squares(self):
        # Recipe for list comprehension:
        #     50% Magic
        #     50% Gross

        row_values = self.get_board_data()
        unplayed_squares = [str(value) for row_value in row_values for value in row_value if value not in ["X", "O"]]

        return unplayed_squares
    
    def get_verticals(self):
        left_column   = [self.top.left,   self.middle.left,   self.bottom.left  ]
        middle_column = [self.top.middle, self.middle.middle, self.bottom.middle]
        right_column  = [self.top.right,  self.middle.right,  self.bottom.right ]

        verticals = [left_column, middle_column, right_column]

        return verticals

    def check_for_win(self):
        horizontals = self.get_horizontals()
        verticals = self.get_verticals()
        diagonals = self.get_diagonals()

        directions = [horizontals, verticals, diagonals]

        for direction_data in directions:
            for pieces in direction_data:
                piece_set = set(pieces)

                # Converting to a set squashes duplicates,
                # if the length is 1 then all elements are the same letter
                if len(piece_set) == 1 :
                    return list(piece_set)[0]
        return None

    def make_move(self, square, letter):
        self.set_square[square](letter)

    def render(self):
        rows = [row.render() for row in self.rows]
        rendered_board = "\n".join(rows)

        print rendered_board

class Opponent:
    def __init__(self, letter):
        self.letter = letter

    def make_move(self, board):
        unplayed_squares = board.get_unplayed_squares()
        random_move = random.choice(unplayed_squares)

        board.make_move(random_move, self.letter)

class Game:
    def __init__(self):
        self.playing = True
        self.letters = {
            "player": "X",
            "opponent": "O"
        }
        self.board = Board(self.letters.values())
        self.opponent = Opponent(self.letters["opponent"])
        self.winner = None
        self.help_text = "Simply enter the number of the square you want to place your letter on"
        self.next_player = "player"
        self.invalid_command_count = 0

        self.main()

    @staticmethod
    def clear_screen():
        # Assign os.system output to an unused var to avoid it's output (0)
        # appearing in console. Using cls and clear for compatability
        _ = os.system("cls")
        _ = os.system("clear")

    def get_winner_from_letter(self, letter):
        for player, player_letter in self.letters.iteritems():
            if player_letter == letter:
                return player

    def get_valid_moves(self):
        unplayed_squares = self.board.get_unplayed_squares()
        return unplayed_squares

    def check_for_winner(self):
        winning_letter = self.board.check_for_win()
        if winning_letter is None:
            # If there is no winning letter but no open squares, it's a draw
            unplayed_squares = self.board.get_unplayed_squares()
            if len(unplayed_squares) == 0:
                self.playing = False
                self.winner = "whiskers the kitty cat"
                self.render_screen()
                print "It's a draw!"

        else:
            self.playing = False
            self.winner = self.get_winner_from_letter(winning_letter)
            self.render_screen()
            print "{} has won!".format(self.winner.capitalize())

    def print_help_message(self):
        print self.help_text

    def print_invalid_command_message(self):
        # Print help message every 3 invalid commands
        should_print_help = self.invalid_command_count % 3 == 0

        print ""
        print "Invalid Command"
        print ""

        if should_print_help:
            self.print_help_message()

    def render_screen(self):
        self.clear_screen()
        self.board.render()

    def main(self):

        self.render_screen()

        while self.playing:

            # Player
            if self.next_player == "player":
                move = raw_input("What's your move?: ").lower()

                if move == "help":
                    self.help_text

                elif move in ["exit", "quit", "qq", "stop", "end"]:
                    print ""
                    print "Exiting"
                    self.playing = False

                elif move in self.get_valid_moves():
                    self.board.make_move(move, self.letters["player"])
                    self.check_for_winner()

                    # This is a dumb check for whether or not a winner has been chosen,
                    # we don't want to clear the victory message!
                    if self.winner is None:
                        self.next_player = "opponent"
                        self.render_screen()

                else:
                    self.invalid_command_count += 1
                    self.render_screen()
                    self.print_invalid_command_message()

            # Opponent
            elif self.next_player == "opponent":
                self.opponent.make_move(self.board)
                self.check_for_winner()

                # This is a dumb check for whether or not a winner has been chosen,
                # we don't want to clear the victory message!
                if self.winner is None:
                    self.next_player = "player"
                    self.render_screen()

if __name__ == "__main__":
    Game()
