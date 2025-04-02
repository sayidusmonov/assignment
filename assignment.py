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
first_guest_num = 0 
second_guest_num = 0 
score = 0 
best_score = 0 
matches = 0 
game_over = False
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Matching Game!')
title_fon = pygame.front.Font('freesansbold.ttf', 56)
small_front = pygame.front.Front('freesansbold.ttf', 26)

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
