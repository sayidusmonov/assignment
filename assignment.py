import random 
import pygame 

pygame.init()

width = 600
height = 600
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (128, 128, 128)
fps = 120
timer = pygame.time.Clock()
row = 6
cols = 8
correct = [[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0], 
           [0, 0, 0, 0, 0, 0, 0, 0]
]

options_list = []
space = []
used = []
new_board = True 
first_guess = False
second_guess = False
first_guess_num = 0 
second_guess_num = 0 
score = 0 
best_score = 0 
matches = 0 
game_over = False

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Matching Game!')
title_font = pygame.front.Font('freesansbold.ttf', 56)
small_font = pygame.front.Front('freesansbold.ttf', 26)

def generate_board():
    global options_list 
    global space 
    global used 
    for item in range (row * cols // 2):
        options_list.append(item)

        for item in range (row * cols): 
            piece = options_list[random.randint(0, len(options_list) -1 )]
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

def draw_board(): 
    global row
    global cols 
    global correct
    board_list = []
    for i in range(cols):
        for j in range(row):
            piece = pygame.draw.rect(screen, white, [ i * 75 +12, j * 65 +112, 50, 50], 0, 4)
            board_list.append(piece)

    for r in range(row):
        for c in range(cols):
            if correct [r] [c] == 1:
                pygame.draw.rect(screen, green , [c * 75 +10, r * 65 +110, 54, 54 ], 3, 4)
                piece_text = small_font.rinder(f'{space[ c * row + r]}', True, black)
                screen.blit(piece_text, (c * 75 + 18 , r * 65 +120))

    return board_list

def chech_guess(firs, second): 
    global space 
    global correct 
    global score 
    global matches

    if space[firs] == space[second]:
        col1 = firs // row
        col2 = second // row
        row1 = firs - (firs // row * row)
        row2 = second - ( second // row * row)
        if correct[row1][col1] == 0 and correct[row1][col2] ==0:
            correct[row1][col1] = 1
            correct[row2][col2] = 1
            score += 1
            match += 1
    else:
        score += 1


running = True
while running:
    timer.tick(fps)
    screen.fill(white)
    if new_board :
        generate_board()
        new_board =False

    restart = draw_backgrounds()
    board =draw_board()

    if first_guess and second_guess:
        chech_guess(first_guess_num, second_guess_num)
        pygame.time.delay(1000)
        first_guess = False 
        second_guess = False

    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)): 
                button = board
                if not game_over: 
                    if button.collidepoint(event.pos) and not first_guess:
                        first_guess = True
                        first_guess = i 
                    if button.collidepoint(event.pos) and not second_guess and  first_guess and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i 
            if restart.collidepoint(event.pos): 
                options_list = []
                used = []
                space = [ ]
                new_board = True
                score = 0 
                matches = 0
                first_guess = False
                second_guess = False
                correct = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                game_over = False

    if matches == row * cols // 2:
        game_over = True
        winner = pygame.draw.rect(screen, gray, [ 10, height - 300, width - 20 , 80], 0, 5)
        winner_text = title_font.render(f'Your score is {score}!', True, white)
        screen.blit(winner_text, (10, height - 290))
        if best_score > score or best_score == 0 :
            best_score = score
