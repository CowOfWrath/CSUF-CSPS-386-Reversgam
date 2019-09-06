# Ryan Chen
# 893219394
# California State University, Fullerton
# CPSC 386
# This application is a text version of Othello
# Source code is taken or derived from the following book:
# Invent Your Own Computer Games with Python by Al Sweigart

import random
import sys

# Game board parameters
WIDTH = 8
HEIGHT = 8


# outputs the current board state
def draw_board(board):
    print('   1 2 3 4 5 6 7 8')
    print(' + - - - - - - - - +')
    for y in range(HEIGHT):
        print('%s| ' % chr(ord('A') + y), end='')
        for x in range(WIDTH):
            print(board[x][y] + ' ', end='')
        print('|%s' % chr(ord('A') + y))
    print(' + - - - - - - - - +')
    print('   1 2 3 4 5 6 7 8')


# create blank board data structure
def get_new_board():
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    return board


# returns False if player's move is invalid
# returns list of spaces that change ownership on valid move
def is_valid_move(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
        return False

    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'

    tiles_to_filp = []
    for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdir
        y += ydir
        while is_on_board(x, y) and board[x][y] == other_tile:
            x += xdir
            y += ydir
            if is_on_board(x, y) and board[x][y] == tile:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    tiles_to_filp.append([x, y])

    if len(tiles_to_filp) == 0:
        return False

    return tiles_to_filp


# returns True of coordinates are locaed on the board
def is_on_board(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1


# returns a copy of the current board with valid moves marked with "."
def get_board_with_valid_moves(board, tile):
    board_copy = get_board_copy(board)

    for x, y in get_valid_moves(board_copy, tile):
        board_copy[x][y] = '.'

    return board_copy


# returns a list of valid moves
def get_valid_moves(board, tile):
    valid_moves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_valid_move(board, tile, x, y) != False:
                valid_moves.append([x, y])

    return valid_moves


# returns the score for each player
def get_score_of_board(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1

    return {'X': xscore, 'O': oscore}


# allow player to enger which tile want to be
# return list [player_tile, computer_tile]
def enter_player_tile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def who_goes_first():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


# return false if invalid move
# return true if valid move
def make_move(board, tile, xstart, ystart):
    tiles_to_flip = is_valid_move(board, tile, xstart, ystart)

    if tiles_to_flip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile

    return True


def get_board_copy(board):
    board_copy = get_new_board()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board_copy[x][y] = board[x][y]

    return board_copy


def is_on_corner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


def get_player_move(board, player_tile):
    DIGIT_1_TO_8 = '1 2 3 4 5 6 7 8'.split()
    ALPHA_A_TO_H = 'A B C D E F G H'.split()

    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGIT_1_TO_8 and move[1].upper() in ALPHA_A_TO_H:
            x = int(move[0]) - 1
            y = int(ord(move[1].upper()) - ord('A'))
            if is_valid_move(board, player_tile, x, y) == False:
                continue
            else:
                break
        elif len(move) == 2 and move[1] in DIGIT_1_TO_8 and move[0].upper() in ALPHA_A_TO_H:
            x = int(move[1]) - 1
            y = int(ord(move[0].upper()) - ord('A'))
            if is_valid_move(board, player_tile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter a row (A-H) and a column (1-8).')
            print('For example, A1 or 1a will move on the top-left corner.')

    return [x, y]


def get_computer_move(board, computer_tile):
    possible_moves = get_valid_moves(board, computer_tile)
    random.shuffle(possible_moves)
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]

    best_score = -1
    for x, y in possible_moves:
        board_copy = get_board_copy(board)
        make_move(board_copy, computer_tile, x, y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score

    return best_move


def print_score(board, player_tile, computer_tile):
    scores = get_score_of_board(board)
    print('You: %s points. Computer: %s points.'
          % (scores[player_tile], scores[computer_tile]))


# game loop
def play_game(player_tile, computer_tile):
    show_hints = False
    turn = who_goes_first()
    print('The ' + turn + 'will go first.')

    # initial board setup
    board = get_new_board()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        player_valid_moves = get_valid_moves(board, player_tile)
        computer_valid_moves = get_valid_moves(board, computer_tile)
        if player_valid_moves == [] and computer_valid_moves == []:
            return board
        elif turn == 'player':
            if player_valid_moves != []:
                if show_hints:
                    valid_moves_board = get_board_with_valid_moves(board, player_tile)
                    draw_board(valid_moves_board)
                else:
                    draw_board(board)

                print_score(board, player_tile, computer_tile)

                move = get_player_move(board, player_tile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    show_hints = not show_hints
                    continue
                else:
                    make_move(board, player_tile, move[0], move[1])

            turn = 'computer'

        elif turn == 'computer':
            if computer_valid_moves != []:
                draw_board(board)
                print_score(board, player_tile, computer_tile)

                input('Press Enter to see the computer\'s move.')

                move = get_computer_move(board, computer_tile)
                make_move(board, computer_tile, move[0], move[1])

            turn = 'player'


# game run code
print('Welcome to Reversegam!')
player_tile, computer_tile = enter_player_tile()

while True:
    final_board = play_game(player_tile, computer_tile)
    draw_board(final_board)
    scores = get_score_of_board(final_board)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))

    if scores[player_tile] > scores[computer_tile]:
        print('You beat the computer by %s points! Congratulations!'
              % (scores[player_tile] - scores[computer_tile]))
    elif scores[player_tile] < scores[computer_tile]:
        print('You lost. The computer beat you by %s points.'
              % (scores[computer_tile] - scores[player_tile]))
    else:
        print('The game was a tie!')

    print('Do you want to play again! (yes or no)')
    if not input().lower().startswith('y'):
        break
