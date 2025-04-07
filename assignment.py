import random
import pygame

pygame.init()

# Game variables and constants
width = 600
height = 600
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (128, 128, 128)
fps = 60
timer = pygame.time.Clock()
rows = 6
cols = 8
correct = [[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]]
options_list = []
space = []
used = []
new_board = True
first_guess = None
second_guess = None
score = 0
best_score = 0
matches = 0
game_over = False
flip_in_progress = False  # Track if a flip is in progress

# Screen setup
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Matching Game!')
title_font = pygame.font.Font('freesansbold.ttf', 56)
small_font = pygame.font.Font('freesansbold.ttf', 26)

def generate_board():
    global options_list
    global space
    global used
    for item in range(rows * cols // 2):
        options_list.append(item)

    for item in range(rows * cols):
        piece = options_list[random.randint(0, len(options_list) - 1)]
        space.append(piece)
        if piece in used:
            used.remove(piece)
            options_list.remove(piece)
        else:
            used.append(piece)

def draw_backgrounds():
    top_menu = pygame.draw.rect(screen, black, [0, 0, width, 100])
    title_text = title_font.render('The Matching Game!', True, white)
    screen.blit(title_text, (10, 20))
    board_space = pygame.draw.rect(screen, gray, [0, 100, width, height - 200], 0)
    bottom_menu = pygame.draw.rect(screen, black, [0, height - 100, width, 100], 0)
    restart_button = pygame.draw.rect(screen, gray, [10, height - 90, 200, 80], 0, 5)
    restart_text = title_font.render('Restart', True, white)
    screen.blit(restart_text, (10, 520))
    score_text = small_font.render(f'Current Turns: {score}', True, white)
    screen.blit(score_text, (350, 520))
    best_text = small_font.render(f'Previous Best: {best_score}', True, white)
    screen.blit(best_text, (350, 560))
    return restart_button

def flip_card_animation(index):
    global flip_in_progress
    if flip_in_progress:
        return  # Prevent another flip while one is in progress

    flip_in_progress = True  # Mark that a flip is in progress
    col = index // rows
    row = index % rows
    x = col * 76 + 12
    y = row * 65 + 112
    card_value = space[index]

    # Animate flip (flip over to show back, then front)
    for scale in range(0, 26, 5):
        pygame.draw.rect(screen, gray, [x - 2, y - 2, 54, 54])  # border
        pygame.draw.rect(screen, white, [x + 25 - scale, y, scale * 2, 50], 0, 4)  # flip effect
        pygame.display.update()
        pygame.time.delay(20)
        
    # After flip, show the card value
    text = small_font.render(str(card_value), True, blue)
    screen.blit(text, (x + 18, y + 12))
    pygame.display.update()

    pygame.time.delay(500)  # Pause to let the player see the card value
    flip_in_progress = False  # Allow for the next flip after the animation

def draw_board():
    global rows
    global cols
    global correct
    board_list = []
    for i in range(cols):
        for j in range(rows):
            piece = pygame.draw.rect(screen, white, [i * 75 + 12, j * 65 + 112, 50, 50], 0, 4)
            board_list.append(piece)

    for r in range(rows):
        for c in range(cols):
            if correct[r][c] == 1:
                pygame.draw.rect(screen, green, [c * 75 + 10, r * 65 + 110, 54, 54], 3, 4)
                piece_text = small_font.render(f'{space[c * rows + r]}', True, black)
                screen.blit(piece_text, (c * 75 + 18, r * 65 + 120))

    return board_list

def check_guesses():
    global first_guess, second_guess, score, matches
    if space[first_guess] == space[second_guess]:
        col1 = first_guess // rows
        col2 = second_guess // rows
        row1 = first_guess - (first_guess // rows * rows)
        row2 = second_guess - (second_guess // rows * rows)
        if correct[row1][col1] == 0 and correct[row2][col2] == 0:
            correct[row1][col1] = 1
            correct[row2][col2] = 1
            score += 1
            matches += 1
    else:
        score += 1

    first_guess = None
    second_guess = None

running = True
while running:
    timer.tick(fps)
    screen.fill(white)
    if new_board:
        generate_board()
        new_board = False

    restart = draw_backgrounds()
    board = draw_board()

    # Check for card matches if two cards have been flipped
    if first_guess is not None and second_guess is not None:
        check_guesses()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)):
                button = board[i]
                if not game_over:
                    if button.collidepoint(event.pos) and first_guess is None:
                        first_guess = i
                        flip_card_animation(i)  # Flip first card
                    elif button.collidepoint(event.pos) and second_guess is None and i != first_guess:
                        second_guess = i
                        flip_card_animation(i)  # Flip second card

            if restart.collidepoint(event.pos):
                options_list = []
                used = []
                space = []
                new_board = True
                score = 0
                matches = 0
                first_guess = None
                second_guess = None
                correct = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                game_over = False

    if matches == rows * cols // 2:
        game_over = True
        winner = pygame.draw.rect(screen, gray, [10, height - 300, width - 20, 80], 0, 5)
        winner_text = title_font.render(f'Your score is {score} !', True, white)
        screen.blit(winner_text, (10, height - 290))
        if best_score > score or best_score == 0:
            best_score = score

    pygame.display.flip()
pygame.quit()
