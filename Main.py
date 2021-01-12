import pygame
import numpy
import math
import sys

num_columns = 7
num_rows = 6

board = numpy.zeros((num_rows, num_columns))

game_over = False

pygame.init()

pygame.display.set_caption('CONNECT 4')

black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

square_size = 90
screen_width = square_size * num_columns
screen_height = square_size * (num_rows + 1)
screen = pygame.display.set_mode((screen_width, screen_height))

radius = int(square_size / 2 - 10)
circle_centre = int(square_size / 2)

turn = 0
red_player = 0
yellow_player = 1


def drop_piece(board, next_open_row, player_move, piece):
    board[next_open_row][player_move] = piece


def get_next_open_row(board, player_move):
    for row in range(num_rows - 1, -1, -1):
        if board[row][player_move] == 0:
            return row


def valid_move(board, player_move):
    return board[0][player_move] == 0


def display_winner(player_won):
    winner_font = pygame.font.SysFont("broadway", 45, bold=False)
    winner_text = winner_font.render("PLAYER " + str(player_won) + " WINS", True, (0, 255, 0))
    pygame.draw.rect(screen, black, (0, 0, square_size * num_columns, square_size))
    screen.blit(winner_text, (130, 20))


def check_win():
    global game_over

    for i in range(0, num_rows - 3):
        for j in range(0, num_columns - 3):
            if board[i][j] == board[i + 1][j + 1] and board[i][j] == board[i + 2][j + 2] and \
                    board[i][j] == board[i + 3][j + 3]:
                if board[i][j] == 1:
                    display_winner(1)
                    game_over = True
                elif board[i][j] == 2:
                    display_winner(2)
                    game_over = True

    for i in range(1, num_rows - 2):
        for j in range(0, num_columns - 3):
            if board[num_rows - i][j] == board[num_rows - i - 1][j + 1] \
                    and board[num_rows - i][j] == board[num_rows - i - 2][j + 2] and \
                    board[num_rows - i][j] == board[num_rows - i - 3][j + 3]:
                if board[num_rows - i][j] == 1:
                    display_winner(1)
                    game_over = True
                elif board[num_rows - i][j] == 2:
                    display_winner(2)
                    game_over = True

    for i in range(0, num_rows - 3):
        for j in range(0, num_columns):
            if board[i][j] == board[i + 1][j] and board[i][j] == board[i + 2][j] and board[i][j] == board[i + 3][j]:
                if board[i][j] == 1:
                    display_winner(1)
                    game_over = True
                elif board[i][j] == 2:
                    display_winner(2)
                    game_over = True

    for i in range(0, num_rows):
        for j in range(0, num_columns - 3):
            if board[i][j] == board[i][j + 1] and board[i][j] == board[i][j + 2] and board[i][j] == board[i][j + 3]:
                if board[i][j] == 1:
                    display_winner(1)
                    game_over = True
                elif board[i][j] == 2:
                    display_winner(2)
                    game_over = True


def draw_board():
    for row in range(num_rows):
        for col in range(num_columns):
            pygame.draw.rect(screen, blue, (square_size * col, square_size * row + square_size, square_size,
                                            square_size))
            if board[row][col] == 0:
                pygame.draw.circle(screen, white, (square_size * col + circle_centre, square_size * row +
                                                   square_size + circle_centre), radius)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, red, (square_size * col + circle_centre, square_size * row +
                                                 square_size + circle_centre), radius)
            else:
                pygame.draw.circle(screen, yellow, (square_size * col + circle_centre, square_size * row +
                                                    square_size + circle_centre), radius)

    pygame.display.update()


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, square_size * num_columns, square_size))
            x_pos = event.pos[0]
            if turn == red_player:
                pygame.draw.circle(screen, red, (x_pos, circle_centre), radius)
            elif turn == yellow_player:
                pygame.draw.circle(screen, yellow, (x_pos, circle_centre), radius)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == red_player:
                x_pos = event.pos[0]
                player_move = math.floor(x_pos / square_size)
                if valid_move(board, player_move):
                    next_open_row = get_next_open_row(board, player_move)
                    drop_piece(board, next_open_row, player_move, 1)
                    pygame.draw.circle(screen, yellow, (x_pos, circle_centre), radius)
                else:
                    turn = -1

            else:
                x_pos = event.pos[0]
                player_move = math.floor(x_pos / square_size)
                if valid_move(board, player_move):
                    next_open_row = get_next_open_row(board, player_move)
                    drop_piece(board, next_open_row, player_move, 2)
                    pygame.draw.circle(screen, red, (x_pos, circle_centre), radius)
                else:
                    turn = 0

            turn += 1
            turn = turn % 2

        draw_board()
        check_win()

    pygame.display.update()

pygame.time.wait(3000)


