# Originally written By Code Monkey King
# Source: https://github.com/maksimKorzh/tictactoe-mtcs/tree/master/src/tutorials/game_loop
# Edited by Abdellah Lahnaoui and Ben Platten from group 24

# packages
from copy import deepcopy
import random
from mcts import *
# Tic Tac Toe board class


class Board():
    # create constructor (init board class instance)
    def __init__(self, board=None):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'

        # define board position
        self.position = {}

        # init (reset) board
        self.init_board()

        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    # init (reset) board
    def init_board(self):
        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                # set every board square to empty square
                self.position[row, col] = self.empty_square
    # NOTE: Should this be toggled by an option? Or make a completely seperate file for the TAs?
    # Initialize a limited board similar to the one in the assignment
    # def init_board(self):
    #     self.position[0, 0] = self.empty_square
    #     self.position[0, 1] = self.player_2
    #     self.position[0, 2] = self.empty_square

    #     self.position[1, 0] = self.player_1
    #     self.position[1, 1] = self.player_1
    #     self.position[1, 2] = self.player_2

    #     for i in range(3):
    #         self.position[2, i] = self.empty_square

    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = Board(self)

        # make move
        board.position[row, col] = self.player_1

        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        # return new board state
        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                # this is not a draw
                return False

        # by default we return a draw
        return True

    # get whether the game is won
    def is_win(self):
        ##################################
        # vertical sequence detection
        ##################################

        # loop over board columns
        for col in range(3):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for row in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True

        ##################################
        # horizontal sequence detection
        ##################################

        # loop over board columns
        for row in range(3):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for col in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True

        ##################################
        # 1st diagonal sequence detection
        ##################################

        # define winning sequence list
        winning_sequence = []

        # loop over board rows
        for row in range(3):
            # init column
            col = row

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True

        ##################################
        # 2nd diagonal sequence detection
        ##################################

        # define winning sequence list
        winning_sequence = []

        # loop over board rows
        for row in range(3):
            # init column
            col = 3 - row - 1

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True

        # by default return non winning state
        return False

    # generate legal moves to play in the current position
    # NOTE: actions are not used currently but I left them in case we need them later
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
        actions = []
        empty_tiles = []
        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/board state to action list
                    actions.append(self.make_move(row, col))
                    empty_tiles.append((row, col))

        # return the list of available actions (board class instances)
        return actions, empty_tiles

    # main game loop
    def game_loop(self):
        print('\n  Tic Tac Toe with Monte Carlo Tree Search\n')
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')

        # print board
        print(self)

        # game loop
        while True:
            # get user input
            user_input = input('> ')

            # escape condition
            if user_input == 'exit':
                break

            # skip empty input
            if user_input == '':
                continue

            try:
                # parse user input (move format [col, row]: 1,2)
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1

                # check move legality
                if self.position[row, col] != self.empty_square:
                    print(' Illegal move!')
                    continue

                # make move on board
                self = self.make_move(row, col)

                # print board
                print(self)

                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break

                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break

                # 2nd player phase
                a, empty_tiles = self.generate_states()
                rand_move_row, rand_move_col = random.choice(empty_tiles)
                self = self.make_move(rand_move_row, rand_move_col)

                # print board
                print(self)

                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break

                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break

            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print(
                    '  Move format [x,y]: 1,2 where 1 is column and 2 is row')

    # print board state
    def __str__(self):
        # define board string representation
        board_string = ''

        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                board_string += ' %s' % self.position[row, col]

            # print new line every row
            board_string += '\n'

        # prepend side to move
        if self.player_1 == 'x':
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string

        elif self.player_1 == 'o':
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string

        # return board string
        return board_string


# main driver
if __name__ == '__main__':
    # create board instance
    board = Board()

    # start game loop
    #board.game_loop()

    mcts = MCTS()

    # simulate random game
    mcts.rollout(board)
