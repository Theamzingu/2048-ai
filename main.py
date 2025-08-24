import pygame
import random
from ai import expectimax_player
from game import GameState, new_game_tile, take_turn
pygame.init()

width = 600
height = 700
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# tile colors
colors = {0: (204, 192, 179), 
          2: (238, 228, 218), 
          4: (237, 224, 200), 
          8: (242, 177, 121), 
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'background': (187, 173, 160)}

# game variables init
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_state = GameState(board_values, score = 0)
game_over = False
new_tile = True
ai_playing = False
key_orientation = ''
suggested_move = ''
file = open('high_score.txt', 'r')
high_score_value = int(file.readline())
file.close()
high_score = high_score_value

# board dimensions and colors
def draw_board():
    pygame.draw.rect(screen, colors['background'], [0, 0, 600, 600], 0, 10)
    score_text = font.render('Score: ' + str(game_state.score), True, colors['dark text'])
    high_score_text = font.render('High Score: ' + str(high_score), True, colors['dark text'])
    move_suggestion_text = font.render(f'Suggested Move: {suggested_move}', True, colors['dark text'])
    screen.blit(score_text, (10, 610))
    screen.blit(high_score_text, (400, 610))
    screen.blit(move_suggestion_text, (10, 640))

# draw pieces on board and color code them acordingly
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 150 + 15, i * 150 + 15, 125, 125], 0, 10)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center = (j * 150 + 78, i * 150 + 78))
                screen.blit(value_text, text_rect)

# draws game over screen
def draw_over():
    pygame.draw.rect(screen, colors['background'], [0, 0, 600, 600], 0, 10)
    game_over_text = font.render('Game Over', True, colors['dark text'])
    game_over_restart = font.render('Press Enter to Restart', True, colors['dark text'])
    screen.blit(game_over_text, (200, 200))
    screen.blit(game_over_restart, (150, 300))

# main game
run = True
while run:
    timer.tick(fps)
    ai_play_next_move = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                key_orientation = 'down'
            elif event.key == pygame.K_UP:
                key_orientation = 'up'
            elif event.key == pygame.K_LEFT:
                key_orientation = 'left'
            elif event.key == pygame.K_RIGHT:
                key_orientation = 'right'
            elif event.key == pygame.K_n:
                ai_play_next_move = True
            elif event.key == pygame.K_SPACE:
                ai_playing = not ai_playing
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    game_state = GameState(board_values, score = 0)
                    game_over = False
                    new_tile = True
                    key_orientation = ''
                    suggested_move = ''
                    ai_playing = False

    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if new_tile:
        board_values, game_over = new_game_tile(board_values)
        suggested_move = expectimax_player(game_state, 5)[1]
        new_tile = False
    if ai_playing or ai_play_next_move:
        key_orientation = suggested_move
    if key_orientation != '':
        take_turn(game_state, key_orientation)
        key_orientation = ''
        new_tile = True
    if game_over:
        draw_over()
        if high_score > high_score_value:
            file = open('high_score.txt', 'w')
            file.write(str(high_score))
            file.close()
            high_score_value = high_score

    if game_state.score > high_score:
        high_score = game_state.score


    pygame.display.flip()
pygame.quit()

# next time: alpha-beta pruning, win and loss conditions
# QOL: change text to show ai is playing, winning screen